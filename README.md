<h1 align="center">EGI to mne/raw</h1>

<p align="center">
  Converts an EGI EEG .raw file to MNE-Python raw FIF format with mne.io.read_raw_egi, setting EOG/ECG/MISC channel types, bad channels and trigger events, with a QC report and PSD plot.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.742"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.742-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Converts an EGI EEG .raw file to MNE-Python raw FIF format with mne.io.read_raw_egi, setting EOG/ECG/MISC channel types, bad channels and trigger events, with a QC report and PSD plot.**

Reads the EGI recording, combines the listed stimulus channels into annotations or a synthetic STI 014 trigger channel, labels EOG/ECG/MISC channels, marks listed and (optionally) flat channels as bad, and writes raw.fif with an HTML report and a power spectral density figure. Use it as the import step for EGI (Geodesic) EEG data before MNE-based processing.

| | |
|---|---|
| **Inputs** | `neuro/eeg/egi` |
| **Outputs** | `neuro/meeg/mne/raw` |
| **Container** | `brainlifemeeg/mne:1.12.1` |
| **Resources** | 8 CPUs · 4 GB memory |
| **Run it** | [doi.org/10.25663/brainlife.app.742](https://doi.org/10.25663/brainlife.app.742) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `egi1` | `neuro/eeg/egi` | yes | EGI (Geodesic) EEG recording in .raw format. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | MNE Raw data in FIF format |

<details>
<summary><b>Parameters</b> (7)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `eog` | string |  | EOG channels if any. Default is None. |
| `ecg` | string |  | ECG channels if any. default is None. |
| `bads` | string |  | Bad channels (comma separated list). |
| `include` | string | `D101,D102,D103,D104,D105,D106,D107,D108,D109,D110,D111,D112,D201,D202,D203,D204,D205,D206,D207,D208,D209,D210,D211,D212,DIN1,DIN2` | Which stimulus channels to include (comma separated list). |
| `misc` | string |  | Names of channels or list of indices that should be designated MISC channels. Default is None. |
| `rm_flat` | boolean | `true` | Mark flat channels as bad if True (default). |
| `events_as_annotations` | boolean | `true` | If True, annotations are created from experiment events. If False, a synthetic trigger channel STI 014 is created from experiment events. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.742](https://doi.org/10.25663/brainlife.app.742), choose `neuro/eeg/egi` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/meeg/mne/raw`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlifemeeg/mne:1.12.1`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "egi": "/path/to/egi1/egi",
       "eog": "",
       "ecg": "",
       "bads": "",
       "include": "D101,D102,D103,D104,D105,D106,D107,D108,D109,D110,D111,D112,D201,D202,D203,D204,D205,D206,D207,D208,D209,D210,D211,D212,DIN1,DIN2",
       "misc": "",
       "rm_flat": true,
       "events_as_annotations": true
   }
   ```

3. Run `./main`.

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

## Local Testing

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

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- EGI to mne/raw. brainlife.io App. [doi:10.25663/brainlife.app.742](https://doi.org/10.25663/brainlife.app.742)
- Gramfort et al. MEG and EEG data analysis with MNE-Python. *Frontiers in Neuroscience* 7 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- [Guiomar Niso](https://github.com/guiomar), Instituto Cajal, CSIC, Spain
- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
