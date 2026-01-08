"""
Convert EGI EEG files to MNE-Python raw format.

This app converts EGI .raw files to MNE-compatible .fif format using the 
mne.io.read_raw_egi function. It generates a report with channel information
and produces output raw data in the standard MNE format for downstream processing.

Input:
    - egi: Path to EGI .raw file
    - include: Optional comma-separated list of channels to include
    - bads: Optional comma-separated list of channels to mark as bad

Output:
    - out_dir/raw.fif: MNE raw data file
    - out_dir/report.html: QC report with channel information
    - product.json: Metadata with channel info and positions
"""

# Copyright (c) 2020 brainlife.io
#
# This app converts EGI EEG files to MNE raw format.
#
# Author: Guiomar Niso
# Indiana University

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne
import numpy as np

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir')

# Load configuration
config = load_config()

# == LOAD DATA ==
fname = config['egi']

# Parse included channels if specified
include_raw = config.get('include', '')
if include_raw and include_raw != 'None':
    include = [ch.strip() for ch in include_raw.split(',')]
else:
    include = None

# Read EGI raw data
raw = mne.io.read_raw_egi(fname, include=include)

# == MARK BAD CHANNELS ==
bads_raw = config.get('bads', '')
if bads_raw and bads_raw != 'None':
    bads = [ch.strip() for ch in bads_raw.split(',')]
    # Filter to only include channels that exist in the data
    bads = [ch for ch in bads if ch in raw.ch_names]
    if bads:
        raw.info['bads'] = bads

# == CREATE REPORT ==
report = mne.Report(title='EGI to MNE Conversion Report')
report.add_raw(raw=raw, title='Raw Data')

# Add channel information to report
channel_info_html = '<p><b>Channels in this EGI file:</b></p>' + ', '.join(raw.ch_names)
report.add_html(title='Channels', html=channel_info_html)

# == SAVE DATA ==
raw.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)
report.save(os.path.join('out_dir', 'report.html'), overwrite=True)

# == CREATE PRODUCT JSON ==
product_items = []

# Add raw info
info_msg = str(raw.info)
add_info_to_product(product_items, info_msg)

# Add bad channels information if any
if raw.info['bads']:
    bads_msg = f"Bad channels marked: {', '.join(raw.info['bads'])}"
    add_info_to_product(product_items, bads_msg)

# Add channel positions if available
positions = raw._get_channel_positions()
if positions is not None and np.any(~np.isnan(positions)):
    channel_positions_msg = "Channel positions:\n" + "\n".join(
        [f"{ch_name}: {pos.tolist()}" for ch_name, pos in zip(raw.ch_names, positions)]
    )
    add_info_to_product(product_items, channel_positions_msg)
else:
    add_info_to_product(product_items, f"Channels (no positions available): {', '.join(raw.ch_names)}")

create_product_json(product_items)
    
