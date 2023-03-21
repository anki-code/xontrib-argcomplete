<p align="center">
<a href="https://github.com/kislyuk/argcomplete">Argcomplete</a> support for python and xonsh scripts in <a href="https://xon.sh">xonsh</a> shell.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/anki-code/xontrib-argcomplete" target="_blank">tweet</a>.
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

First of all you need to [add the argcomplete support to your script](https://kislyuk.github.io/argcomplete/#synopsis):
* The `PYTHON_ARGCOMPLETE_OK` marker should be found in the first 10 lines of the file ([example](https://github.com/anki-code/xontrib-argcomplete/blob/37e24660351780501eed64a2a77cb2a3309c109c/tests/proto.py#L2)).
* Additional `.completer` was set for `add_argument` ([example](https://github.com/anki-code/xontrib-argcomplete/blob/37e24660351780501eed64a2a77cb2a3309c109c/tests/proto.py#L7)).
* `argcomplete.autocomplete(parser)` added before `parser.parse_args()` ([example](https://github.com/anki-code/xontrib-argcomplete/blob/37e24660351780501eed64a2a77cb2a3309c109c/tests/proto.py#L8)).

Example for [`proto.py`](https://github.com/anki-code/xontrib-argcomplete/blob/master/tests/proto.py):
```xsh
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

The argcomplete xonsh completer will be activated with this cases:
```xsh
python script.py <Tab>
./script.py <Tab>
./path/script.py <Tab>

xonsh script.xsh <Tab>
./script.xsh <Tab>
./path/script.xsh <Tab>

# scripts without extension should have "env python" or "env xonsh" or path to python/xonsh in the shebang
./script <Tab>
script <Tab>    # script should be found in $PATH
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
