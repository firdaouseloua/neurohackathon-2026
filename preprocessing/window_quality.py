"""Window-based EEG quality assessment."""

import numpy as np
import pandas as pd


def assess_windows(raw, window_seconds=5):
    """Measure channel variability in consecutive EEG windows."""

    sfreq = raw.info["sfreq"]
    window_samples = int(window_seconds * sfreq)

    data = raw.get_data(picks="eeg") * 1e6
    n_channels, n_samples = data.shape
    n_windows = n_samples // window_samples

    results = []

    for window_idx in range(n_windows):
        start = window_idx * window_samples
        stop = start + window_samples

        segment = data[:, start:stop]

        # Measure each channel within this window.
        std = np.std(segment, axis=1)
        ptp = np.ptp(segment, axis=1)

        for ch_idx, channel in enumerate(raw.ch_names):
            results.append({
                "channel": channel,
                "window": window_idx,
                "start_s": start / sfreq,
                "end_s": stop / sfreq,
                "std_uV": std[ch_idx],
                "ptp_uV": ptp[ch_idx],
            })

    return pd.DataFrame(results)
