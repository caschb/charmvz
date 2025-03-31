import pytest
from charmvz.sts.stsreader import StsReader, WrongFileExtensionError

def detects_wrong_filetype():
    reader = StsReader()
    with pytest.raises(WrongFileExtensionError):
        reader.read_sts("Nofile.txt")

def correctly_opens_file():
    reader = StsReader()
    reader.read_sts("resources/leanmd.prj.sts")
