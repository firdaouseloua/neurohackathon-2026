"""Visualize window-based EEG variability."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from preprocessing.load_data import load_eeg
from preprocessing.window_quality import assess_windows


bdf = Path(
    "sample/CURATED/P001/"
    "P001_day-1_task-resting-state_multimodal.bdf"
)

raw = load_eeg(bdf)
quality = assess_windows(raw, window_seconds=5)

matrix = quality.pivot(
    index="channel",
    columns="window",
    values="std_uV",
)

# Keep the original electrode order.
matrix = matrix.reindex(raw.ch_names)

fig, ax = plt.subplots(figsize=(14, 12))

image = ax.imshow(
    np.log10(matrix.to_numpy() + 1),
    aspect="auto",
    interpolation="nearest",
    cmap="viridis",
)

ax.set_yticks(range(len(matrix.index)))
ax.set_yticklabels(matrix.index, fontsize=7)

ax.set_xlabel("5-second window")
ax.set_ylabel("EEG channel")
ax.set_title("EEG variability across time : P001 CURATED")

fig.colorbar(
    image,
    ax=ax,
    label="log10(Standard deviation in µV + 1)",
)

fig.tight_layout()

output = Path("results/figures")
output.mkdir(parents=True, exist_ok=True)

fig.savefig(
    output / "window_quality_heatmap.png",
    dpi=180,
    bbox_inches="tight",
)

quality.to_csv(
    Path("results/window_quality_P001.csv"),
    index=False,
)

plt.close(fig)

print("Window quality analysis completed!")
print("Windows:", quality["window"].nunique())
print("Channels:", quality["channel"].nunique())
print("Saved: results/figures/window_quality_heatmap.png")
