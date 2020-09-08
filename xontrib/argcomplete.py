#!/usr/bin/env xonsh

import re
from pathlib import Path

def _xontrib_argcomplete_completer(prefix, line, begidx, endidx, ctx):
    """
    Adding support of kislyuk/argcomplete to xonsh.
    """
    file = None
    m = re.match('^(python[0-9.]*) ([\']*.+?\\.py[\']*)', line)
    if m:
        py = m.group(1)
        file = m.group(2)
    else:
        m = re.match('^([\']*.+?\\.py[\']*)', line)
        if m:
            py = 'python'  # TODO: get from shebang
            file = m.group(1)

    if not file:
        return None

    file = file[1:-1] if file[0] == "'" and file[-1] == "'" else file
    filep = Path(file)
    if not filep.exists():
        return ((prefix, 'argcomplete: file does not exists'), len(prefix))

    found_argcomplete = False
    with open(filep) as f:
        for x in range(100):
            if 'PYTHON_ARGCOMPLETE_OK' in next(f):
                found_argcomplete = True
                break

    if found_argcomplete:
        with __xonsh__.env.swap(_ARGCOMPLETE=str(1), _ARGCOMPLETE_IFS='\n', COMP_LINE=str(line), COMP_POINT=str(begidx)):
            result = __xonsh__.subproc_captured_object(['bash', '-c', f"{py} '{file}' 8>&1"])
            result.rtn # workaround https://github.com/xonsh/xonsh/issues/3394
        tokens = set([t.replace(r'\ ', ' ') for t in result.output.split('\n') if prefix in t])

        if len(tokens) == 0:
            return ((prefix, 'argcomplete: completions not found'), len(prefix))

        return (tokens, len(prefix))

    return None

__xonsh__.completers['xontrib_argcomplete'] = _xontrib_argcomplete_completer
__xonsh__.completers.move_to_end('xontrib_argcomplete', last=False)
