import pytest
import sys
import requests
from pathlib import PurePath
import subprocess
import time
from tempfile import TemporaryDirectory


@pytest.fixture
def app_process():
    with TemporaryDirectory() as tmpdir:
        install_app_from_github(tmpdir)
        proc = subprocess.Popen(
            [PurePath(tmpdir, ".venv", "bin", "python"), "-m", "flaskapp"]
        )
        yield proc
        proc.kill()


@pytest.mark.e2e
def test_e2e(app_process):
    """
    This is the first teeny-tiny feature of the item-catalog app.
    I call this test the 'walking skeleton', after Nat Pryce in his book.
    It serves the purpose of setting up the skeleton of the application.
    It has to be automated and totally end to end.
    Totally means really 'totally', along with automatically installing the app
    and running it.

    User story:
    A new-comming user enters the item-catalog web site http://localhost:5000.
    The page loads without any errors.
    """
    time.sleep(1)
    status_code = requests.get("http://localhost:5000").status_code

    assert status_code == 200


def install_app_from_github(location_dir):
    subprocess.run(["python", "-m", "venv", PurePath(location_dir, ".venv")])
    subprocess.run(
        [
            PurePath(location_dir, ".venv", "bin", "pip"),
            "install",
            "git+https://github.com/lukhen/item-catalog.git",
        ]
    )
