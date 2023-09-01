# Online Map Downloader

## Requirements

Python>=3.8

AutoCAD>=2014

It's recommended that you use Conda to create an environment to run code from this repository.

## Usage

### command line

```console
git clone https://github.com/shenlc19/MapCrawler.git
cd MapCrawler
pip install -r requirements.txt
python main.py (your url here)
```


In the last line of command (namely, "python main.py ..."), your url must be added as an argument. For example:
```console
python main.py https://map.baidu.com/@12950435.038356394,4839483.068886998,21z
```

### gui.py

In command line:
```console
python gui.py
```

In GUI:

Paste your url in the entry bar and press the "Download" button.

Then a CAD file in .dxf format will be available in the current directory.