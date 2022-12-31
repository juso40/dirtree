# dirtree
Generate good-looking ascii trees of directories and files.

## Installation
Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):
```bash
pip install -U ascii-dirtree
```

## Usage
```yaml
usage: dirtree [-h] [-p [PATH]] [-f] [-c] [-i [IGNORE ...]] [-d DEPTH]

optional arguments:
  -h, --help            show this help message and exit
  -p [PATH], --path [PATH]
                        Path to start from
  -f, --files           print files
  -c, --clip            copy to clipboard
  -i [IGNORE ...], --ignore [IGNORE ...]
                        ignore files matching glob
  -d DEPTH, --depth DEPTH
                        depth to traverse, negative for infinite
```

Example:  
![](https://user-images.githubusercontent.com/39841117/209985305-bcdf7945-debc-439e-bf69-a0f935d08d03.gif)
