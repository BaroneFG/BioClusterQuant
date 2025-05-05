"""
Generates synthetic, spatially calibrated TIFF images of puncta patterns
(clusters, random, etc.) for software testing purposes.

Author:     Francesco G. Barone, PhD
Date:       2025-04-17
Version:    1.0.0
License: MIT License
"""

import numpy as np
from pathlib import Path
import os
from skimage import draw 
import tifffile 
import traceback

print("Script starting...")


OUTPUT_FOLDER_NAME = "synthetic_images_calibrated"
NUM_REPLICATES = 10
IMAGE_WIDTH = 256  # Image width in pixels
IMAGE_HEIGHT = 256  # Image height in pixels


PIXEL_SIZE_UM = 0.04  # Microns per pixel


PUNCTA_RADIUS_PIXELS = 2  # Radius of drawn disks (puncta) in pixels
PUNCTA_INTENSITY = 255  # Intensity value for puncta (white)
BACKGROUND_INTENSITY = 0  # Intensity value for background (black)
IMAGE_DTYPE = np.uint8  # Data type for image (8-bit)

# Pattern parameters (These define distances/spreads in PIXEL units)
NUM_POINTS_CLUSTER = 50
DISTANCE_CLOSE = float(PUNCTA_RADIUS_PIXELS * 2)  # e.g., 4.0 pixels
CLUSTER_CENTER = (IMAGE_HEIGHT / 2, IMAGE_WIDTH / 2)  # Y, X center in pixels
STD_DEV_DISPERSED = float(IMAGE_WIDTH / 5)  # Std Dev in pixels
STD_DEV_MIDDLE = float(IMAGE_WIDTH / 10)  # Std Dev in pixels
STD_DEV_CONDENSED = float(IMAGE_WIDTH / 30)  # Std Dev in pixels
NUM_POINTS_RANDOM = 50


def generate_cluster_coords(img_shape, num_points, center, std_dev):
    """Generates points from a 2D Gaussian distribution, clipped to box."""
    coords = np.random.normal(loc=center, scale=std_dev, size=(num_points, 2))
    coords[:, 0] = np.clip(
        coords[:, 0], PUNCTA_RADIUS_PIXELS, img_shape[0] - 1 - PUNCTA_RADIUS_PIXELS
    )  # Y
    coords[:, 1] = np.clip(
        coords[:, 1], PUNCTA_RADIUS_PIXELS, img_shape[1] - 1 - PUNCTA_RADIUS_PIXELS
    )  # X
    return coords.astype(int)


def generate_two_points_fixed_distance(img_shape, distance_pixels):
    """Generates two points separated by a specific fixed pixel distance near the center."""
    center_y, center_x = img_shape[0] / 2, img_shape[1] / 2
    p1_x = center_x - distance_pixels / 2
    p2_x = center_x + distance_pixels / 2
    p1_y = center_y
    p2_y = center_y
    coords = np.array([[p1_y, p1_x], [p2_y, p2_x]])
    coords[:, 0] = np.clip(
        coords[:, 0], PUNCTA_RADIUS_PIXELS, img_shape[0] - 1 - PUNCTA_RADIUS_PIXELS
    )
    coords[:, 1] = np.clip(
        coords[:, 1], PUNCTA_RADIUS_PIXELS, img_shape[1] - 1 - PUNCTA_RADIUS_PIXELS
    )
    return coords.astype(int)


def generate_single_point_coords(img_shape):
    """Generates a single point at a random pixel location."""
    min_y, max_y = PUNCTA_RADIUS_PIXELS, img_shape[0] - 1 - PUNCTA_RADIUS_PIXELS
    min_x, max_x = PUNCTA_RADIUS_PIXELS, img_shape[1] - 1 - PUNCTA_RADIUS_PIXELS
    coords = np.random.rand(1, 2)
    coords[:, 0] = coords[:, 0] * (max_y - min_y) + min_y  # Scale Y
    coords[:, 1] = coords[:, 1] * (max_x - min_x) + min_x  # Scale X
    return coords.astype(int)


def generate_random_coords(img_shape, num_points):
    """Generates points randomly within the box (pixel coordinates)."""
    min_y, max_y = PUNCTA_RADIUS_PIXELS, img_shape[0] - 1 - PUNCTA_RADIUS_PIXELS
    min_x, max_x = PUNCTA_RADIUS_PIXELS, img_shape[1] - 1 - PUNCTA_RADIUS_PIXELS
    coords = np.random.rand(num_points, 2)
    coords[:, 0] = coords[:, 0] * (max_y - min_y) + min_y  # Y
    coords[:, 1] = coords[:, 1] * (max_x - min_x) + min_x  # X
    return coords.astype(int)


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = Path(OUTPUT_FOLDER_NAME)
    output_dir.mkdir(exist_ok=True)
    print(f"Outputting synthetic TIFF images to folder: {output_dir.resolve()}")

    img_shape = (IMAGE_HEIGHT, IMAGE_WIDTH)

    # Define the conditions and their corresponding generator functions
    conditions = {
        "SinglePoint": lambda: generate_single_point_coords(img_shape),
        "TwoFar": lambda: generate_random_coords(img_shape, 2),
        "TwoClose": lambda: generate_two_points_fixed_distance(
            img_shape, DISTANCE_CLOSE
        ),
        "Random": lambda: generate_random_coords(img_shape, NUM_POINTS_RANDOM),
        "DispersedCluster": lambda: generate_cluster_coords(
            img_shape, NUM_POINTS_CLUSTER, CLUSTER_CENTER, STD_DEV_DISPERSED
        ),
        "MiddleCluster": lambda: generate_cluster_coords(
            img_shape, NUM_POINTS_CLUSTER, CLUSTER_CENTER, STD_DEV_MIDDLE
        ),
        "CondensedCluster": lambda: generate_cluster_coords(
            img_shape, NUM_POINTS_CLUSTER, CLUSTER_CENTER, STD_DEV_CONDENSED
        ),
    }

    resolution_xy = 1.0 / PIXEL_SIZE_UM  # Pixels per micron
    resolution_unit = "micron"  # Unit for metadata

    # Loop through conditions and replicates
    for name, generator_func in conditions.items():
        print(f"Generating condition: {name}")
        for i in range(1, NUM_REPLICATES + 1):
            image = np.full(img_shape, BACKGROUND_INTENSITY, dtype=IMAGE_DTYPE)
            coords_yx = generator_func()
            for y, x in coords_yx:
                rr, cc = draw.disk(
                    (y, x), radius=PUNCTA_RADIUS_PIXELS, shape=image.shape
                )
                image[rr, cc] = PUNCTA_INTENSITY

            filename = f"{name}_Rep{i}.tif"
            output_path = output_dir / filename
            try:
                # --- Save TIFF with spatial calibration metadata ---
                tifffile.imwrite(
                    output_path,
                    image,
                    imagej=True,  # Helps Fiji read basic metadata
                    resolution=(
                        resolution_xy,
                        resolution_xy,
                    ),  # Xres, Yres (pixels per unit)
                    metadata={
                        "unit": resolution_unit
                    },  # Set unit explicitly for ImageJ/Fiji
                )
                # print(f"  Saved: {filename}")
            except Exception as e:
                print(f"  ERROR saving {filename}: {e}")
                traceback.print_exc()

    print(f"\nSynthetic image generation complete in folder '{OUTPUT_FOLDER_NAME}'.")
    print(f"Images saved with pixel size: {PIXEL_SIZE_UM} {resolution_unit}/pixel")
