# app-egi2mne

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.742-blue.svg)](https://doi.org/10.25663/brainlife.app.742)

## Description

Converts EGI EEG `.raw` files to MNE-compatible `.fif` format using `mne.io.read_raw_egi` from MNE-Python. This app enables downstream processing of EGI data through the Brainlife.io ecosystem.

## Inputs

- **egi**: EGI `.raw` EEG data file
- **include** (optional): Comma-separated list of channels to include during conversion
- **bads** (optional): Comma-separated list of channels to mark as bad

## Outputs

- **out_dir/raw.fif**: Converted raw data in MNE format
- **out_report/report.html**: QC report containing raw data summary and channel information
- **product.json**: Metadata with channel information and positions

## Configuration Parameters

### Required
- `egi`: Path to the input EGI `.raw` file

### Optional
- `include`: Comma-separated channel names to select (e.g., "D101,D102,D103"). If empty or "None", all channels are included.
- `bads`: Comma-separated channel names to mark as bad (e.g., "D101,D115"). Marked channels will be excluded from analysis by downstream processing steps.

## Usage

The app processes the EGI file and generates:
1. A converted `.fif` file ready for downstream MNE processing
2. An HTML report with channel information and raw data visualization
3. A product.json file with metadata for Brainlife.io

## Technical Details

- Execution: Singularity container with brainlife/mne Docker image
- Format conversion: EGI `.raw` → MNE `.fif`
- Channel filtering: Optional channel selection during conversion
- Report generation: MNE Report object for quality control

## Authors

- [Guiomar Niso](https://github.com/guiomar), Instituto Cajal, CSIC, Spain
- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

**brainlife.io: A decentralized and open source cloud platform to support neuroscience research**. Hayashi, S., Caron, B. A., et al. & Pestilli, F. (2023). ArXiv. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10274934/

**MEG and EEG data analysis with MNE-Python**. Gramfort A, et al. & Hämäläinen MS. (2013). Frontiers in Neuroscience, 7(267):1–13. https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

#### MIT Copyright (c) 2026 brainlife.io The University of Texas at Austin and Indiana University

## Citation

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
