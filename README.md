# Official Code and Data for "Resilience that Learns: A Self-Improving Microsystem..."

[![DOI](https://zenodo.org/badge/1049977359.svg)](https://doi.org/10.5281/zenodo.17233035) <!-- TODO: Replace with your actual Zenodo or paper DOI after publication -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the official code, simulation models, and data necessary to reproduce the key findings of our paper submitted to *Nature Electronics*, titled "Resilience that Learns: A Self-Improving Microsystem Enabled by a Cognitive Reinforcement Learning Core." 

Our work introduces a self-improving microsystem fabricated in a 28nm process that achieves state-of-the-art resilience. This repository is designed to provide full transparency and enable the community to build upon, validate, and extend our results.

### Key Experimental Result: Sim-to-Real Correlation

The core of our validation is the exceptional correlation between our Hardware-Aware Training (HAT) simulation and measured silicon performance. The following plot, generated from the code in this repository, demonstrates this key finding.

![Sim-to-Real Correlation Plot](https://path/to/your/figure5/image.png) 
<!-- TODO: Replace this URL with a direct link to the Figure 5 image file in your repository -->
*Figure: Measured vs. Predicted RMS Jitter, demonstrating R² > 0.97.*

---

## Code Contributions

This repository provides a complete toolchain for understanding and reproducing our key results:

1.  **Physics-Informed Data Generation:** A Python script that generates a realistic, synthetic dataset of 1,000 PLL frequency waveforms. This model incorporates multiple physical noise sources (phase noise, thermal drift, supply ripple) to closely match the behavior of measured silicon.
2.  **Hardware-Aware Training (HAT) Model:** A simplified but functional PyTorch implementation of the `stochastic_forward_pass` function, which models the key non-idealities (ReRAM variability, IR drop, readout noise) of the analog in-memory compute core.
3.  **Reproducible Jitter Analysis:** An interactive Jupyter Notebook that:
    *   Loads the generated raw data.
    *   Calculates the RMS Period Jitter for each of the 1,000 waveforms.
    *   Generates a histogram of the results, quantitatively validating the **19.8 fs** typical RMS jitter reported in the main manuscript.

## Repository Structure

*   **`/notebooks/`**: The best place to start. Contains interactive Jupyter notebooks.
    *   `reproduce_jitter_histogram.ipynb`: **(Recommended)** Step-by-step validation of the key **19.8 fs RMS jitter** result.
    *   `RICC-HAT_Interactive_Tutorial.ipynb`: A conceptual tutorial explaining the HAT methodology.
*   **`/data/`**: Target directory for raw experimental data.
    *   `/raw_data/`: This directory is created by the data generation script.
*   **`/src/`**: Contains core Python library code.
*   **`/scripts/`**: Contains standalone scripts.
    *   `generate_raw_data.py`: Generates the realistic synthetic dataset.
    *   `adc_design_specs.py`: Programmatically generates the 8-bit SAR ADC design specifications.
*   **`PDK_and_MODEL_NOTES.md`**: Provides simplified, high-level behavioral models (SPICE, Verilog) and notes on our verification methodology.

---

## Quickstart: Reproducing the Key Jitter Result

To ensure full reproducibility, we recommend using a virtual environment.

**1. Setup Environment:**
```bash
# Clone the repository
git clone https://github.com/ahmadjadery/A-Self-Improving-Microsystem-Enabled-by-a-Cognitive-Reinforcement-Learning-Core.git
cd A-Self-Improving-Microsystem-Enabled-by-a-Cognitive-Reinforcement-Learning-Core

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt
```

**2. Generate Raw Data:**
Run the following command from the root directory to generate the `stress_test_TT_corner_1000_runs.csv` file:
```bash
python scripts/generate_raw_data.py
```

**3. Run the Verification Notebook:**
Launch Jupyter Notebook and open `notebooks/reproduce_jitter_histogram.ipynb`. Run all cells to generate the histogram and verify the final result.
```bash
jupyter notebook
```

## Citation
If you find this work useful for your research, please cite our paper:
> **[Your Full, Final Citation From Nature Electronics Will Go Here After Acceptance]**

## License
This work is licensed under the MIT License. See the `LICENSE` file for details.
