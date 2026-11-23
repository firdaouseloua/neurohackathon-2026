"""Test bad-channel detection on participant P001."""

from pathlib import Path

from preprocessing.load_data import load_eeg
from preprocessing.filters import filter_eeg
from preprocessing.bad_channels import detect_bad_channels


bdf = Path(
    "sample/CURATED/P001/"
    "P001_day-1_task-resting-state_multimodal.bdf"
)

raw = load_eeg(bdf)

# Detect on raw EEG to avoid hiding large slow artifacts.
results = detect_bad_channels(raw)

print("\n===== CHANNEL QUALITY =====")
print(results.to_string(index=False))

bad = results.loc[results["suspected_bad"], "channel"].tolist()

print("\nSuspected bad channels:", bad)
print("Number of suspected bad channels:", len(bad))

output = Path("results")
output.mkdir(exist_ok=True)

results.to_csv(output / "bad_channels_P001.csv", index=False)
print("\nSaved: results/bad_channels_P001.csv")
