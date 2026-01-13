#!/bin/bash

# Python interpreter from the Conda environment
PYTHON_PATH="/home/jacek/miniconda3/envs/dev-audio-transkryption-tool/bin/python"
# Path to the specific Conda environment PyInstaller
PYINSTALLER_PATH="/home/jacek/miniconda3/envs/dev-audio-transkryption-tool/bin/pyinstaller"

# Dynamically get the Whisper model path
echo "Resolving Whisper model path..."
MODEL_PATH=$($PYTHON_PATH get_model_path.py)

if [ -z "$MODEL_PATH" ]; then
    echo "Error: Could not find model path."
    exit 1
fi

echo "Building executable with PyInstaller..."
echo "Model Path: $MODEL_PATH"

VERSION_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
$PYINSTALLER_PATH --noconfirm --onefile --windowed --name "AudioTranscriber.$VERSION_TIMESTAMP.bin" \
    --add-data "$MODEL_PATH:whisper_model" \
    --hidden-import="customtkinter" \
    --hidden-import="faster_whisper" \
    --collect-all="customtkinter" \
    --collect-all="faster_whisper" \
    main.py

echo "Build complete. Executable is in dist/AudioTranscriber.$VERSION_TIMESTAMP.bin"

