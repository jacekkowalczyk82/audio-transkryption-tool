import sys
import tkinter as tk
from cli_handler import run_cli
from gui_handler import TranscribeGUI

def main():
    # If arguments are provided in console -> run CLI
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        sys.argv.pop(1)
        run_cli()
    else:
        # Otherwise -> run GUI
        root = tk.Tk()
        app = TranscribeGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
