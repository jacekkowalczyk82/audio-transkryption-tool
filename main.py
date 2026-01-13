import sys
import customtkinter as ctk
from cli_handler import run_cli
from gui_handler import TranscribeGUI

# Set customtkinter theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def main():
    # If arguments are provided in console -> run CLI
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        sys.argv.pop(1)
        run_cli()
    else:
        # Otherwise -> run GUI
        root = ctk.CTk()
        app = TranscribeGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
