# audio-transkryption-tool
Audio transkryption to text tool.the application allows to record audio note which will be automatically transcribed to text. Instead of typing on the keyboard you can talk to your computer. 

## Development env 

``` 
conda create -n "dev-audio-transkryption-tool" python=3.12
conda activate "dev-audio-transkryption-tool"
pip install -r requirements.txt

```
## Usage

```bash
python main.py --cli  --file path/to/file.mp3 --lang pl
python main.py --cli  --dir path/to/folder --lang en

# to run with gui 
python main.py
```

The `--lang` option accepts `pl` (Polish) or `en` (English) and defaults to
Polish. In the GUI, choose the transcription language from the menu before
selecting a file or recording audio. To record a note from the CLI, use
`python main.py --create-note --lang en` (or `pl`).

## dyktafon

/home/jacek/git/audio-transkryption-tool/transcribe-all.sh

## Building Executable

To build a standalone executable with the bundled AI model:

```bash
./build_executable.sh
```

## Running in LXC

To run this application inside an LXC container with GUI and Microphone support, please refer to [LXC Deployment Guide](lxc_deployment.md).
