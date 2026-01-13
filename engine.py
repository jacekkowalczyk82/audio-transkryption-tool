import os
from faster_whisper import WhisperModel

class TranscribeEngine:
    def __init__(self, model_size="base"):
        # Ustawienie device="cpu" dla uniwersalności (zadziała na każdym PC)
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, file_path):
        if not os.path.exists(file_path):
            return "Błąd: Plik nie istnieje."
        
        segments, _ = self.model.transcribe(file_path, beam_size=5, language="pl")
        text = " ".join([segment.text for segment in segments])
        return text.strip()

    def batch_process(self, folder_path):
        supported_ext = ('.mp3', '.wav', '.m4a', '.flac')
        results = []
        
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_ext)]
        for file in files:
            full_path = os.path.join(folder_path, file)
            print(f"Przetwarzanie: {file}...")
            text = self.transcribe(full_path)
            
            # Zapisz wynik do pliku .txt o tej samej nazwie
            output_name = os.path.splitext(full_path)[0] + ".txt"
            with open(output_name, "w", encoding="utf-8") as f:
                f.write(text)
            results.append((file, output_name))
        
        return results