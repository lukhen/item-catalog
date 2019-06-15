import tempfile
import time
import pytest
import pathlib
import subprocess


@pytest.mark.integrated
def test_creating_temp_dir():
    path = None
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = pathlib.PurePath(tmpdirname, "some_irrelevant_file")
        subprocess.run(["touch", path])
        assert pathlib.Path(path).exists()
    assert not pathlib.Path(path).exists()
