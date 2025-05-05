"""
A Python GUI application for batch calculation of NND metrics using Fiji/ImageJ ROI centroid CSVs

This script provides a GUI using magicgui. Users select a folder
containing individual CSV files exported from Fiji's Analyze Particles
(one CSV per ROI, expected columns: 'X', 'Y', and optionally 'Label').

The script calculates the average Nearest Neighbor Distance (Avg_NND) and
the average Inverse NND (Avg_Inverse_NND, representing clusterization)
for the centroids within each input CSV file (Single Cell/ROI).

It saves a summary CSV file (including the original Label, calculated
metrics, and foci/vescicle count per ROI) into the selected input folder. The
output filename includes a timestamp to prevent overwriting.

Author:     Francesco G. Barone, PhD
Date:       2025-04-17
Version:    1.0.0
License: MIT License
"""

import magicgui
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import glob
from pathlib import Path
import traceback
import datetime  # Added for timestamp output CSV

X_COL = "X"  # Expected X coordinate column name in input CSV
Y_COL = "Y"  # Expected Y coordinate column name in input CSV
LABEL_COL_INPUT = "Label"  # Expected Label column name in input CSV from Fiji
EPSILON = 1e-9
# Define output column names
OUT_ID_COL = "Identifier"  # Derived from input filename stem
OUT_LABEL_COL = "Label"  # Copied from input Fiji Label column
OUT_AVG_NND_COL = "Avg_NND"
OUT_AVG_INV_NND_COL = "Avg_Inverse_NND"  # Clusterization Score
OUT_NUMFOCI_COL = "NumFoci"


def calculate_nnd_metrics_for_cell(df_cell_foci):
    """
    Calculates NND metrics for foci within a single cell's DataFrame.
    Returns (average_nnd, average_inverse_nnd, num_foci)
    Returns NaN for metrics if n_foci < 2.
    """
    coords = df_cell_foci[[X_COL, Y_COL]].values
    n_foci = len(coords)

    if n_foci == 1:
        return np.nan, np.nan, 1  # Return NaN for NND metrics if only 1 foci/punctum
    elif n_foci >= 2:
        avg_nnd = np.nan  # Initialize as NaN
        avg_inv_nnd = np.nan  # Initialize as NaN
        try:
            nbrs = NearestNeighbors(n_neighbors=2, algorithm="ball_tree").fit(coords)
            distances, _ = nbrs.kneighbors(coords)
            nnds = distances[:, 1]
            avg_nnd = np.mean(nnds)
            # Calculate inverse NND (1/NND)
            nnds_no_zero = np.maximum(
                nnds, EPSILON
            )  # Avoid division by zero if NND is somehow 0
            inverse_nnds = 1.0 / nnds_no_zero
            avg_inv_nnd = np.mean(inverse_nnds)
        except Exception as e:
            print(f"      Error calculating NND for {n_foci} foci: {e}")
            # Keep avg_nnd and avg_inv_nnd as NaN if error occurs
            pass  # Already initialized to NaN
        return avg_nnd, avg_inv_nnd, n_foci
    else:  # n_foci == 0
        return np.nan, np.nan, 0


