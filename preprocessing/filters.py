"""Basic EEG filtering for the HABS dataset."""


def filter_eeg(raw):
    """Apply a band-pass and notch filter to EEG data."""

    eeg = raw.copy()

    # For now, keep frequencies between 1 and 40 Hz.
    eeg.filter(
        l_freq=1.0,
        h_freq=40.0,
        picks="eeg",
        method="fir",
        phase="zero",
        verbose=False,
    )

    # Remove electrical interference at 50 Hz if present.
    # Note: the 40 Hz low-pass already attenuates 50 Hz.
    # We can evaluate whether a separate notch is needed later.

    return eeg
