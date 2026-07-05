import pytest
import os
import json
import subprocess
import shutil

# ==============================================================================
# 🎛️ PART 1: CONFIGURATION AND SCENARIOS (Modify according to application)
# ==============================================================================


DATASET_TEST = "tests/datasets/eeg" 


BASE_CONFIG = {
    "eog": "None",
    "ecg": "None",
    "bads": "None",
    "include": "None",
    "misc": "None",
    "rm_flat": True,
    "events_as_annotations": True
}

# SCENARIOS: Write the parameters you want to modify
# Format: ("Scenario name", {modifications_dict}, should_succeed_bool)
SCENARIOS = [
    (
        "1. Vanilla Execution (All defaults)", 
        {},  # Empty dict: keep 100% of BASE_CONFIG
        True
    ),
    (
        "2. Channel Exclusion (Bads)", 
        {"bads": "D101,D102"}, # Overrides only the "bads" key
        True
    ),
    (
        "3. Complex Combination (Include + Rm_flat disabled)", 
        {
            "include": "DIN1,DIN2", 
            "rm_flat": False
        }, 
        True
    ),
    (
        "4. Security Test (Negative testing on non-existent channel)", 
        {"include": "INVALID_CHANNEL"}, 
        False # MNE should crash, test is successful if exit code is not 0
    )
]

# ==============================================================================
# ⚙️ PART 2: THE UNIVERSAL BRAINLIFE ENGINE (Never change)
# ==============================================================================


@pytest.fixture
def dataset():
    """Verifies the presence of the source file before running the test suite."""
    if not os.path.exists(DATASET_TEST):
        pytest.skip(f"File '{DATASET_TEST}' missing. Test skipped.")
    return DATASET_TEST

def cleanup():
    """Cleans up the workspace to prevent pollution between scenarios."""
    for item in ['config.json', 'out_dir', 'product.json']:
        if os.path.exists(item):
            shutil.rmtree(item) if os.path.isdir(item) else os.remove(item)

@pytest.mark.parametrize("test_name, scenario_modifications, should_succeed", SCENARIOS)
def test_dynamic_application(dataset, test_name, scenario_modifications, should_succeed):
    """Test engine that merges the base and scenario, then simulates BrainLife."""
    # 1. Prepare a clean workspace
    cleanup()

    # 2. Merge (Base + Scenario Override)
    final_config = {"egi": dataset}
    final_config.update(BASE_CONFIG)   # Add all default values
    final_config.update(scenario_modifications)  # Override with scenario values
    
    # 3. Generate the configuration file expected by BrainLife
    with open('config.json', 'w') as f:
        json.dump(final_config, f)

    # Simulate BrainLife: create the expected output folder
    os.makedirs('out_dir', exist_ok=True)

    # 4. Run the application as a black box
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    
    # 5. Assertions according to platform standards
    if should_succeed:
        assert result.returncode == 0, f"Unexpected crash ({test_name}):\n{result.stderr}"
        assert os.path.exists(os.path.join('out_dir', 'raw.fif')), "File raw.fif missing."
        assert os.path.exists('product.json'), "File product.json missing."
    else:
        assert result.returncode != 0, f"Application should have crashed ({test_name})."

    # 6. Final cleanup
    cleanup()