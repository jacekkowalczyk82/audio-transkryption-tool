import argparse
from engine import TranscribeEngine

def run_cli():
    parser = argparse.ArgumentParser(description="TranscribeToolbox - CLI & Batch")
    parser.add_argument("--file", help="Ścieżka do pojedynczego pliku audio")
    parser.add_argument("--dir", help="Ścieżka do folderu (tryb Batch)")
    
    args = parser.parse_args()
    engine = TranscribeEngine()

    if args.file:
        result = engine.transcribe(args.file)
        print(f"\nWynik transkrypcji:\n{result}")
    elif args.dir:
        print(f"Rozpoczynam przetwarzanie folderu: {args.dir}")
        processed = engine.batch_process(args.dir)
        print(f"Zakończono! Przetworzono plików: {len(processed)}")
    else:
        parser.print_help()
        