import argparse
import pathlib

import charmvz.log.logreader
from charmvz.sts.stsreader import StsReader


def main():
    parser = argparse.ArgumentParser(
        prog="Log Parser",
        description="Takes a directory for a Projections log and creates a CSV for PajeNG",
    )
    parser.add_argument("log_directory", type=pathlib.Path)
    parser.add_argument(
        "-o",
        "--out_file",
        type=pathlib.Path,
        required=False,
        help="File to output csv",
    )
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

    sts_reader = StsReader()
    sts_reader.read_sts(stsfilepath)
    logreader = charmvz.log.logreader.LogReader(logfilepaths, sts_reader)
    logreader.print_entries()


if __name__ == "__main__":
    main()
