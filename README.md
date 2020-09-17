<p align="center">
Adding support of <a href="https://github.com/kislyuk/argcomplete">argcomplete</a> to <a href="https://xon.sh">xonsh</a>.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and stay tuned by watching releases.
</p>

## Install
```shell script
xpip install xontrib-argcomplete
echo 'xontrib load argcomplete' >> ~/.xonshrc
# Reload xonsh
```

## Usage

The [argcomplete](https://kislyuk.github.io/argcomplete/#synopsis) xonsh completer will be activated with this cases:
```bash
./script.py        <Tab>
./path/script.py   <Tab>
python script.py   <Tab>
./script.xsh       <Tab>
./path/script.xsh  <Tab>
xonsh script.xsh   <Tab>
```
The `PYTHON_ARGCOMPLETE_OK` marker should be found in the first 10 lines of the file.

## Example
```bash
xpip install xontrib-argcomplete
xontrib load argcomplete

cd /tmp && git clone https://github.com/anki-code/xontrib-argcomplete
cd xontrib-argcomplete/tests

python proto.py <Tab>
# Suggestions: --help --proto -h

./proto.py --proto tt<Tab>
# Suggestions: http https

./proto.xsh --proto tt<Tab>
# Suggestions: http https
```

## Development
* [Documentation for environment variables that used by argcomplete](https://github.com/kislyuk/argcomplete/issues/319)
