# Convert EGI EEG Data to MNE Format

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.742-blue.svg)](https://doi.org/10.25663/brainlife.app.742)

## Description

Converts EGI EEG `.raw` files to MNE-compatible `.fif` format using `mne.io.read_raw_egi` from MNE-Python. Channels can be labeled as EOG, ECG or MISC, additional channels can be marked as bad, and trigger/event channels can be combined either into `mne.Annotations` or into a synthetic `STI 014` trigger channel. Flat (zero-variance) channels are marked as bad by default. This app enables downstream processing of EGI data through the Brainlife.io ecosystem.

The app generates:
- A converted raw `.fif` file (`out_dir/raw.fif`)
- A QC report with channel information (`out_report/report.html`)
- A power spectral density figure (`out_figs/psd.png`)
- A `product.json` summarizing channel info, bad channels and positions

## Inputs

- **`egi`** (`neuro/eeg/egi`): EGI `.raw` EEG data file to convert (required)

## Outputs

- **`out_dir/raw.fif`** (`neuro/meeg/mne/raw`): converted raw EEG data in MNE format, with EOG/ECG/MISC channel types, bad channels, and trigger/event information applied.
- **`out_report/report.html`**: QC report containing raw data summary and channel information.
- **`out_figs/psd.png`**: Power Spectral Density plot of the converted data.
- **`product.json`**: Metadata with channel information, bad-channel summary and channel positions.

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `eog` | string | `""` (None) | Comma-separated list of channel names to mark as EOG. |
| `ecg` | string | `""` (None) | Comma-separated list of channel names to mark as ECG. |
| `misc` | string | `""` (None) | Comma-separated list of channel names to mark as MISC (miscellaneous). |
| `include` | string | `""` (None) | Comma-separated list of stimulus channel names to combine into trigger events — either `mne.Annotations` or a synthetic `STI 014` channel, depending on `events_as_annotations`. |
| `bads` | string | `""` (None) | Comma-separated list of channel names to additionally mark as bad. Channels not present in the data are ignored. |
| `rm_flat` | boolean | `true` | If `true`, channels that are strictly flat (zero variance) are marked as bad. |
| `events_as_annotations` | boolean | `true` | If `true`, experiment events from the `include` channels are converted to `mne.Annotations`. If `false`, a synthetic trigger channel `STI 014` is created instead. |

## Usage

### Running on Brainlife.io

1. Select this app when building a pipeline/process on Brainlife.io.
2. Provide an EGI `.raw` file for the `egi` input.
3. Optionally set EOG/ECG/MISC channels, bad channels, included trigger channels, flat-channel removal, and the events-as-annotations switch; otherwise the defaults above are used.
4. Submit the process. The converted `.fif` file, QC report and PSD figure are written to the process's output directories.

### Local Testing

```bash
git clone <this-repo>
cd egi2mne
# create config.json with the input file path and any parameters, e.g.:
# {"egi": "path/to/data.raw"}
./main
```

## Technical Details

- Execution: Singularity container with the `brainlifemeeg/mne:1.12.1` Docker image
- Format conversion: EGI `.raw` → MNE `.fif` via `mne.io.read_raw_egi`
- Channel typing: EOG/ECG/MISC assignment and bad-channel marking during conversion
- Report generation: `mne.Report` object for quality control

## Authors

- [Guiomar Niso](https://github.com/guiomar), Instituto Cajal, CSIC, Spain
- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2

Gramfort, A. et al. MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7, 267 (2013). https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
