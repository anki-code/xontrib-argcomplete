#!/usr/bin/env xonsh
# PYTHON_ARGCOMPLETE_OK
import argparse, argcomplete
from argcomplete.completers import ChoicesCompleter

parser = argparse.ArgumentParser()
parser.add_argument("--proto").completer=ChoicesCompleter(('http', 'https', 'ssh', 'rsync', 'wss'))
argcomplete.autocomplete(parser)
args = parser.parse_args()
print(args.proto)
