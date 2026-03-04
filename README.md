# Exploration of Turing emissions from computing

This repo contains focused on exploring the Alan Turing Institute's emissions from computing:
- `run_baskerville_emissions.ipynb`: notebook containing code for calculating the emissions from our use of Baskerville HPC, compares different fuel types and averaging methods.
- `src`: contains code for calculating energy usage from sacct data and getting carbon intensity data from the Carbon Intensity API.
- `report`: report focused on the Turing's emissions from computing, including cloud (Azure), HPC (Baskerville) and GitHub Actions.
- `explore_ci_hourly.ipynb`: notebook showing how CI changes throughout the day across different months and how this compares against Baskerville job run times.

## Methodology

The methodology for calculating carbon emissions from our use of HPC comes from the [Green Algorithms paper](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202100707) and [the GRACE-HPC docs](https://grace-hpc.readthedocs.io/en/latest/methodology.html#usage-based-energy-estimates).

## Requirements

Python dependencies:
- pandas
- matplotlib
- numpy
- pyyaml
- IPython (Jupyter)

Data you will need to run the `run_baskerville_emissions.ipynb` notebook:
- `Baskerville_total_commas.csv` (ask me)
- `cluster_info.yaml` (ask me or create your own, the format comes from [here](https://github.com/GreenAlgorithms/GreenAlgorithms4HPC/blob/main/data/cluster_info.yaml))
