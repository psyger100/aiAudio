import os
import requests
import moviepy.editor as mp
from google.cloud import texttospeech, speech_v1 as speech
from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv()


def transcribe_audio(audio_file_path):
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  
    sample_rate_hertz=44100, 
    language_code="en-US" 
)
    response = client.recognize(config=config, audio=audio)
    transcription = ''
    for result in response.results:
        transcription += result.alternatives[0].transcript + ' '
    return transcription.strip()


def correct_transcription_with_gpt4o(transcription):
    url = os.getenv("ENDPOINT")
    headers = {
        "Content-Type": "application/json",
        "api-key":os.getenv("API_KEY"),  
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a transcription corrector."},
            {"role": "user", "content": transcription}
        ],
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    return response_data['choices'][0]['message']['content']


def synthesize_speech(text, output_audio_path):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-J" 
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_audio_path}"')
    audio = AudioSegment.from_file(output_audio_path)
    trimmed_audio  = audio[1500:] 
    trimmed_audio.export(output_audio_path, format="mp3")



def process_video(video_path):
    video = mp.VideoFileClip(video_path)
    audio_file_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_file_path)

    
    mono_audio_path = "temp_audio_mono.wav"
    os.system(f"ffmpeg -i {audio_file_path} -ac 1 {mono_audio_path}")

    
    transcription = transcribe_audio(mono_audio_path)
    print("Transcription:", transcription)

    
    corrected_transcription = correct_transcription_with_gpt4o(transcription)
    print("Corrected Transcription:", corrected_transcription)

    
    output_audio_path = "corrected_audio.mp3"
    synthesize_speech(corrected_transcription, output_audio_path)

    
    final_video_path = "final_video.mp4"
    final_video = video.set_audio(mp.AudioFileClip(output_audio_path))
    final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac")

    
    video.close()
    os.remove(audio_file_path)
    os.remove(mono_audio_path)  



if __name__ == "__main__":
    video_path = "input_video.mp4"  # Path to your input video file
    process_video(video_path)
