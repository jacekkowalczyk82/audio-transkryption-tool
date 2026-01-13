import sys
import tkinter as tk
from cli_handler import run_cli
from gui_handler import TranscribeGUI

def main():
    # Jeśli podano argumenty w konsoli -> uruchom CLI
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        # W przeciwnym razie -> uruchom GUI
        root = tk.Tk()
        app = TranscribeGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
