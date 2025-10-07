# bindcraft-analysis-app

## Overview

This repository hosts the `bindcraft-analysis-app`, a Streamlit dashboard designed to provide an intuitive and interactive platform for analyzing output from [BindCraft](https://github.com/martinpacesa/BindCraft) runs. Users can easily upload their Protein Data Bank (PDB) files to visualize the binding interface, explore detailed statistics, and apply various filters and sorting options to gain deeper insights into their protein-ligand interactions.

BindCraft is an open-source and automated pipeline for *de novo* protein binder design, utilizing advanced techniques such as AlphaFold2 backpropagation, MPNN, and PyRosetta [1, 2]. This analysis app aims to make the results of such powerful computational design more accessible and interpretable for researchers.

## Features

*   **PDB Upload**: Seamlessly upload your PDB files containing BindCraft analysis results.
*   **Binding Interface Visualization**: Interactively view the protein-ligand binding interface directly within the dashboard.
*   **Statistical Summary**: Access a comprehensive summary of key statistics from your BindCraft runs.
*   **Filtering and Sorting**: Customize your view of the data with powerful filtering and sorting capabilities.
*   **User-Friendly Interface**: A clean and intuitive Streamlit interface designed for ease of use.

## Getting Started

### Accessing the `bindcraft-analysis-app`

This application is hosted on Streamlit Cloud, providing easy access without any local installation required. The link to the live application will be provided here once deployed.

### Generating BindCraft Analysis Output

To utilize this analysis app, you first need to generate output from BindCraft. The original BindCraft software repository can be found here: [https://github.com/martinpacesa/BindCraft](https://github.com/martinpacesa/BindCraft).

For users looking for a streamlined setup to run BindCraft, especially on cloud platforms, we recommend the following repository:

*   **BindCraft on RunPod Cloud**: [https://github.com/A-Yarrow/bindcraft-runpod](https://github.com/A-Yarrow/bindcraft-runpod)

This repository provides a full setup for running BindCraft on RunPod. After generating your analysis data using the `bindcraft-runpod` setup, you can then upload your PDB files to this `bindcraft-analysis-app` for visualization and detailed analysis.

## Contribution

This project is open source and built for the community. We encourage contributions from developers, researchers, and anyone interested in improving protein binder analysis. Whether it's bug fixes, new features, or documentation improvements, your input is highly valued. Please refer to the `CONTRIBUTING.md` file (to be added) for guidelines on how to contribute.

## References

[1] Pacesa, M. (2024). *BindCraft: one-shot design of functional protein binders*. bioRxiv. [https://www.biorxiv.org/content/10.1101/2024.09.30.615802v1]
