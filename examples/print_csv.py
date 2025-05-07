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
    parser.add_argument(
        "-o",
        "--out_file",
        type=pathlib.Path,
        required=False,
        help="File to output csv",
    )
    args = parser.parse_args()
    log_directory: pathlib.Path = args.log_directory
    out_file: pathlib.Path = args.out_file
    print(out_file)

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
    logreader.read_logs()
    logreader.print_entries(out_file)


if __name__ == "__main__":
    main()
