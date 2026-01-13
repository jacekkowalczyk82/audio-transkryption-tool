import argparse
from engine import TranscribeEngine

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
        