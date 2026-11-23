"""Compare raw and filtered HABS EEG."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from preprocessing.load_data import load_eeg
from preprocessing.filters import filter_eeg


bdf = Path(
    "sample/CURATED/P001/"
    "P001_day-1_task-resting-state_multimodal.bdf"
)

raw = load_eeg(bdf)
filtered = filter_eeg(raw)

# Compare a short interval from the same channel.
channel = "Fp1"
start, stop = 20, 25

sfreq = raw.info["sfreq"]
first = int(start * sfreq)
last = int(stop * sfreq)

times = raw.times[first:last]

raw_signal = raw.get_data(
    picks=[channel], start=first, stop=last
)[0] * 1e6

filtered_signal = filtered.get_data(
    picks=[channel], start=first, stop=last
)[0] * 1e6

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

axes[0].plot(times, raw_signal, linewidth=0.7)
axes[0].set_title(f"Raw EEG : {channel}")
axes[0].set_ylabel("Amplitude (µV)")

axes[1].plot(times, filtered_signal, linewidth=0.7)
axes[1].set_title(f"Filtered EEG (1-40 Hz) : {channel}")
axes[1].set_ylabel("Amplitude (µV)")
axes[1].set_xlabel("Time (s)")

for ax in axes:
    ax.grid(alpha=0.2)

fig.tight_layout()

output = Path("results/figures")
output.mkdir(parents=True, exist_ok=True)

fig.savefig(
    output / "raw_vs_filtered.png",
    dpi=180,
    bbox_inches="tight",
)

plt.close(fig)

print("Filtering completed!")
print("Figure saved to results/figures/raw_vs_filtered.png")
