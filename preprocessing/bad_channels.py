"""Detect potentially bad EEG channels using simple signal statistics."""

import numpy as np
import pandas as pd


def detect_bad_channels(raw):
    """Flag suspicious EEG channels without removing them."""

    data = raw.get_data(picks="eeg") * 1e6

    # Standard deviation in microvolts.
    std = np.std(data, axis=1)

    # Peak-to-peak amplitude.
    ptp = np.ptp(data, axis=1)

    # Median absolute deviation for robust outlier detection.
    median_std = np.median(std)
    mad_std = np.median(np.abs(std - median_std))

    # Avoid division by zero.
    if mad_std == 0:
        mad_std = 1e-12

    robust_z = 0.6745 * (std - median_std) / mad_std

    results = pd.DataFrame({
        "channel": raw.ch_names,
        "std_uV": std,
        "ptp_uV": ptp,
        "robust_z": robust_z,
    })

    # Initial heuristic thresholds, to be validated.
    results["flat"] = std < 0.5
    results["high_variance"] = robust_z > 3.5
    results["low_variance"] = robust_z < -3.5

    results["suspected_bad"] = (
        results["flat"]
        | results["high_variance"]
        | results["low_variance"]
    )

    return results

