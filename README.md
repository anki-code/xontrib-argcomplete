<p align="center">
<a href="https://github.com/kislyuk/argcomplete">Argcomplete</a> support for python and xonsh scripts in <a href="https://xon.sh">xonsh</a> shell.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and stay tuned by watching releases.
</p>

<p align="center">  
<img src="https://raw.githubusercontent.com/anki-code/xontrib-argcomplete/master/static/xontrib-argcomplete-demo.png" alt="[Demo]"><br />
<sup><i>Screenshot made with <a href="https://github.com/anki-code/xontrib-prompt-bar">xontrib-prompt-bar</a> and <a href="https://konsole.kde.org/">Konsole</a>.</i></sup>
</p>

## Install
```shell script
xpip install xontrib-argcomplete
echo 'xontrib load argcomplete' >> ~/.xonshrc
# Reload xonsh
```

## Usage

Before usage you must [add the argcomplete support to your script](https://kislyuk.github.io/argcomplete/#synopsis). The `PYTHON_ARGCOMPLETE_OK` marker should be found in the first 10 lines of the file.

The argcomplete xonsh completer will be activated with this cases:
```bash
python script.py
./script.py
./path/script.py

xonsh script.xsh
./script.xsh
./path/script.xsh

# scripts without extension should have "env python" or "env xonsh" or path to python/xonsh in the shebang
./script
script    # script should be found in $PATH
```

## Example
```bash
xpip install xontrib-argcomplete
xontrib load argcomplete

cd /tmp && git clone https://github.com/anki-code/xontrib-argcomplete
cd xontrib-argcomplete/tests

python proto.py <Tab>  # Suggestions: --help --proto -h
./proto.py --proto tt<Tab>  # Suggestions: http https
./proto.xsh --proto tt<Tab>  # Suggestions: http https
./proto --proto tt<Tab>  # Suggestions: http https

$PATH.append($PWD)
proto --proto tt<Tab>  # Suggestions: http https
```

## Known issues

Windows is not supported. PRs are welcome!

## Development
* To switch on the debug mode run `$XONTRIB_ARGCOMPLETE_DEBUG = True`.
* [Argcomplete environment variables](https://github.com/kislyuk/argcomplete/issues/319#issuecomment-693295017)
* [Argcomplete documentation](https://kislyuk.github.io/argcomplete/)

## Links 
* This package is the part of [ergopack](https://github.com/anki-code/xontrib-ergopack) - the pack of ergonomic xontribs.
* This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
