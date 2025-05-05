# Author: Francesco G. Barone, PhD

# Affiliation: Biochemistry Section, Surgical Neurology Branch, National Institute of Neurological Disorders and Stroke, NIH, Bethesda, MD, USA

# Email: baronefg@nih.gov

This archive contains the BioClusterQuant v1.0.0 software package submitted to Zenodo.
Structure:
- BioClusterQuant.py ........ Main pipeline script for NND analysis
- Make_synthetic_roi.py .. Optional script to generate synthetic benchmark images (optional)
- LICENSE.txt ............ MIT license
- requirements.txt ....... List of required Python packages for BioClusterQuant
- README.txt ............. This file
- requirements_synthetic.txt ....... List of required Python packages for Make_synthetic_roi.py (optional)
- README_synthetic.txt (optional)
- Fiji_Preprocessing_Guide.txt .... Short Guide about input (optional)
- Supplementary resources such as: example synthetic images, centroid export csv and BioClusterQuant NND analysis.

# BioClusterQuant

**BioClusterQuant** is a Python tool for quantifying intracellular puncta clustering from centroid coordinates exported by ImageJ/Fiji or similar segmentation workflows.  
It outputs both the mean nearest-neighbour distance (**Avg_NND**) and its inverse (**Avg_Inverse_NND**) at single-cell resolution and can be used via a graphical interface or command line.

-----------------------------------------------------------------------------------------------

## Features

* Batch analysis of single ROI `.csv` files  
* GUI built with magicgui (no coding required)   
* Timestamped summary `.csv` output  
* Cross-platform, MIT-licensed, Python 3.9+

-----------------------------------------------------------------------------------------------

## Installation and Launch GUI

### 1. Create and activate a virtual environment

# On MacOS/Linux:

```bash
python3 -m venv test_env
source test_env/bin/activate
```

# On Windows (Powershell)

python -m venv test_env
test_env\Scripts\Activate.ps1

# Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

## Launch - Graphical User Interface (GUI)

```bash
python BioClusterQuant.py   # launch GUI, select ROI folder, batch analysis, save summary
```