import argparse
import sounddevice as sd

from engine import TranscribeEngine
import threading
import time
import numpy as np
from scipy.io.wavfile import write
import os


is_recording = False
last_recorded_audio = None

FS = 44100  # Probing frequency


def run_cli():
    parser = argparse.ArgumentParser(description="TranscribeToolbox - CLI & Batch")
    parser.add_argument("--file", help="Path to single audio file")
    parser.add_argument("--dir", help="Path to folder (Batch mode)")
    
    args = parser.parse_args()
    engine = TranscribeEngine()

    if args.file:
        result = engine.transcribe(args.file)
        print(f"\nTranscription result:\n{result}")
    elif args.dir:
        print(f"Starting processing folder: {args.dir}")
        processed = engine.batch_process(args.dir)
        print(f"Finished! Processed files: {len(processed)}")
    else:
        parser.print_help()

def _record_loop():
    global last_recorded_audio
    global is_recording
    audio_chunks = []
    print("\nRecording started... you can talk now")
    try:
        with sd.InputStream(samplerate=FS, channels=1) as stream:
            while is_recording:
                # Read chunks of audio (e.g., 0.1 seconds)
                data, overflowed = stream.read(int(FS * 0.1))
                audio_chunks.append(data)
        
        # Concatenate all chunks
        if audio_chunks:
            recording = np.concatenate(audio_chunks, axis=0)
            last_recorded_audio = get_new_audio_file_name()
            write(last_recorded_audio, FS, recording)
            
            print(f"\nRecording saved: {last_recorded_audio}")
            
            # Schedule auto-transcription
            print("\nAuto-transcription starting in 5 seconds...")
            time.sleep(5)
            transcribe(last_recorded_audio)
    except Exception as e:
        print(f"\nError recording: {e}")
        is_recording = False


def get_new_audio_file_name():
    # use date time to create unique file name
    import datetime
    now = datetime.datetime.now()
    return f"recorded_audio_{now.strftime('%Y%m%d_%H%M%S')}.wav"   

def run_create_note():
    global is_recording
    # this function will start recording and wait for user to stop it, using interactive prompt in CLI

    # this function will create a note from transcrbed audio file
    
    is_recording = True
    recording_thread = threading.Thread(target=_record_loop)
    recording_thread.start()

    while is_recording:
        user_input = input("Press 'q' to stop recording: ")
        if user_input.lower() == 'q':
            is_recording = False
    
    # Wait for the recording thread to finish (including auto-transcription)
    recording_thread.join()


def transcribe(audio_path):
    # use TranscribeEngine
    engine = TranscribeEngine()
    result = engine.transcribe(audio_path)
    print("\nProcessing... please wait.")
    _save_transcription(audio_path, result, engine)

def _save_transcription(audio_path, text, engine):
    try:
        output_name = os.path.splitext(audio_path)[0] + ".txt"
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n\nTranscription saved to: {output_name}")

        # create custom markdown file withh note text and name based on the first 5 words of the text  and current date time timestamp 
        note_name = engine.create_note(text)
        print(f"\n\nNote saved to: {note_name}")
    except Exception as e:
        print(f"\n\nError saving transcription: {e}")

