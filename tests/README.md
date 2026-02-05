# BioClusterQuant Automated Tests

This directory contains automated tests to verify the installation and stability of the software.

## Files
* `test_import.py`: A minimal sanity check that verifies the software environment is correctly configured and that `BioClusterQuant` can be imported without errors.

## How to Run Manually
If you want to run these tests locally, install `pytest` and run:

```bash
pip install pytest
pytest tests/test_import.py
