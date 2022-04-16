#!/usr/bin/env xonsh
import os
import re
import subprocess as sp
import tempfile
from pathlib import Path

from xonsh.built_ins import XonshSession, XSH
from xonsh.completers import completer
from xonsh.completers.tools import (
    contextual_command_completer,
    completion_from_cmd_output,
)
from xonsh.parsers.completion_context import CommandContext

# without this, all names will be imported in the context
__all__ = ()


def _get_executor(arg):
    m = re.match("^(python[0-9.]*|xonsh|pypy[0-9.]*)$", arg)
    return m.group(1) if m else None


def _get_filepath(arg):
    return arg.strip("'").rstrip("\n")


# Scan the beginning of an executable file ($1) for a regexp ($2). By default,
# scan for the magic string indicating that the executable supports the
# argcomplete completion protocol. By default, scan the first kilobyte;
# if $3 is set to -n, scan until the first line break up to a kilobyte.
def _python_argcomplete_scan_head(file: str) -> bool:
    with open(file, "rb") as reader:
        txt = reader.read(1024)
        # todo: implement reading until line-breakup
    return b"PYTHON_ARGCOMPLETE_OK" in txt


def arg_complete_proc(line: str, *args: str, begidx: "int|None" = None) -> "None|str":
    comp_point = str(len(line)) if begidx is None else str(begidx)

    outfile = tempfile.NamedTemporaryFile(delete=False)
    outfile.close()
    env = dict(
        _ARGCOMPLETE="1",
        _ARGCOMPLETE_IFS="\n",
        _ARGCOMPLETE_DFS="\t",
        _ARGCOMPLETE_SUPPRESS_SPACE="1",
        _ARGCOMPLETE_SHELL="fish",
        _ARGCOMPLETE_STDOUT_FILENAME=outfile.name,  # or fd=8 is used
        COMP_LINE=line,
        COMP_POINT=comp_point,
    )
    env.update(XSH.env.detype())

    try:
        # pytest 8>&1 9>&2 1>/dev/null 2>&1
        # fd 9 is used for debug output
        sp.run(
            args,
            stderr=sp.DEVNULL,
            stdout=sp.DEVNULL,
            env=env,
        )
        out = Path(outfile.name).read_bytes().decode()
    finally:
        os.unlink(outfile.name)

    return out


def _get_completions(line: str, *args: str, begidx: "int|None" = None):
    output = arg_complete_proc(line, *args, begidx=begidx)
    if output:
        for line in output.strip().splitlines(keepends=False):
            yield completion_from_cmd_output(line, append_space=True)


@contextual_command_completer
def python_argcomplete(ctx: CommandContext):
    """Argcomplete-https://kislyuk.github.io/argcomplete/ support"""
    if not ctx.args:
        return

    cmd = ctx.args[0].value
    line = ctx.text_before_cursor

    args = None
    if ctx.arg_index > 1 and _get_executor(cmd):
        # Handle the case where the script is executed with Python/xonsh binary
        file_path = ctx.args[1].value
        if _python_argcomplete_scan_head(file_path):
            args = [cmd, file_path]

    defined_exes = XSH.env.get("XONSH_ARGCOMPLETE_COMMANDS") or set()
    if cmd in defined_exes:
        # Handle the case where the first argument is an executable
        args = [cmd]

    if args:
        # todo: return dict once supported
        result = _get_completions(line, *args, begidx=ctx.begidx)
        return result, False  # not filtered


def xonsh_entrypoint(xsh: XonshSession, **_):
    # todo: xsh.completers.add_one_completer
    completer.add_one_completer("argcomplete", python_argcomplete, "<import")
    known_clis = {
        "pytest",
    }
    xsh.env.register(
        name="XONSH_ARGCOMPLETE_COMMANDS",
        default=known_clis,
        doc="register a command that uses argcomplete",
        doc_default=f"Some of the popular commands that use argcomplete is added by default. {known_clis}",
    )


xonsh_entrypoint(XSH)


# todo:
#  1. global completion ( disabled by default.
#       can be controlled by env variable as it will make other completions slow as well)
#       - https://kislyuk.github.io/argcomplete/#global-completion
#  2. ./script.py or python script.py completion. it should be called with subprocess with tmp-file path completion
#       ii. the script file with a shebang (``$ ./script.py`` ...)
#
