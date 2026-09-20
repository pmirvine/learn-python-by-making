import platform
import shutil
import subprocess

import pytest

P00 = "00-hello-beeb"


def test_boot_banner(play):
    out = play(f"{P00}/main.py", [])
    assert out.startswith(f"Python {platform.python_version()} Computer\n")
    assert out.rstrip().endswith("Ready\n>")


@pytest.mark.skipif(shutil.which("uv") is None, reason="needs uv on the PATH")
def test_inline_dependency_script_runs(request):
    script = request.config.rootpath / "projects" / P00 / "banner.py"
    result = subprocess.run(
        ["uv", "run", "--no-project", str(script)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert "Computer" in result.stdout
