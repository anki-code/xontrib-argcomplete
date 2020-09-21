#!/usr/bin/env xonsh

import re
from pathlib import Path
from shutil import which

def _get_subproc_output(cmds):
    result = __xonsh__.subproc_captured_object(cmds)
    result.rtn  # workaround https://github.com/xonsh/xonsh/issues/3394
    return result.output

def _xontrib_argcomplete_completer(prefix, line, begidx, endidx, ctx):
    """
    Adding support of argcomplete to xonsh.
    """
    py = None
    file = None
    m = re.match('^(python[0-9.]*|xonsh) ([\']*.+?(\\.py[0-9.]*|\\.xsh)[\']*)', line)
    if m:
        py = m.group(1)
        file = m.group(2)
    else:
        m = re.match('^([\']*.+?(\\.py|\\.xsh)[\']*)', line)
        if m:
            file = m.group(1)
            py = 'xonsh' if file.endswith('.xsh') else 'python'
        else:
            m = re.match('^(.+?)(\\s+|$)', line)
            if m:
                if not m.group(2):
                    return None

                maybe_file = m.group(1)
                if Path(maybe_file).exists():
                    file = str(maybe_file)
                else:
                    which_maybe_file = which(maybe_file)
                    if which_maybe_file and Path(which_maybe_file).exists():
                        file = str(which_maybe_file)
                    else:
                        try:
                            which_maybe_file = _get_subproc_output(['which', maybe_file, '2>', '/dev/null']).strip()
                        except:
                            return None
                        if which_maybe_file and Path(which_maybe_file).exists():
                            file = which_maybe_file

    if not file:
        if __xonsh__.env.get('XONTRIB_ARGCOMPLETE_DEBUG', False):
            return ((prefix, 'xontrib-argcomplete DEBUG: filename not found'), len(prefix))
        return None

    file = file[1:-1] if file[0] == "'" and file[-1] == "'" else file
    if not Path(file).exists():
        if __xonsh__.env.get('XONTRIB_ARGCOMPLETE_DEBUG', False):
            return ((prefix, 'xontrib-argcomplete DEBUG: file does not exists'), len(prefix))
        return None

    if 'text' not in _get_subproc_output(['file', file]):
        if __xonsh__.env.get('XONTRIB_ARGCOMPLETE_DEBUG', False):
            return ((prefix, 'xontrib-argcomplete DEBUG: file type is not text'), len(prefix))
        return None

    found_argcomplete = False
    with open(file) as f:
        for x in range(10):
            fline = next(f)
            if x == 0 and not py:
                m = re.match('.*env (python[0-9.]*|xonsh).*', fline)
                if m:
                    py = m.group(1)
                else:
                    m = re.match('#!(/.*/(python[0-9.]*|xonsh))', fline)
                    if m:
                        py = m.group(1)
                        if not Path(py).exists():
                            if __xonsh__.env.get('XONTRIB_ARGCOMPLETE_DEBUG', False):
                                return ((prefix, 'xontrib-argcomplete DEBUG: the python/xonsh path in the script`s shebang does not exists'), len(prefix))
                            py = None

            if 'PYTHON_ARGCOMPLETE_OK' in fline:
                found_argcomplete = True
                break

    if found_argcomplete and py:
        with __xonsh__.env.swap(_ARGCOMPLETE=str(1), _ARGCOMPLETE_IFS='\n', COMP_LINE=str(line), COMP_POINT=str(begidx)):
            output = _get_subproc_output(['bash', '-c', f"{py} '{file}' 8>&1"])
        tokens = set([t.replace(r'\ ', ' ') for t in output.split('\n') if prefix in t])

        if len(tokens) == 0:
            if __xonsh__.env.get('XONTRIB_ARGCOMPLETE_DEBUG', False):
                return ((prefix, 'xontrib-argcomplete DEBUG: completions not found'), len(prefix))
            return None

        return (tokens, len(prefix))

    return None

__xonsh__.completers['xontrib_argcomplete'] = _xontrib_argcomplete_completer
__xonsh__.completers.move_to_end('xontrib_argcomplete', last=False)
