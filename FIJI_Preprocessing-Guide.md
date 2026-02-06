# Fiji Preprocessing Guide for BioClusterQuant

This guide explains how to preprocess fluorescence microscopy images in Fiji to extract centroid coordinates for input into **BioClusterQuant**.

## Requirements
- Fiji (ImageJ distribution)
- Input image channel where high-intensity puncta are visible
- Manually selected ROIs corresponding to individual cells (optional but recommended)

## Steps

1. **Import your fluorescence image** in Fiji.
   - `File > Import > Bio-Formats`

2. **Set Measurements** (Only needed the first time).
   - Go to `Analyze > Set Measurements...`
   - Check **Centroid** (For X, Y coordinates).
   - Check **Display label** (to track label IDs in `BioClusterQuant.py`).

3. **(Optional) Use the ROI Manager**.
   - Use the freehand selection tools to select a single cell.
   - Add the ROI to the ROI Manager (`Analyze > Tools > ROI Manager > Add` or press `T`).

4. **Apply an intensity threshold** to isolate puncta.
   - `Image > Adjust > Threshold...`
   - Choose a suitable thresholding method (e.g., Otsu, or manually based on high puncta intensity control group).

5. **Run particle detection**.
   - `Analyze > Analyze Particles...`
   - Check the following boxes:
     - "Display results"
     - "Clear results"
     - "Add to Manager" (optional)
   - Set size and circularity filters if needed (e.g., 0.2-5.00 for size, 0.2-1.00 for circularity).

6. **Save the Results table**.
   - `File > Save As...`
   - Save the table as `.csv`.
   - **Tip:** Name the file with the ROI or image name (e.g., `cell1.csv`).

7. Repeat steps 3–6 for each ROI or cell.

8. **Prepare for BioClusterQuant**.
   - Place all `.csv` files into a single folder.
   - This folder will be selected as input when launching the BioClusterQuant GUI.

## Notes
- **Required columns:** `X`, `Y`
- **Optional column:** `Label` (e.g., time point, condition)

> Refer to the main documentation or example input files if unsure.
