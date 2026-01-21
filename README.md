# audio-transkryption-tool
Audio transkryption to text tool 

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
