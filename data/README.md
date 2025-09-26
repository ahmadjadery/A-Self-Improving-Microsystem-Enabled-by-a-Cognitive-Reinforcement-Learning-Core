# /data/ Directory

This directory is the target location for the raw and processed datasets associated with the "Resilience that Learns" project.

## Populating this Directory

This directory is intentionally left empty in the main repository to keep the repository size small.

To populate this directory with the realistic, synthetic raw data used for the reproducibility analysis, please run the data generation script from the **root directory** of this repository:

```bash
python scripts/generate_raw_data.py --corner TT
