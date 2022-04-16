import os

import pytest


@pytest.fixture(autouse=True)
def argcomplete(load_xontrib, xession, os_env):
    # relative paths should work now
    os.chdir(os.path.dirname(__file__))

    xession.env["PATH"] = os_env["PATH"]
    return load_xontrib("argcomplete")


def test_cmd_pytest(check_completer):
    out = check_completer("pytest", prefix="-")
    assert out.issuperset(
        {
            "--log-format",
            "--log-level",
            "--markers",
            "--maxfail",
            "--new-first",
            "--nf",
            "--no-header",
            "--no-summary",
            "--noconftest",
            "--override-ini",
            "--pastebin",
            "--pdb",
            "--pdbcls",
            "--pyargs",
            "--pythonwarnings",
            "--quiet",
            "--rootdir",
            "--runxfail",
            "--setup-only",
            "--setup-plan",
            "--setup-show",
            "--setuponly",
            "--setupplan",
            "--setupshow",
            "--show-capture",
        }
    )


class TestScripts:
    """test executing a script"""

    @pytest.mark.parametrize(
        "cmd, file",
        [
            ("python", "proto.py"),
            pytest.param(
                "xonsh",
                "proto.xsh",
                marks=pytest.mark.xfail(
                    reason="the xompletions/xonsh is interfering and will fail"
                ),
            ),
        ],
    )
    def test_executing_scripts(self, check_completer, cmd, file):
        out = check_completer(f"{cmd} {file}", prefix="-")
        assert out.issuperset({"--proto"})

    @pytest.mark.parametrize(
        "cmd",
        [
            "./proto",
            "./proto.py",
            "./proto.xsh",
        ],
    )
    @pytest.mark.parametrize(
        "line, expected",
        [
            ("-", {"--proto", "-h"}),
            ("--proto ", {"http", "https", "rsync", "ssh", "wss"}),
        ],
    )
    def test_shebang_scripts(self, check_completer, cmd, line, expected):
        out = check_completer(f"{cmd} {line}", prefix=None)
        assert out.issuperset(expected)
