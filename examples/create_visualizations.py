import polars as pl

from sys import argv

from charmvz.analysis import visualization


def main():
    if len(argv) != 2:
        print(f"Correct usage: f{argv[0]} <parquet filename>.pq")
        exit(-1)

    print("Reading parquet file..")
    df = pl.read_parquet(
        argv[1], columns=["Parent", "Start", "End", "Duration", "Value"]
    )
    print("Pre-processing data..")
    df = df.drop_nulls()

    for col in df.iter_columns():
        col = col.str.strip_chars()
        if col.name == "Parent":
            col = col.str.replace(r"^pe", "").cast(pl.Int32)
        elif col.name != "Value":
            col = col.cast(pl.Float32)
        df = df.with_columns(col)

    df = df.rename({"Value": "Chare", "Parent": "Processing Element"})
    df = df.filter(pl.col.Duration > 0.0)

    print("Creating frequency plot..")
    visualization.create_frequency_plot(df, filename=f"freq_plot_{argv[1].split("_")[-1].split(".")[0]}.png")
    print("Creating total duration plot..")
    visualization.create_total_duration_plot(df)
    print("Creating activity per pe heatmap..")
    visualization.create_chare_activity_per_pe_heatmap(df)

if __name__ == "__main__":
    main()
