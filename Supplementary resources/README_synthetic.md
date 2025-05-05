# Author: Francesco G. Barone, PhD

# Affiliation: Biochemistry Section, Surgical Neurology Branch, National Institute of Neurological Disorders and Stroke, NIH, Bethesda, MD, USA

# Email: baronefg@nih.gov

# Synthetic ROI Generator for BioClusterQuant

(OPTIONAL) - This Python script (`Make_synthetic_roi.py`) generates synthetic two-dimensional point distributions simulating puncta arrangements in microscopy images. It is designed for benchmarking the [BioClusterQuant.py] spatial clustering analysis tool. 

Note: These synthetic images are intended solely for testing image analysis software functionality.

## Features

- Generate predefined spatial patterns:
  - Single punctum
  - Two distant puncta
  - Random distribution
  - Dispersed cluster
  - Middle-density cluster
  - Condensed cluster
  - Two equidistant close puncta

## Requirements

Install dependencies using:

```bash
pip install -r requirements_synthetic.txt
```