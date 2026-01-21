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
python main.py --cli  --file path/to/file.mp3
python main.py --cli  --dir path/to/folder

# to run with gui 
python main.py

```

## Building Executable

To build a standalone executable with the bundled AI model:

```bash
./build_executable.sh
```

## Running in LXC

To run this application inside an LXC container with GUI and Microphone support, please refer to [LXC Deployment Guide](lxc_deployment.md).
