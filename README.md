# Video Transcription and Correction Tool

This project is a Python-based tool that processes video files to extract audio, transcribe the audio using Google Speech-to-Text, correct the transcription using Azure OpenAI's GPT-4o, synthesize speech with Google Text-to-Speech, and finally replace the original audio in the video with the corrected audio.

## Features

- Extracts audio from video files.
- Transcribes audio to text using Google Speech-to-Text.
- Corrects transcription using Azure OpenAI GPT-4o.
- Synthesizes corrected text back to speech using Google Text-to-Speech.
- Replaces original audio in the video with the synthesized audio.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- Google Cloud account with Speech-to-Text and Text-to-Speech enabled.
- Azure OpenAI account with access to GPT-4o.
- FFmpeg installed on your system (required for audio processing).

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory in your terminal.
3. Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables in a .env file in the project directory:
5. Ensure that FFmpeg is installed and added to your system's PATH.

## Usage

1. Place your video file in the project directory or provide the full path to the video file.
2. pdate the video_path variable in the **main** section of the code to point to your input video file:

   ```python
   video_path = "input_video.mp4"  # Path to your input video file
   ```

3. Run the script:

   ```bash
   python your_script_name.py
   ```

4. The output will be a video file named final_video.mp4 with the corrected audio.