# --- magicgui Widget Definition ---
@magicgui.magicgui(
    input_folder={"mode": "d", "label": "Input Folder (ROI CSVs):"},
    call_button="Run Analysis and Save NND Summary",
)
def process_folder_gui(input_folder: Path = Path(".")):
    """GUI function to select folder, run NND analysis, and save results."""
    # Use a Label widget for status messages within the GUI
    status_label = getattr(process_folder_gui, "_status_label", None)
    if status_label is None:
        status_label = magicgui.widgets.Label(value="Status: Idle")
        process_folder_gui.insert(1, status_label)
        process_folder_gui._status_label = status_label
    else:
        status_label.value = "Status: Idle"

    if not input_folder or not input_folder.is_dir():
        status_label.value = "Error: Please select a valid input folder."
        print("Error: Please select a valid input folder.")
        return

    # Add timestamp to output filename
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    output_filename = f"NND_Summary_Results_{timestamp}.csv"
    output_csv = input_folder / output_filename

    status_label.value = f"Processing folder: {input_folder.name}..."
    print(f"Input folder: {input_folder}")
    print(f"Output file will be: {output_csv}")

    search_path = str(input_folder / "*.csv")
    csv_files = sorted(glob.glob(search_path))

    if not csv_files:
        status_label.value = "Error: No CSV files found in folder."
        print(f"Error: No CSV files found in '{input_folder}'.")
        return

    print(f"Found {len(csv_files)} CSV files to process.")
    all_results = []
    processed_count = 0

    for filepath in csv_files:
        p = Path(filepath)
        filename = p.name
        identifier = p.stem  # Filename without extension

        # Skip any previously generated output files
        if filename.startswith("NND_Summary_Results_"):
            print(f"  Skipping potential previous output file: {filename}")
            continue

        print(f"  Processing: {filename}  (ID: {identifier})")

        try:
            df_foci = pd.read_csv(filepath)

            if X_COL not in df_foci.columns or Y_COL not in df_foci.columns:
                print(
                    f"      WARNING: Skipping {filename} - Missing '{X_COL}' or '{Y_COL}'."
                )
                continue

            # Extract Label column
            label_value = "N/A"  # Default if column missing or empty
            if (
                LABEL_COL_INPUT
                and LABEL_COL_INPUT in df_foci.columns
                and not df_foci.empty
            ):
                # Assume label is constant for the file, take from first row
                label_value = df_foci[LABEL_COL_INPUT].iloc[0]
            elif LABEL_COL_INPUT:
                # Only warn if the column was expected but not found/empty
                print(
                    f"      WARNING: Label column '{LABEL_COL_INPUT}' not found or file empty in {filename}."
                )

            if len(df_foci) < 1:
                num_foci = 0
                avg_nnd = np.nan  # Use NaN if 0 foci
                avg_inv_nnd = np.nan  # Use NaN if 0 foci
            else:
                avg_nnd, avg_inv_nnd, num_foci = calculate_nnd_metrics_for_cell(df_foci)

            # Add results to list
            all_results.append(
                {
                    OUT_ID_COL: identifier,
                    OUT_LABEL_COL: label_value,
                    OUT_AVG_NND_COL: avg_nnd,
                    OUT_AVG_INV_NND_COL: avg_inv_nnd,
                    OUT_NUMFOCI_COL: num_foci,
                }
            )
            processed_count += 1

        except pd.errors.EmptyDataError:
            print(f"      WARNING: Skipping empty file {filename}.")
            all_results.append(
                {
                    OUT_ID_COL: identifier,
                    OUT_LABEL_COL: "Empty File",
                    OUT_AVG_NND_COL: np.nan,  # Use NaN for consistency
                    OUT_AVG_INV_NND_COL: np.nan,  # Use NaN for consistency
                    OUT_NUMFOCI_COL: 0,
                }
            )
        except Exception as e:
            print(f"      ERROR processing file {filename}: {e}")
            traceback.print_exc()
            # General errors already use NaN, which is good
            all_results.append(
                {
                    OUT_ID_COL: identifier,
                    OUT_LABEL_COL: "Processing Error",
                    OUT_AVG_NND_COL: np.nan,
                    OUT_AVG_INV_NND_COL: np.nan,
                    OUT_NUMFOCI_COL: -1,  # Use -1 to indicate error vs 0 foci
                }
            )

    if not all_results:
        status_label.value = "Finished: No results generated."
        print("No results were generated.")
        return

    results_df = pd.DataFrame(all_results)
    # Update column order for output
    final_columns = [
        OUT_ID_COL,
        OUT_LABEL_COL,
        OUT_AVG_NND_COL,
        OUT_AVG_INV_NND_COL,
        OUT_NUMFOCI_COL,
    ]
    # Ensure columns exist before reordering, handle potential errors during processing
    results_df = results_df.reindex(columns=final_columns)

    print(
        f"\nSaving summary results ({processed_count} files processed) to: {output_csv}"
    )
    try:
        # Save with NaN representation recognized by most software
        results_df.to_csv(output_csv, index=False, float_format="%.5f", na_rep="NaN")
        status_label.value = f"Success! Results saved ({processed_count} files):\n{output_filename}"  # Show filename in GUI status
        print("Summary saved successfully.")
    except Exception as e:
        status_label.value = "Error saving results!"
        print(f"ERROR saving results CSV '{output_csv}': {e}")
        traceback.print_exc()


if __name__ == "__main__":
    print("Launching BioClusterQuant GUI...")
    # Create and show the GUI. run=True makes the script wait until the GUI is closed.
    process_folder_gui.native.setWindowTitle("BioClusterQuant v1.0.0")
    process_folder_gui.show(run=True)
    print("BioClusterQuant GUI closed.")
