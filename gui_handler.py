import tkinter as tk
from tkinter import filedialog, messagebox
from engine import TranscribeEngine

class TranscribeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TranscribeToolbox")
        self.engine = TranscribeEngine()

        self.label = tk.Label(root, text="Wybierz plik do transkrypcji:")
        self.label.pack(pady=10)

        self.btn_select = tk.Button(root, text="Wybierz Audio", command=self.select_file)
        self.btn_select.pack(pady=5)

        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Przetwarzanie... proszę czekać.")
            self.root.update()
            
            result = self.engine.transcribe(file_path)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, result)