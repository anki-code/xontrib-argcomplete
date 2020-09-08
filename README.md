<p align="center">
Adding support of <a href="https://github.com/kislyuk/argcomplete">kislyuk/argcomplete</a> to <a href="https://xon.sh">xonsh</a>.
</p>

<p align="center">  
If you like the idea of xontrib-argcomplete click ⭐ on the repo and stay tuned by watching releases.
</p>

## Install
```shell script
xpip install -U xontrib-argcomplete
echo 'xontrib load argcomplete' >> ~/.xonshrc
# Reload xonsh
```

## Usage
Current version of completion is working only for commands that starts with:
 * `python <path/to/python_script.py> ...`
 * `<path/to/python_script.py> ...`

For example create `proto.py` with the content:
```python
#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse, argcomplete
from argcomplete.completers import ChoicesCompleter

parser = argparse.ArgumentParser()
parser.add_argument("--proto").completer=ChoicesCompleter(('http', 'https', 'ssh', 'rsync', 'wss'))
argcomplete.autocomplete(parser)
args = parser.parse_args()
print('ok')
```
Then try completion:
```bash
python proto.py <Tab>
# Suggestions: --help --proto -h

chmod +x proto.py
./proto.py --proto tt<Tab>
# Suggestions: http https
```

## Known issues
This is the alpha version of the xontrib-argcomplete and the proof of concept. It was tested on Ubuntu+Conda+Xonsh and on Mac.

### No completions or "Completions not found" message

To get completions list for your Python script it runs in subprocess shell (`sh` by default) with appropriate argcomplete environment variables. The common reason you can get empty list or "Completions not found" message" is that you have different setting for Python in xonsh and in `sh` shell. 

To test that your `script.py` with `argparse` and `argcomplete` is working properly in `sh` try to run:
```bash
sh -c 'python script.py'
# OR
sh -c 'python script.py --help' # to avoid full running the script
# AND check the Python version and paths
sh -c 'python -V'
sh -c 'python -c "import sys; print(sys.path)"'
```
If you see the errors this is the cause why xontrib returns no completions. The causes may be different: xontrib-argcomplete may not properly set the environment and PR to fix is required or your environment is complex and you should synchronize xonsh and `sh`.
