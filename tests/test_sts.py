import pytest
from charmvz.sts.stsreader import StsReader, WrongFileExtensionError


def test_detects_wrong_filetype():
    reader = StsReader()
    with pytest.raises(WrongFileExtensionError):
        reader.read_sts("Nofile.txt")


def test_correctly_opens_file():
    reader = StsReader()
    reader.read_sts("tests/resources/leanmd.prj.sts")
