#!/usr/bin/env xonsh

import re
from pathlib import Path
from shutil import which

def _get_subproc_output(cmds, debug=False):
    if not debug:
        cmds += ['2>', '/dev/null']    
    result = __xonsh__.subproc_captured_object(cmds)
    result.rtn  # workaround https://github.com/xonsh/xonsh/issues/3394
    return result.output

def _get_executor(arg):
    m = re.match('^(python[0-9.]*|xonsh)$', arg)
    return m.group(1) if m else None

def _get_filepath(arg):
    return arg.strip("'").rstrip('\n')

def _xontrib_argcomplete_completer(prefix, line, begidx, endidx, ctx):
    """
    Argcomplete support to tab completion of python and xonsh scripts in xonsh shell.
    """
    debug = __xonsh__.env.get('XONTRIB_ARGCOMPLETE_DEBUG', False)
    py = None
    file = None

    args = __xonsh__.execer.parser.lexer.split(line)

    if len(args) == 0:
        return None

    py = _get_executor(args[0])
    if py:
        if len(args) > 1:
            file = _get_filepath(args[1])
        else:
            return None if not debug else ((prefix, 'xontrib-argcomplete DEBUG: file not found'), len(prefix))
    else:
        file = _get_filepath(args[0])

        if file.endswith('.xsh'):
            py = 'xonsh'
        elif file.endswith('.py'):
            py = 'python'

    if not Path(file).exists():
        which_maybe_file = which(file)
        if which_maybe_file and Path(which_maybe_file).exists():
            file = str(which_maybe_file)
        else:
            try:
                which_maybe_file = _get_subproc_output(['which', file], debug).strip()
            except:
                return None
            if which_maybe_file and Path(which_maybe_file).exists():
                file = which_maybe_file

    if not file:
        return None if not debug else ((prefix, 'xontrib-argcomplete DEBUG: path to file not found'), len(prefix))

    if not Path(file).exists():
        return None if not debug else ((prefix, 'xontrib-argcomplete DEBUG: file does not exists'), len(prefix))

    file_type = _get_subproc_output(['file', '--mime-type', '--brief', file], debug).strip()
    if not file_type.startswith('text'):
        return None if not debug else ((prefix, f'xontrib-argcomplete DEBUG: file type is not text: {file_type}'), len(prefix))

    found_argcomplete = False
    with open(file) as f:
        for x in range(10):
            try:
                fline = next(f)
            except:
                break
            if x == 0 and not py:
                m = re.match('.*env (python[0-9.]*|xonsh).*', fline)
                if m:
                    py = m.group(1)
                else:
                    m = re.match('#!(/.*/(python[0-9.]*|xonsh))', fline)
                    if m:
                        py = m.group(1)
                        if not Path(py).exists():
                            if debug:
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
            return None if not debug else ((prefix, 'xontrib-argcomplete DEBUG: completions not found'), len(prefix))

        return (tokens, len(prefix))

    return None

__xonsh__.completers['xontrib_argcomplete'] = _xontrib_argcomplete_completer
__xonsh__.completers.move_to_end('xontrib_argcomplete', last=False)
