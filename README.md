# audio-transkryption-tool
Audio transkryption to text tool 

## Development env 

``` 
conda create -n "dev-audio-transkryption-tool" python=3.12
conda activate "dev-audio-transkryption-tool"
pip install -r requirements.txt

```


## Running gui
```
python main.py
```

## Running cli
```
python main.py --cli  --file path/to/file.mp3
python main.py --cli  --dir path/to/folder


```

## Building app
```
./build_executable.sh
```
