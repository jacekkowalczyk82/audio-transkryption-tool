import tkinter as tk
from tkinter import filedialog, messagebox
from engine import TranscribeEngine


import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import os

FS = 44100  # Probing frequency

class TranscribeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TranscribeToolbox")
        self.engine = TranscribeEngine()

        self.label = tk.Label(root, text="Select file to transcribe:")
        self.label.pack(pady=10)

        self.btn_select = tk.Button(root, text="Select Audio", command=self.select_file)
        self.btn_select.pack(pady=5)

        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(pady=10)

        self.btn_record = tk.Button(root, text="Record Audio", command=self.record_audio)
        self.btn_record.pack(pady=5)

        self.btn_transcribe = tk.Button(root, text="Transcribe", command=self.transcribe)
        self.btn_transcribe.pack(pady=5)

        self.btn_exit = tk.Button(root, text="Exit", command=self.root.quit)
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
    
    def record_audio(self, duration=10):
        print(f"Recording for {duration} seconds...")
        recording = sd.rec(int(duration * FS), samplerate=FS, channels=1)
        sd.wait()  # wait for recording to finish
        self.last_recorded_audio = self.get_new_audio_file_name()
        write(self.last_recorded_audio, FS, recording)
        
        print("Recording finished.")

    
    def transcribe(self):
        # use TranscribeEngine
        result = self.engine.transcribe(self.last_recorded_audio)
        self.text_area.insert(tk.END, "Processing... please wait.")
        self.root.update()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.root.update()


        