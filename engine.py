import os
import sys
from faster_whisper import WhisperModel

class TranscribeEngine:
    def __init__(self, model_size="medium"):
        # model_size can be "base", "small", "medium", "large-v2", "large-v3"
        
        # Check if running as PyInstaller OneFile
        if getattr(sys, 'frozen', False):
            # If frozen, looking for model in the temp bundle directory
            model_path = os.path.join(sys._MEIPASS, "whisper_model")
            print(f"Loading model from bundled path: {model_path}")
            self.model = WhisperModel(model_path, device="cpu", compute_type="int8")
        else:
            # Normal run, load from cache/download
            # Set device="cpu" for universality (will work on any PC)
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, file_path):
        if not os.path.exists(file_path):
            return "Error: File does not exist."
        
        segments, _ = self.model.transcribe(file_path, beam_size=5, language="pl")
        text = " ".join([segment.text for segment in segments])
        return text.strip()

    def batch_process(self, folder_path):
        supported_ext = ('.mp3', '.wav', '.m4a', '.flac')
        results = []
        
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_ext)]
        for file in files:
            full_path = os.path.join(folder_path, file)
            print(f"Processing: {file}...")
            text = self.transcribe(full_path)
            
            # Save result to .txt file with the same name
            output_name = os.path.splitext(full_path)[0] + ".txt"
            with open(output_name, "w", encoding="utf-8") as f:
                f.write(text)
            results.append((file, output_name))
        
        return results
    
    def create_note(self, text):
        import datetime
        now = datetime.datetime.now()
        note_name = f"note_{now.strftime('%Y%m%d_%H%M%S')}_{self._create_note_name_prefix_short(text)}.md"
        with open(note_name, "w", encoding="utf-8") as f:
            f.write(f"# Note {now.strftime('%Y%m%d_%H%M%S')}\n\n")
            f.write(f"Short title: {self._create_note_name_prefix_short(text)}\n\n")
            f.write(f"*Transcription full text:*\n\n")
            f.write(text)
            f.write(f"\n\n*End of transcription*")
            f.write(f"\n\n*Note created by Audio Transcriber*")
            f.write(f"\n\n*Note created at: {now.strftime('%Y%m%d_%H%M%S')}*")
            f.write(f"\n\n*Note created in folder: {os.getcwd()}*")

        return note_name

    def _create_note_name_prefix_short(self, text):
        # select 5 first words of the text and remove special characters
        # return "_".join(text.split()[:5]).replace("-", "_").replace(" ", "_").replace(".", "_").replace(",", "_").replace("!", "_").replace("?", "_").replace("'", "_").replace("\"", "_").replace("/", "_").replace("\\", "_").replace("|", "_").replace("*", "_").replace('#', "_").replace("$", "_").replace("%", "_").replace("^", "_").replace("&", "_").replace("(", "_").replace(")", "_").replace("+", "_").replace("=", "_").replace("[", "_").replace("]", "_").replace("{", "_").replace("}", "_").replace("<", "_").replace(">", "_").replace(";", "_").replace(":", "_").replace("\n", "_").replace("\t", "_").replace("\r", "_").replace("\b", "_").replace("\f", "_").replace("\v", "_").replace("\a", "_").replace("\e", "_").replace("\c", "_").replace("\d", "_").replace("\o", "_").replace("\x", "_").replace("\u", "_").replace("\U", "_").replace("\N", "_").replace("\\", "_")
        return "_".join(text.split()[:5]).replace("-", "_").replace(" ", "_").replace(".", "_").replace(",", "_").replace("!", "_").replace("?", "_").replace("'", "_").replace("\"", "_").replace("/", "_").replace("\\", "_").replace("|", "_").replace("*", "_").replace('#', "_").replace("$", "_").replace("%", "_").replace("^", "_").replace("&", "_").replace("(", "_").replace(")", "_").replace("+", "_").replace("=", "_").replace("[", "_").replace("]", "_").replace("{", "_").replace("}", "_").replace("<", "_").replace(">", "_").replace(";", "_").replace(":", "_").replace("\n", "_").replace("\t", "_").replace("\r", "_").replace("\\", "_")
