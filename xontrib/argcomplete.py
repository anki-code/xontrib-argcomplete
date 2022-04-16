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
    RichCompletion,
)
from xonsh.parsers.completion_context import CommandContext

# without this, all names will be imported in the context
__all__ = ()

def _get_executor(arg):
    m = re.match("^(python[0-9.]*|xonsh)$", arg)
    return m.group(1) if m else None


def _get_filepath(arg):
    return arg.strip("'").rstrip("\n")


# Run something, muting output or redirecting it to the debug stream
# depending on the value of _ARC_DEBUG.
def _python_argcomplete_run():
    # if [[ -z "${ARGCOMPLETE_USE_TEMPFILES-}" ]]; then
    #     __python_argcomplete_run_inner "$@"
    #     return
    # fi
    # local tmpfile="$(mktemp)"
    # _ARGCOMPLETE_STDOUT_FILENAME="$tmpfile" __python_argcomplete_run_inner "$@"
    # local code=$?
    # cat "$tmpfile"
    # rm "$tmpfile"
    # return $code
    sp.check_output(args=[])


# Scan the beginning of an executable file ($1) for a regexp ($2). By default,
# scan for the magic string indicating that the executable supports the
# argcomplete completion protocol. By default, scan the first kilobyte;
# if $3 is set to -n, scan until the first line break up to a kilobyte.
def _python_argcomplete_scan_head(file: Path) -> bool:
    with file.open("rb") as reader:
        txt = reader.read(1024)
        # todo: implement reading until line-breakup
    return b"PYTHON_ARGCOMPLETE_OK" in txt


def _complete_script_file():
    """"""

    # if [[ "$executable" == python* ]] || [[ "$executable" == pypy* ]]; then
    #     if [[ "${COMP_WORDS[1]}" == -m ]]; then
    #         if __python_argcomplete_run "$executable" -m argcomplete._check_module "${COMP_WORDS[2]}"; then
    #             ARGCOMPLETE=3
    #         else
    #             return
    #         fi
    #     elif [[ -f "${COMP_WORDS[1]}" ]] && __python_argcomplete_scan_head_noerr "${COMP_WORDS[1]}"; then
    #         local ARGCOMPLETE=2


def _complete_executable():
    """
    Handle two cases, where
        1. the executable file is actually a Python script (``$ pytest`` ...)
        2. the script file with a shebang (``$ ./script.py`` ...)
    """

    # elif type -P "$executable" >/dev/null 2>&1; then
    #     local SCRIPT_NAME=$(type -P "$executable")
    #     if (type -t pyenv && [[ "$SCRIPT_NAME" = $(pyenv root)/shims/* ]]) >/dev/null 2>&1; then
    #         local SCRIPT_NAME=$(pyenv which "$executable")
    #     fi
    #     if __python_argcomplete_scan_head_noerr "$SCRIPT_NAME"; then
    #         local ARGCOMPLETE=1
    #     elif __python_argcomplete_scan_head_noerr "$SCRIPT_NAME" '^#!(.*)$' -n && [[ "${BASH_REMATCH[1]}" =~ ^.*(python|pypy)[0-9\.]*$ ]]; then
    #         local interpreter="$BASH_REMATCH"
    #         if (__python_argcomplete_scan_head_noerr "$SCRIPT_NAME" "(PBR Generated)|(EASY-INSTALL-(SCRIPT|ENTRY-SCRIPT|DEV-SCRIPT))" \
    #             && "$interpreter" "$(type -P python-argcomplete-check-easy-install-script)" "$SCRIPT_NAME") >/dev/null 2>&1; then
    #             local ARGCOMPLETE=1
    #         elif __python_argcomplete_run "$interpreter" -m argcomplete._check_console_script "$SCRIPT_NAME"; then
    #             local ARGCOMPLETE=1
    #         fi
    #     fi
    # fi


def create_rich_completion(line: str):
    line = line.strip()
    if "\t" in line:
        cmd, desc = map(str.strip, line.split("\t", maxsplit=1))
    else:
        cmd, desc = line, ""
    return RichCompletion(
        str(cmd),
        description=str(desc),
        append_space=True,
    )


def _run_binary(exe: str, line: str, begidx: "int|None" = None) -> "None|str":
    args = [exe]
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
            [args[0]],
            stderr=sp.DEVNULL,
            stdout=sp.DEVNULL,
            env=env,
        )
        out = Path(outfile.name).read_bytes().decode()
    finally:
        os.unlink(outfile.name)

    return out


def _get_completions(exe: str, line: str, begidx: "int|None" = None):
    output = _run_binary(exe, line, begidx)
    if output:
        for line in output.strip().splitlines(keepends=False):
            yield create_rich_completion(line)


@contextual_command_completer
def python_argcomplete(ctx: CommandContext):
    """Argcomplete-https://kislyuk.github.io/argcomplete/ support"""
    if not ctx.args:
        return

    line = ctx.text_before_cursor
    executable = ctx.args[0].value
    defined_exes = XSH.env.get("XONSH_ARGCOMPLETE_COMMANDS") or set()
    if executable not in defined_exes:
        return
    return _get_completions(executable, line, ctx.begidx), False


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
#  1. global completion ( disabled by default. can be controlled by env variable)
#  2. ./script.py or python script.py completion. it should be called with subprocess with tmp-file path completion
