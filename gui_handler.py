import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from engine import TranscribeEngine


import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import os

import threading
import numpy as np

FS = 44100  # Probing frequency

class TranscribeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TranscribeToolbox")
        self.engine = TranscribeEngine()

        self.label = ctk.CTkLabel(root, text="Select file to transcribe:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.btn_select = ctk.CTkButton(root, text="Select Audio", command=self.select_file)
        self.btn_select.pack(pady=5)

        self.text_area = ctk.CTkTextbox(root, height=200, width=500)
        self.text_area.pack(pady=10)

        # Initialize recording state
        self.is_recording = False
        self.recording_thread = None

        self.btn_record = ctk.CTkButton(root, text="Start Recording", command=self.toggle_recording)
        self.btn_record.pack(pady=5)

        self.btn_transcribe = ctk.CTkButton(root, text="Transcribe", command=self.transcribe)
        self.btn_transcribe.pack(pady=5)

        self.btn_exit = ctk.CTkButton(root, text="Exit", command=self.root.quit, fg_color="red", hover_color="darkred")
        self.btn_exit.pack(pady=5)

    def get_new_audio_file_name(self):
        # use date time to create unique file name
        import datetime
        now = datetime.datetime.now()
        return f"recorded_audio_{now.strftime('%Y%m%d_%H%M%S')}.wav"

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Processing... please wait.")
            self.root.update()
            
            result = self.engine.transcribe(file_path)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, result)
            self._save_transcription(file_path, result)
    
    def toggle_recording(self):
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.btn_record.configure(text="Stop Recording", fg_color="red")
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Recording... Press 'Stop Recording' to finish.")
            self.recording_thread = threading.Thread(target=self._record_loop)
            self.recording_thread.start()
        else:
            # Stop recording
            self.is_recording = False
            self.btn_record.configure(text="Start Recording", fg_color=["#3B8ED0", "#1F6AA5"]) # Reset to default blue
            # Thread will finish automatically when flag is False

    def _record_loop(self):
        audio_chunks = []
        try:
            with sd.InputStream(samplerate=FS, channels=1) as stream:
                while self.is_recording:
                    # Read chunks of audio (e.g., 0.1 seconds)
                    data, overflowed = stream.read(int(FS * 0.1))
                    audio_chunks.append(data)
            
            # Concatenate all chunks
            if audio_chunks:
                recording = np.concatenate(audio_chunks, axis=0)
                self.last_recorded_audio = self.get_new_audio_file_name()
                write(self.last_recorded_audio, FS, recording)
                
                # Update UI from main thread (scheduled)
                self.root.after(0, lambda: self.text_area.insert(tk.END, f"\nRecording saved: {self.last_recorded_audio}"))
        except Exception as e:
            self.root.after(0, lambda: self.text_area.insert(tk.END, f"\nError recording: {e}"))
            self.is_recording = False
            self.root.after(0, lambda: self.btn_record.configure(text="Start Recording", fg_color=["#3B8ED0", "#1F6AA5"]))

    
    def transcribe(self):
        # use TranscribeEngine
        result = self.engine.transcribe(self.last_recorded_audio)
        self.text_area.insert(tk.END, "Processing... please wait.")
        self.root.update()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.root.update()
        self._save_transcription(self.last_recorded_audio, result)

    def _save_transcription(self, audio_path, text):
        try:
            output_name = os.path.splitext(audio_path)[0] + ".txt"
            with open(output_name, "w", encoding="utf-8") as f:
                f.write(text)
            self.text_area.insert(tk.END, f"\n\nTranscription saved to: {output_name}")
        except Exception as e:
            self.text_area.insert(tk.END, f"\n\nError saving transcription: {e}")


        