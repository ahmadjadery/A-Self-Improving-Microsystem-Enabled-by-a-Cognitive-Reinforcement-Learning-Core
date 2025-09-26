# src/jitter_analysis.py
# (Version 2.0 - Final, with Enhanced Documentation)
"""
Provides a robust function to calculate RMS Period Jitter from discrete
time-domain frequency waveform data, as measured from a real-time
spectrum analyzer or high-speed oscilloscope.

This methodology is used in the `reproduce_jitter_histogram.ipynb` notebook.
"""

import numpy as np

def calculate_rms_period_jitter(time_series_s, frequency_series_hz):
    """
    Calculates the RMS Period Jitter from an instantaneous frequency waveform.

    This function assumes the input waveform represents a stationary process
    (i.e., the PLL is in a locked, steady-state condition).

    Args:
        time_series_s (np.array): Time vector in seconds. Should be uniformly spaced.
        frequency_series_hz (np.array): Instantaneous frequency vector in Hz.

    Returns:
        float: RMS Period Jitter in femtoseconds (fs).
    """
    # --- Pre-computation Checks ---
    if len(time_series_s) != len(frequency_series_hz):
        raise ValueError("Time and frequency series must have the same length.")
    if len(time_series_s) < 10:
        # A reasonable number of points is needed for a stable statistic
        raise ValueError("Input series is too short for a reliable jitter calculation.")
        
    # --- Calculation Steps ---
    
    # 1. Convert instantaneous frequency [Hz] to instantaneous period [s]
    # An epsilon is added for numerical stability in case of zero frequency points.
    period_series_s = 1.0 / (frequency_series_hz + 1e-12)
    
    # 2. Calculate the mean period over the observation window
    mean_period_s = np.mean(period_series_s)
    
    # 3. Calculate the deviation of each period from the mean
    period_deviations_s = period_series_s - mean_period_s
    
    # 4. Calculate the Root Mean Square (RMS) of these deviations
    # This is the definition of RMS Period Jitter.
    rms_jitter_s = np.sqrt(np.mean(np.square(period_deviations_s)))
    
    # 5. Convert the final result from seconds to femtoseconds for reporting
    rms_jitter_fs = rms_jitter_s * 1e15
    
    return rms_jitter_fs
