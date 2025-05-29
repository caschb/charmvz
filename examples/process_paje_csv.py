from charmvz.parquet.parquet_creator import create_parquet

import sys
import pathlib

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <paje_dump>.csv")
        sys.exit(-1)

    create_parquet(pathlib.Path(sys.argv[1]))

if __name__ == '__main__':
    main()
