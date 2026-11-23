"""Load EEG recordings from the HABS dataset."""

from pathlib import Path
import sys

import mne
import numpy as np

# Reuse the loader provided by the neuro-hackathon
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "starting_notebooks"))

from bdf_loader import load_bdf  # noqa: E402


TO_VOLTS = {
    "V": 1.0,
    "mV": 1e-3,
    "uV": 1e-6,
    "µV": 1e-6,
    "μV": 1e-6,
    "nV": 1e-9,
}


def load_eeg(bdf_path):
    """Load only EEG channels and return an MNE Raw object."""
    raw, signals, channels = load_bdf(Path(bdf_path))

    electrodes = channels.loc[
        channels.mne_type == "eeg", "bdf_label"
    ].tolist()

    units = channels.set_index("bdf_label")["header_unit"].to_dict()

    eeg_data = np.vstack([
        signals[ch].to_numpy() * TO_VOLTS[units[ch]]
        for ch in electrodes
    ])

    info = mne.create_info(
        ch_names=electrodes,
        sfreq=float(raw.info["sfreq"]),
        ch_types="eeg",
    )

    return mne.io.RawArray(eeg_data, info, verbose=False)
