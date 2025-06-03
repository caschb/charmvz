import polars as pl
import matplotlib as mlp
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import seaborn as sns

from matplotlib.colors import LinearSegmentedColormap

custom_cmap = LinearSegmentedColormap.from_list("my_cmap", ["#ffffff", "#ff000000"])


def create_frequency_plot(dataframe: pl.DataFrame, filename="freq_plot.png"):
    frequency_df = dataframe.group_by("Chare").agg(pl.len()).sort(by="len")
    fig, ax = plt.subplots()
    ax.barh(y=frequency_df["Chare"], width=frequency_df["len"])
    ax.set_ylabel("Chare")
    ax.set_xlabel("Frequency")
    fig.savefig(filename)


def create_total_duration_plot(dataframe: pl.DataFrame, filename="duration_plot.png"):
    durations_df = (
        dataframe.group_by("Chare").agg(pl.sum("Duration")).sort(by="Duration")
    )
    fig, ax = plt.subplots()
    ax.barh(y=durations_df["Chare"], width=durations_df["Duration"])
    ax.set_ylabel("Chare")
    ax.set_xlabel("Duration (ms)")
    fig.savefig(filename)


def create_chare_activity_per_pe_heatmap(
    dataframe: pl.DataFrame,
    num_nodes=4,
    pes_per_node=20,
    filename="activity_per_pe_hm.png",
):
    agg_pe_chare_df = (
        dataframe.group_by(["Processing Element", "Chare"])
        .agg(pl.sum("Duration") * 0.001)
        .sort(["Processing Element", "Duration"])
    )
    heatmap_pe_chare_df = agg_pe_chare_df.pivot(
        index="Processing Element", on="Chare", values="Duration"
    )
    heatmap_pe_chare_df = heatmap_pe_chare_df.drop("Processing Element")
    fig = plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        heatmap_pe_chare_df,
        cmap=custom_cmap,
        # cmap=custom_cmap,  # or "magma", "coolwarm", etc.
        cbar_kws={"label": "Duration"},
        linecolor="none",
        xticklabels=heatmap_pe_chare_df.columns,
    )
    total_pes = num_nodes * pes_per_node
    for i in range(pes_per_node, total_pes, pes_per_node):
        ax.axhline(i, color="blue", linestyle="--", linewidth=2)

    ax.set_title("Processing Element Activity Heatmap")
    ax.set_xlabel("Chare")
    ax.set_ylabel("Processing Element")
    fig.savefig(filename)
