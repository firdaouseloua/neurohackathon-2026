from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from preprocessing.load_data import load_eeg
from preprocessing.filters import filter_eeg

curated_bdf = Path(
    "sample/CURATED/P001/"
    "P001_day-1_task-resting-state_multimodal.bdf"
)

preprocessed_bdf = Path(
    "sample/PREPROCESSED/P001/"
    "P001_day-1_task-resting-state_multimodal.bdf"
)

raw_curated = load_eeg(curated_bdf)
raw_preprocessed = load_eeg(preprocessed_bdf)
our_filtered = filter_eeg(raw_curated)

channel = "Fp1"
start, stop = 20, 25

sfreq = raw_curated.info["sfreq"]
first = int(start * sfreq)
last = int(stop * sfreq)

times = raw_curated.times[first:last]

curated_signal = raw_curated.get_data(
    picks=[channel], start=first, stop=last
)[0] * 1e6

filtered_signal = our_filtered.get_data(
    picks=[channel], start=first, stop=last
)[0] * 1e6

preprocessed_signal = raw_preprocessed.get_data(
    picks=[channel], start=first, stop=last
)[0] * 1e6

fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

axes[0].plot(times, curated_signal, linewidth=0.7)
axes[0].set_title(f"CURATED raw EEG : {channel}")
axes[0].set_ylabel("Amplitude (µV)")

axes[1].plot(times, filtered_signal, linewidth=0.7)
axes[1].set_title(f"Our filtered EEG (1-40 Hz) : {channel}")
axes[1].set_ylabel("Amplitude (µV)")

axes[2].plot(times, preprocessed_signal, linewidth=0.7)
axes[2].set_title(f"HABS PREPROCESSED EEG : {channel}")
axes[2].set_ylabel("Amplitude (µV)")
axes[2].set_xlabel("Time (s)")

for ax in axes:
    ax.grid(alpha=0.2)

fig.tight_layout()

output = Path("results/figures")
output.mkdir(parents=True, exist_ok=True)

fig.savefig(
    output / "curated_vs_ours_vs_preprocessed.png",
    dpi=180,
    bbox_inches="tight",
)

plt.close(fig)

print("Comparison figure saved to:")
print("results/figures/curated_vs_ours_vs_preprocessed.png")
print()
print("Durations:")
print("CURATED:", raw_curated.times[-1])
print("OURS:", our_filtered.times[-1])
print("PREPROCESSED:", raw_preprocessed.times[-1])
print()
print("EEG channels:")
print("CURATED:", len(raw_curated.ch_names))
print("OURS:", len(our_filtered.ch_names))
print("PREPROCESSED:", len(raw_preprocessed.ch_names))