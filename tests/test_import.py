import sys
from pathlib import Path

# Get the repository root directory (parent of 'tests')
REPO_ROOT = Path(__file__).resolve().parents[1]

# Add the repo root to sys.path so Python can find 'BioClusterQuant.py'
sys.path.insert(0, str(REPO_ROOT))

def test_import_main_module():
    """
    Tries to import the main module. 
    If this fails, pytest will automatically mark it as failed.
    """
    import BioClusterQuant
