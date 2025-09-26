# generate_raw_data.py (Version 2.0 - Ultra-Realistic)
# This script generates a highly realistic, physics-informed synthetic dataset
# for the RICC-HAT reproducibility package, incorporating multiple noise sources.

import numpy as np
import pandas as pd
import os
from tqdm import tqdm

def generate_ultra_realistic_waveform(time_vector, target_freq_hz, target_jitter_fs):
    """
    Generates a single, ultra-realistic frequency waveform incorporating
    multiple physically-motivated noise and drift sources.
    
    Args:
        time_vector (np.array): Time vector in seconds.
        target_freq_hz (float): The central target frequency in Hz.
        target_jitter_fs (float): The desired RMS period jitter in femtoseconds.

    Returns:
        np.array: The instantaneous frequency waveform in Hz.
    """
    num_points = len(time_vector)
    dt = time_vector[1] - time_vector[0]
    
    # --- 1. Base Phase Noise (as before, but will be combined) ---
    target_jitter_s = target_jitter_fs * 1e-15
    phase_noise_std_dev = target_jitter_s * 2 * np.pi * target_freq_hz
    phase_innovations = np.random.randn(num_points) * phase_noise_std_dev * np.sqrt(dt)
    base_phase_noise = np.cumsum(phase_innovations)
    
    # --- 2. Low-Frequency Drift (Thermal Drift Simulation) ---
    # Simulates a very slow, random linear drift over the 40us window.
    # The drift will be tiny, e.g., a few kHz over the entire window.
    drift_rate_hz_per_s = (np.random.rand() - 0.5) * 5e7  # up to +/- 25 kHz/s
    thermal_drift_in_phase = 2 * np.pi * drift_rate_hz_per_s * (time_vector**2 / 2)
    
    # --- 3. Power Supply Noise (Ripple Simulation) ---
    # Simulates a small ripple from a switching regulator, e.g., at 50 MHz.
    ripple_freq_hz = 50e6
    ripple_amplitude_hz = target_freq_hz * 1e-6 # 1 ppm frequency pushing
    psu_noise_in_phase = (ripple_amplitude_hz / ripple_freq_hz) * np.sin(2 * np.pi * ripple_freq_hz * time_vector + np.random.rand()*2*np.pi)
    
    # --- 4. Combine all phase effects ---
    total_phase_noise = base_phase_noise + thermal_drift_in_phase + psu_noise_in_phase
    
    # --- 5. Differentiate phase to get frequency ---
    phase_derivative = np.gradient(total_phase_noise, dt)
    frequency_noise_hz = phase_derivative / (2 * np.pi)
    
    instantaneous_frequency_hz = target_freq_hz + frequency_noise_hz
    
    return instantaneous_frequency_hz

# Main execution part remains largely the same
def main():
    """Main function to generate and save the dataset."""
    
    # --- Configuration Parameters ---
    NUM_RUNS = 1000
    TIME_START_US = 80.0
    TIME_END_US = 120.0
    TIME_STEP_US = 0.1
    
    TARGET_FREQ_GHZ = 0.2
    TARGET_JITTER_FS_MEAN = 19.8
    JITTER_DISTRIBUTION_STD_FS = (6.2 / 3.0)

    OUTPUT_DIR = "raw_data"
    OUTPUT_FILENAME = "stress_test_TT_corner_1000_runs.csv"

    # --- Data Generation ---
    print("Starting ULTRA-REALISTIC data generation...")
    
    time_us = np.arange(TIME_START_US, TIME_END_US + TIME_STEP_US, TIME_STEP_US)
    time_s = time_us * 1e-6
    
    data_dict = {"Time_us": time_us}
    
    for i in tqdm(range(1, NUM_RUNS + 1)):
        run_target_jitter = np.random.normal(loc=TARGET_JITTER_FS_MEAN, scale=JITTER_DISTRIBUTION_STD_FS)
        
        freq_hz = generate_ultra_realistic_waveform(time_s, TARGET_FREQ_GHZ * 1e9, run_target_jitter)
        
        freq_ghz = freq_hz / 1e9
        data_dict[f'Run_{i}'] = freq_ghz
        
    df = pd.DataFrame(data_dict)
    
    # --- Saving the file ---
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    print(f"Saving data to '{output_path}'...")
    df.to_csv(output_path, index=False, float_format='%.7f') # Save with high precision
    
    print("\n✅ Generation complete.")
    print(f"File '{OUTPUT_FILENAME}' created successfully.")
    
if __name__ == "__main__":
    main()
