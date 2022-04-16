from pytest import fixture


@fixture(autouse=True)
def argcomplete(load_xontrib, xession):
    return load_xontrib("argcomplete")


def test_cmd_pytest(check_completer, os_env, xession):
    xession.env["PATH"] = os_env["PATH"]
    out = check_completer("pytest", prefix="-")
    assert out.issuperset({
        '--log-format',
        '--log-level',
        '--markers',
        '--maxfail',
        '--new-first',
        '--nf',
        '--no-header',
        '--no-summary',
        '--noconftest',
        '--override-ini',
        '--pastebin',
        '--pdb',
        '--pdbcls',
        '--pyargs',
        '--pythonwarnings',
        '--quiet',
        '--rootdir',
        '--runxfail',
        '--setup-only',
        '--setup-plan',
        '--setup-show',
        '--setuponly',
        '--setupplan',
        '--setupshow',
        '--show-capture',
    })
