import pathlib
from charmvz.sts.stsreader import StsReader
import charmvz.log.logreader
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="Log Parser",
        description="Takes a directory for a Projections log and creates a CSV for PajeNG",
    )
    parser.add_argument("log_directory", type=pathlib.Path)
    args = parser.parse_args()
    log_directory: pathlib.Path = args.log_directory

    stsfilepath = None
    logfilepaths = []

    for file in log_directory.iterdir():
        if file.suffix == ".sts":
            stsfilepath = file
        elif file.suffix == ".gz" or file.suffix == ".log":
            logfilepaths.append(file)

    assert stsfilepath is not None
    assert len(logfilepaths) > 0

    logreader = charmvz.log.logreader.LogReader(logfilepaths)
    logreader.read_log(0)
    logreader.read_log(1)


if __name__ == "__main__":
    main()
