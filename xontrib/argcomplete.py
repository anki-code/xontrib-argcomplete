#!/usr/bin/env xonsh

import sys, re, subprocess
from pathlib import Path

def _xontrib_argcomplete_completer(prefix, line, begidx, endidx, ctx):
    """
    Adding support of kislyuk/argcomplete to xonsh.
    """
    file = None
    m = re.match('^python[0-9.]* ([\']*.+?\\.py[\']*)', line)
    m = re.match('^([\']*.+?\\.py[\']*)', line) if not m else m

    if m:
        file = m.group(1)
    else:
        return None

    file = file[1:-1] if file[0] == "'" and file[-1] == "'" else file
    filep = Path(file)
    if not filep.exists():
        return (('argcomplete: file does not exists',), len(prefix))

    found_argcomplete = False
    with open(filep) as f:
        for x in range(100):
            if 'PYTHON_ARGCOMPLETE_OK' in next(f):
                found_argcomplete = True
                break

    if found_argcomplete:
        with __xonsh__.env.swap(_ARGCOMPLETE=str(1), _ARGCOMPLETE_IFS='\n', COMP_LINE=str(line), COMP_POINT=str(begidx)):
            result = __xonsh__.subproc_captured_inject(['bash', '-c', f"python '{file}' 8>&1"])

        tokens = set([t for t in result if prefix in t])

        if len(tokens) == 0:
            return (('argcomplete: completions not found',), len(prefix))

        return (tokens, len(prefix))

    return None

__xonsh__.completers['xontrib_argcomplete'] = _xontrib_argcomplete_completer
__xonsh__.completers.move_to_end('xontrib_argcomplete', last=False)
