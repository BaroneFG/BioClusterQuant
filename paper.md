---
title: 'BioClusterQuant: a GUI-based Python tool for quantifying intracellular puncta clustering from centroid coordinates'
tags:
  - Python
  - microscopy
  - image analysis
  - spatial statistics
  - nearest-neighbor distance
authors:
  - name: Francesco G. Barone
    orcid: 0000-0003-4382-9313
    affiliation: 1
affiliations:
 - index: 1
   name: National Institute of Neurological Disorders and Stroke, National Institutes of Health, Bethesda, MD, USA

date: 04 February 2026
bibliography: paper.bib
---

# Summary

**BioClusterQuant** is an open-source Python tool designed to quantify the spatial clustering of intracellular structures (puncta) from fluorescence microscopy data. It functions as a post-processing pipeline that takes centroid coordinates exported from image segmentation software (such as Fiji/ImageJ) and computes spatial metrics—specifically Nearest Neighbor Distance (NND) and its inverse—to assess the degree of clustering at the single-cell level. The tool features a graphical user interface (GUI) built with `magicgui` [@magicgui], allowing researchers without programming experience to perform reproducible batch analysis on large datasets.

# Statement of Need

The spatial organization of intracellular organelles and protein complexes is a critical readout in cell biology, yet standard analysis often stops at object counting. In processes such as autophagy or immune signaling, proteins redistribute into specific spatial configurations that are difficult to quantify manually [@Mizushima:2020].

**BioClusterQuant** is designed for researchers who need to rigorously quantify these spatial phenotypes but lack the programming expertise to write custom spatial statistics scripts. While standard platforms like Fiji [@Schindelin:2012] excel at segmentation, they often lack streamlined, automated workflows for batch-calculating spatial relationships across experimental conditions. This tool bridges that gap, solving the problem of "batch processing spatial data" by providing a platform-agnostic, reproducible workflow for NND quantification.

# State of the Field

Currently, researchers aiming to quantify puncta clustering face a dichotomy of tools:

1.  **Fiji/ImageJ:** While excellent for segmentation, standard Fiji distributions often require complex macro scripting to batch-calculate NND metrics across multiple cells, which can be brittle and difficult to share [@Schindelin:2012].
2.  **Advanced Profiling Tools:** Ecosystems like CellProfiler [@Carpenter:2006] or specialized spatial statistics packages (e.g., `spatstat` in R [@Baddeley:2005]) offer powerful metrics but represent more general frameworks. These often require significant pipeline configuration and scripting, which can be a barrier for users seeking a focused clustering solution.
3.  **Custom Scripts:** Many labs write one-off Python or MATLAB scripts for specific papers. These are rarely documented, packaged, or equipped with a GUI, making them inaccessible to the wider community.

**BioClusterQuant** fills this niche by offering a dedicated, lightweight GUI specifically for NND analysis. We chose to build a standalone tool rather than contributing a script to a larger library to prioritize usability for non-coders. It allows users to maintain their existing segmentation workflows (in Fiji) while offloading the spatial calculation to a reproducible, version-controlled Python environment.

# Software Design

The design of **BioClusterQuant** prioritizes **modularity** and **accessibility**. We made specific architectural choices to ensure the tool is lightweight and robust:

* **Decoupled Architecture:** By accepting simple `.csv` centroid inputs rather than raw images, we decoupled the potentially subjective step of segmentation from the objective step of quantification. This makes the tool compatible with any upstream segmentation software that exports coordinates.
* **Vectorized Computation:** Internally, the tool uses `scikit-learn`'s `NearestNeighbors` algorithm (BallTree or KDTree) [@scikit-learn] to compute distances. This is significantly faster and more memory-efficient than naive pairwise distance calculations, enabling scalable processing of high-content screening datasets.
* **Defined Outputs:** The tool outputs a summary CSV file containing per-ROI metrics including Mean NND, Mean Inverse NND ($1/NND$), and Puncta Count. It robustly handles edge cases; for example, ROIs containing fewer than two puncta (where NND is undefined) are automatically flagged and returned as `NaN` to prevent statistical skewing.
* **Minimalist GUI:** We utilized `magicgui` to auto-generate the interface from type-hinted Python functions. BioClusterQuant can be installed via standard Python tooling (`pip install -r requirements.txt`) and run locally following the usage instructions in the repository.

![Schematic of the BioClusterQuant analysis pipeline. (A-D) Preprocessing stage where centroid coordinates are extracted from microscopy images using standard segmentation tools. (E-G) Batch processing stage via the BioClusterQuant GUI. (H-I) Conceptual definition of the Nearest Neighbor Distance (NND) metric.](figures/fig1_schematic.png)

# Research Impact Statement

**BioClusterQuant** has been evaluated using synthetic benchmarking and demonstrated on an example microscopy dataset.

1.  **Benchmarking:** We tested the tool's accuracy using synthetic datasets with known spatial distributions (Figure 2). The software correctly discriminated between random dispersion, dense clustering, and edge cases (e.g., equidistant pairs), demonstrating it provides a consistent metric for spatial organization.
2.  **Applicability to Live-Cell Imaging:** We applied the tool to a time-lapse microscopy dataset (STING activation as an example perturbation) [@Fischer:2020] to demonstrate its utility on experimental data. The software processed the centroid data exported from these live-cell images and captured time-dependent changes in clustering metrics over a 5-hour time course (Figure 3).
3.  **Reproducibility:** The tool enables the standardization of clustering analysis. By providing a fixed, versioned algorithm for NND calculation, it removes the variability of manual analysis, directly supporting the reproducibility goals of the microscopy community.

![Evaluation of BioClusterQuant using synthetic 2D spatial distributions. (A-G) Synthetic images generated to model distinct puncta arrangements. (H-I) Quantification of Mean NND and Mean Inverse NND metrics across conditions. The software accurately distinguishes between random, dispersed, and clustered patterns.](figures/fig2_benchmark.png)

![Example application on a time-lapse microscopy dataset. (A) Representative images of HeLa cells expressing mEGFP-LC3B following a perturbation in a time-lapse experiment. (B-C) BioClusterQuant analysis captures the time-dependent decrease in Mean NND and increase in Mean Inverse NND per cell, demonstrating the tool's ability to quantify dynamic spatial phenotypes in experimental data.](figures/fig3_livecell.png)

# AI Usage Disclosure

No generative AI tools were used to write the manuscript text, generate figures, or develop the software.

# Acknowledgements

This work was supported by the Intramural Research Program (IRP) of the National Institute of Neurological Disorders and Stroke (NINDS). We acknowledge the support of the NHLBI Flow Cytometry Core and the NINDS Light Microscopy Core.

# References
