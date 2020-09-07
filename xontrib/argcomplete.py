#!/usr/bin/env xonsh

import sys, re, subprocess
from pathlib import Path

def _SC(cmds, env):
    """
    Run shell command (workaround for https://github.com/xonsh/xonsh/issues/3746)
    """
    proc = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True)
    [out, err] = proc.communicate()
    return (out, err, proc)

def _xontrib_argcomplete_completer(prefix, line, begidx, endidx, ctx):
    """
    Adding support of kislyuk/argcomplete to xonsh.
    """
    file = None
    m = re.match('^python[0-9.]* ([\']*.+?\\.py[\']*)', line)
    if not m:
        m = re.match('^([\']*.+?\\.py[\']*)', line)

    if m:
        file = m.group(1)
    else:
        return None

    if file[0] == "'" and file[-1] == "'":
        file = file[1:-1]

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
        env = {
            "PATH": ':'.join(sys.path) + ':' + ':'.join(__xonsh__.env['PATH']),
            "_ARGCOMPLETE": str(1),
            "_ARGCOMPLETE_IFS":'\n',
            "COMP_LINE": str(line),
            "COMP_POINT": str(begidx)
        }
        o, e, proc = _SC('python "'+file+'" 8>&1', env=env)

        tokens = set([t for t in o.decode().split('\n') if prefix in t])

        if len(tokens) == 0:
            return (('argcomplete: completions not found',), len(prefix))

        return (tokens, len(prefix))

    return None

__xonsh__.completers['xontrib_argcomplete'] = _xontrib_argcomplete_completer
__xonsh__.completers.move_to_end('xontrib_argcomplete', last=False)
