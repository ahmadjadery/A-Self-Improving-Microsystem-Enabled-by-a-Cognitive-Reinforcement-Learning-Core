# src/jitter_analysis.py
# Provides functions to analyze jitter from frequency waveform data.

import numpy as np

def calculate_rms_period_jitter(time_series_s, frequency_series_hz):
    """
    Calculates the RMS Period Jitter from a frequency vs. time waveform.

    Args:
        time_series_s (np.array): Time vector in seconds.
        frequency_series_hz (np.array): Instantaneous frequency vector in Hz.

    Returns:
        float: RMS Period Jitter in femtoseconds (fs).
    """
    # 1. Convert frequency to instantaneous period
    # Add a small epsilon to avoid division by zero if frequency is zero
    period_series_s = 1.0 / (frequency_series_hz + 1e-12)
    
    # 2. Calculate the mean period
    mean_period_s = np.mean(period_series_s)
    
    # 3. Calculate the period deviations (the "jitter" itself)
    period_deviations_s = period_series_s - mean_period_s
    
    # 4. Calculate the Root Mean Square (RMS) of the deviations
    rms_jitter_s = np.sqrt(np.mean(period_deviations_s**2))
    
    # 5. Convert from seconds to femtoseconds (1 s = 1e15 fs)
    rms_jitter_fs = rms_jitter_s * 1e15
    
    return rms_jitter_fs
