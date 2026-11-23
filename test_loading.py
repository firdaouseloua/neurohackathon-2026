from pathlib import Path

from preprocessing.load_data import load_eeg

bdf = Path(
    "sample/CURATED/P001/"
    "P001_day-1_task-resting-state_multimodal.bdf"
)

eeg = load_eeg(bdf)

print(eeg)
print("Sampling frequency:", eeg.info["sfreq"])
print("EEG channels:", len(eeg.ch_names))
print("Duration (seconds):", eeg.times[-1])
print("First five channels:", eeg.ch_names[:5])
