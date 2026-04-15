"""
Convert EGI EEG files to MNE-Python raw format.

This app converts EGI .raw files to MNE-compatible .fif format using the 
mne.io.read_raw_egi function. It generates a report with channel information
and produces output raw data in the standard MNE format for downstream processing.

Input:
    - egi: Path to EGI .raw file
    - eog: Optional comma-separated list of channels to mark as EOG
    - misc: Optional comma-separated list of channels to mark as miscellaneous
    - include: Optional comma-separated list of channels to use to create
      synthetic trigger annotations.
    - bads: Optional comma-separated list of channels to mark as bad
    - events_as_annotations: If True, annotations are created from experiment events.
    If False, a synthetic trigger channel STI 014 is created from experiment events.

Output:
    - out_dir/raw.fif: MNE raw data file
    - out_report/report.html: QC report with channel information
    - out_figs/psd.png: Power Spectral Density plot
    - product.json: Metadata with channel info and positions
"""

# Copyright (c) 2026 brainlife.io
#
# This app converts EGI EEG files to MNE raw format.
#
# Authors:
# - Guiomar Niso (https://github.com/guiomar)
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne
import numpy as np
import matplotlib.pyplot as plt

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_report', 'out_figs')

# Load configuration
config = load_config()

# == LOAD DATA ==
fname = config['egi']
eog = config.get('eog', None)
if eog is not None:
    eog = [ch.strip() for ch in eog.split(',')]
else:
    eog = None
misc = config.get('misc', None)
if misc is not None:
    misc = [ch.strip() for ch in misc.split(',')]
else:
    misc = None

# Parse included channels if specified
include_raw = config.get('include', '')
if include_raw and include_raw != 'None':
    include = [ch.strip() for ch in include_raw.split(',')]
else:
    include = None

# Parse events_as_annotations if specified
events_as_annotations = config.get('events_as_annotations', True)

# Read EGI raw data
raw = mne.io.read_raw_egi(fname, eog=eog, misc=misc, include=include,
                          events_as_annotations=events_as_annotations)

already_bad = raw.info['bads']
if already_bad:
    print(f"Channels already marked as bad in the EGI file: {', '.join(already_bad)}")
       
# == MARK BAD CHANNELS ==
bads_raw = config.get('bads', '')
if bads_raw and bads_raw != 'None':
    bads = [ch.strip() for ch in bads_raw.split(',')]
    # Filter to only include channels that exist in the data
    bads = [ch for ch in bads if ch in raw.ch_names]
    if bads:
        raw.info['bads'].extend(bads)
        raw.info['bads'] = list(set(raw.info['bads']))  # Remove duplicates
        print(f"Newly marked as bads: {', '.join(bads)}")
else:
    bads = []


# == CREATE REPORT ==
report = mne.Report(title='EGI to MNE Conversion Report')
report.add_raw(raw=raw, title='Raw Data')

# Add channel information to report
channel_info_html = '<p><b>Channels in this EGI file:</b></p>' + ', '.join(raw.ch_names)
report.add_html(title='Channels', html=channel_info_html)

# == SAVE DATA ==
raw.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)
report.save(os.path.join('out_report', 'report.html'), overwrite=True)

# == CREATE PSD PLOT ==
fig = raw.compute_psd().plot(exclude='bads', show=False)
fig.savefig(os.path.join('out_figs', 'psd.png'), dpi=100, bbox_inches='tight')
plt.close(fig)

# == CREATE PRODUCT JSON ==
product_items = []

# Add structured raw info messages
add_raw_info_to_product(product_items, raw)

if include is not None:
    if events_as_annotations:
        included_channels_msg = f"Combined channels {', '.join(include)} into annotations."
        add_info_to_product(product_items, included_channels_msg, msg_type='success')
    else:
        if 'STI 014' not in raw.ch_names:
            include_channels_msg = f"Warning: 'STI 014' channel not found after including channels {', '.join(include)}."
            add_info_to_product(product_items, include_channels_msg, msg_type='error')
        else:
            included_channels_msg = f"Combined channels {', '.join(include)} to create synthetic trigger channel STI014."
            add_info_to_product(product_items, included_channels_msg, msg_type='success')

# Add bad channels information if any
if raw.info['bads']:
    already_bad_msg = f"Channels already marked as bad in the EGI file: {', '.join(already_bad)}" if already_bad else "No channels were marked as bad in the original EGI file."
    bads_msg = f"Bad channels marked: {', '.join(bads)}" if bads else "No additional bad channels marked from config."
    add_info_to_product(product_items, already_bad_msg, 'warning' if already_bad else 'info')
    add_info_to_product(product_items, bads_msg, 'info')
    final_bads_msg = f"Total bad channels marked: {', '.join(raw.info['bads'])}"
    add_info_to_product(product_items, final_bads_msg, 'success')

# Add channel positions if available
positions = raw._get_channel_positions()
if positions is not None and np.any(~np.isnan(positions)):
    channel_positions_msg = "Channel positions:\n" + "\n".join(
        [f"{ch_name}: {pos.tolist()}" for ch_name, pos in zip(raw.ch_names, positions)]
    )
    add_info_to_product(product_items, channel_positions_msg)
else:
    add_info_to_product(product_items, f"Channels (no positions available): {', '.join(raw.ch_names)}")

add_info_to_product(product_items, "Imported EGI .raw file and converted to MNE format successfully.", msg_type='success')

# Add PSD plot if it exists
psd_image_path = os.path.join('out_figs', 'psd.png')
if os.path.exists(psd_image_path):
    add_image_to_product(product_items, name='Power Spectral Density (PSD)', filepath=psd_image_path)

create_product_json(product_items)
    
