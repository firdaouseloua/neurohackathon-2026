"""Compare EEG channel lists between HABS dataset versions."""

from pathlib import Path
from preprocessing.load_data import load_eeg

base = Path("sample")

filename = "P001_day-1_task-resting-state_multimodal.bdf"

curated = load_eeg(base / "CURATED" / "P001" / filename)
preprocessed = load_eeg(base / "PREPROCESSED" / "P001" / filename)

curated_channels = set(curated.ch_names)
preprocessed_channels = set(preprocessed.ch_names)

print("\n===== CHANNEL COMPARISON =====")

print("CURATED:", len(curated_channels))
print("PREPROCESSED:", len(preprocessed_channels))

print("\nMissing from PREPROCESSED:")
print(sorted(curated_channels - preprocessed_channels))

print("\nOnly in PREPROCESSED:")
print(sorted(preprocessed_channels - curated_channels))

print("\nCommon channels:")
print(len(curated_channels & preprocessed_channels))

print("\nSampling frequencies:")
print("CURATED:", curated.info["sfreq"])
print("PREPROCESSED:", preprocessed.info["sfreq"])
