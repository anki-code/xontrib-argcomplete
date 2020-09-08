<p align="center">
Adding support of <a href="https://github.com/kislyuk/argcomplete">kislyuk/argcomplete</a> to <a href="https://xon.sh">xonsh</a>.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and stay tuned by watching releases.
</p>

## Install
```shell script
xpip install -U xontrib-argcomplete
echo 'xontrib load argcomplete' >> ~/.xonshrc
# Reload xonsh
```

## Usage
For example create `proto.py`:
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

