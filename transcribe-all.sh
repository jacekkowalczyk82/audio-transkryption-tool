#!/bin/bash

LANGUAGE=$1
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="pl"
    
fi

# Initialize conda for this shell session
# This ensures 'conda activate' works even if the script is run non-interactively
eval "$(conda shell.bash hook)"

# Activate the specific environment
conda activate dev-audio-transkryption-tool

# Run the application, passing all arguments ("$@") to it
python main.py --cli  --dir /home/jacek/dyktafon/ --lang $LANGUAGE

