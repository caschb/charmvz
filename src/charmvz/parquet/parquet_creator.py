from typing import Optional
import pathlib
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd


def create_parquet(
    file_path: pathlib.Path,
    parquet_path: Optional[pathlib.Path] = None,
    chunksize=100_000,
):
    columns = [
        "Container",
        "Parent",
        "Type",
        "Start",
        "End",
        "Duration",
        "Imbrication",
        "Value",
    ]
    writer: Optional[pq.ParquetWriter] = None

    if parquet_path is None:
        parquet_path = pathlib.Path("output.pq")

    for chunk in pd.read_csv(
        file_path, names=columns, chunksize=chunksize, header=None, dtype=str
    ):
        table = pa.Table.from_pandas(chunk)

        if writer is None:
            writer = pq.ParquetWriter(parquet_path, table.schema, compression="snappy")

        writer.write_table(table)
    if writer:
        writer.close()
