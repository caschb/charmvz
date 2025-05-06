from charmvz.sts.stsreader import StsReader, WrongFileExtensionError

import sys


def main(argv):
    if len(argv) < 2:
        print(f"Usage: ./{argv[0]} <sts file>")
        exit(-1)

    sts_reader = StsReader()

    try:
        sts_reader.read_sts(argv[1])
    except WrongFileExtensionError:
        print("Error!")
        exit(-1)

    print(len(sts_reader.chares), sts_reader.total_chares)

    print("Chares: ")
    for key in sts_reader.chares.keys():
        print(key, sts_reader.chares[key])

    print("Entry chares: ")
    for key in sts_reader.entry_chares.keys():
        print(key, sts_reader.entry_names[key], sts_reader.entry_chares[key])


if __name__ == "__main__":
    main(sys.argv)
