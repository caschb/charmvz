import os


class StsReader:
    def __init__(self):
        pass

    def read_sts(self, fullpath: os.PathLike):
        extension = os.path.splitext(fullpath)[-1][1:]
        if extension != "sts":
            raise IOError(f"Wrong file type: {extension}")
        with open(fullpath, "r") as f:
            print(os.path.basename(fullpath), len(f.readlines()))
