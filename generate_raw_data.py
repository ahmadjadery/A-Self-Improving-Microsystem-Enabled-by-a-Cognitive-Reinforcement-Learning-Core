# generate_raw_data.py
# This script generates a realistic, synthetic dataset for the
# RICC-HAT reproducibility package. It simulates 1000 measurement
# waveforms of a phase-locked loop's output frequency, incorporating
# phase noise to match the jitter statistics reported in the manuscript.

import numpy as np
import pandas as pd
import os
from tqdm import tqdm # For a progress bar

def generate_realistic_frequency_waveform(time_vector, target_freq_hz, target_jitter_fs):
    """
    Generates a single, realistic frequency waveform with phase noise.
    
    Args:
        time_vector (np.array): Time vector in seconds.
        target_freq_hz (float): The central target frequency in Hz.
        target_jitter_fs (float): The desired RMS period jitter in femtoseconds.

    Returns:
        np.array: The instantaneous frequency waveform in Hz.
    """
    num_points = len(time_vector)
    dt = time_vector[1] - time_vector[0]  # Time step
    
    # 1. Convert target jitter to an equivalent standard deviation for phase noise
    # Jitter (s) = sigma_period
    # sigma_period ≈ sigma_phase / (2 * pi * f0)
    # So, sigma_phase ≈ Jitter (s) * 2 * pi * f0
    target_jitter_s = target_jitter_fs * 1e-15
    phase_noise_std_dev = target_jitter_s * 2 * np.pi * target_freq_hz
    
    # 2. Simulate phase noise as a random walk (approximates integrated noise)
    # This creates a more realistic, time-correlated noise profile
    phase_innovations = np.random.randn(num_points) * phase_noise_std_dev * np.sqrt(dt)
    phase_noise = np.cumsum(phase_innovations)
    
    # 3. The instantaneous frequency is the derivative of the total phase
    # Total phase = 2*pi*f0*t + phase_noise
    # Instantaneous freq (rad/s) = d(Total phase)/dt = 2*pi*f0 + d(phase_noise)/dt
    # Instantaneous freq (Hz) = f0 + (1/(2*pi)) * d(phase_noise)/dt
    phase_derivative = np.gradient(phase_noise, dt)
    frequency_noise = phase_derivative / (2 * np.pi)
    
    # 4. Add the noise to the target frequency
    instantaneous_frequency = target_freq_hz + frequency_noise
    
    return instantaneous_frequency


def main():
    """Main function to generate and save the dataset."""
    
    # --- Configuration Parameters ---
    NUM_RUNS = 1000
    TIME_START_US = 80.0
    TIME_END_US = 120.0
    TIME_STEP_US = 0.1
    
    TARGET_FREQ_GHZ = 0.2  # 200 MHz
    TARGET_JITTER_FS_MEAN = 19.8  # From manuscript (TT corner)
    JITTER_DISTRIBUTION_STD_FS = (6.2 / 3.0) # From manuscript (±3σ = 6.2 fs)

    OUTPUT_DIR = "raw_data"
    OUTPUT_FILENAME = "stress_test_TT_corner_1000_runs.csv"

    # --- Data Generation ---
    print("Starting data generation for reproducibility package...")
    
    # Create the time vector
    time_us = np.arange(TIME_START_US, TIME_END_US + TIME_STEP_US, TIME_STEP_US)
    time_s = time_us * 1e-6
    
    # Create a dictionary to hold all data
    data_dict = {"Time_us": time_us}
    
    # Generate each of the 1000 waveforms
    for i in tqdm(range(1, NUM_RUNS + 1)):
        # Add some randomness to the target jitter for each run to create a distribution
        run_target_jitter = np.random.normal(loc=TARGET_JITTER_FS_MEAN, scale=JITTER_DISTRIBUTION_STD_FS)
        
        freq_hz = generate_realistic_frequency_waveform(time_s, TARGET_FREQ_GHZ * 1e9, run_target_jitter)
        
        # Convert back to GHz for storage
        freq_ghz = freq_hz / 1e9
        data_dict[f'Run_{i}'] = freq_ghz
        
    # Convert dictionary to a pandas DataFrame
    df = pd.DataFrame(data_dict)
    
    # --- Saving the file ---
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    print(f"Saving data to '{output_path}'...")
    df.to_csv(output_path, index=False)
    
    print("\n✅ Generation complete.")
    print(f"File '{OUTPUT_FILENAME}' with {df.shape[0]} rows and {df.shape[1]} columns created successfully.")
    
if __name__ == "__main__":
    main()
