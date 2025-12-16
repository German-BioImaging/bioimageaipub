import os
import json
import shutil
import logging
from random import random
from pathlib import Path, PurePath

import cv2
import numpy as np
from bioio import BioImage


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_for_png(arr: np.ndarray):
    """Prepare image array for saving as PNG using OpenCV."""
    arr = np.asarray(arr).transpose((1, 0, 2))  # Transpose to Height x Width x Channel dimension order (for OpenCV)
    arr = arr.astype(np.uint16, copy=False)  # Ensure data is 16-bit depth

    normalized_image = cv2.normalize(
        arr, None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)  # Normalize image dynamic range for better visibility  # noqa

    cv2.cvtColor(normalized_image, cv2.COLOR_BGR2RGB, normalized_image)  # Convert from RGB to BGR color space for OpenCV  # noqa

    return normalized_image


def convert_zarr(root_data_path: Path, converted_data_path: Path, zarr_file_list: str, output_format: str = "png"):
    """Convert Zarr files to PNG images for accessibility."""
    with open(zarr_file_list, "r") as f:
        zarr_rel_paths = [line.strip() for line in f.readlines()]
        for zarr_rel_path in zarr_rel_paths:
            zarr_path = os.path.join(root_data_path, zarr_rel_path)
            zattrs_json = json.load(open(os.path.join(zarr_path, ".zattrs"), "r"))
            for well_json in zattrs_json["plate"]["wells"]:
                well_path = well_json["path"]
                well_zattrs = json.load(open(os.path.join(zarr_path, well_path, ".zattrs"), "r"))
                for image_json in well_zattrs["well"]["images"]:
                    image_path = image_json["path"]
                    img_zarr_path = os.path.join(zarr_path, well_path, image_path + ".zarr")
                    logger.info("Creating " + img_zarr_path)
                    shutil.copytree(
                        os.path.join(zarr_path, well_path, image_path), img_zarr_path, dirs_exist_ok=True
                    )
                    img = BioImage(img_zarr_path)
                    img.set_resolution_level(0)
                    img_rgb = img.get_image_data("XYC")

                    normalized_image = prepare_for_png(img_rgb)

                    output_png_path = converted_data_path / zarr_rel_path.replace(".zarr", "") / well_path \
                        / (image_path + f".{output_format}")
                    logger.info("Saving " + str(output_png_path))
                    Path(output_png_path).parent.mkdir(parents=True, exist_ok=True)
                    cv2.imwrite(str(output_png_path), normalized_image)

                    # copy Zarr metadata over

            shutil.copy(
                os.path.join(zarr_path, ".zattrs"), os.path.join(output_png_path.parent.parent.parent, ".zattrs")
            )


def split_into_folders(target: Path, max_files: int) -> None:
    """Split files in target directory into subfolders with a maximum number of files each."""
    folder_index = 1
    files_in_current = 0

    # Create first folder
    current_folder = target / f"folder{folder_index}"
    current_folder.mkdir(exist_ok=True)

    # Iterate over items directly in target_dir
    for entry in sorted(target.iterdir()):
        # skip directories (including folder1, folder2, ...)
        if entry.is_dir():
            continue

        # move file into current folder
        dest = current_folder / entry.name
        shutil.move(str(entry), str(dest))
        files_in_current += 1

        # if current folder is full, start a new one
        if files_in_current >= max_files:
            folder_index += 1
            current_folder = target / f"folder{folder_index}"
            current_folder.mkdir(exist_ok=True)
            files_in_current = 0


def zarr_name_to_plate_name(converted_data_path: str) -> dict:
    """Map Zarr hash names from AWS S3 to plate names and save the mapping."""
    zarr_dirs = [converted_data_path / d for d in os.listdir(converted_data_path)]
    zarr_hash_plate_mapping = {}
    os.makedirs(f"{converted_data_path}/metadata/", exist_ok=True)

    for i in range(len(zarr_dirs)):
        hash_filepath = zarr_dirs[i]
        zarr_name = PurePath(hash_filepath).name
        with open(f"{hash_filepath}/{zarr_name}/.zattrs") as f:
            zattrs = json.load(f)
            print(f"Hashtag {zarr_name} - IDR Plate {zattrs['plate']['name']}")
            zarr_hash_plate_mapping[zarr_name] = zattrs['plate']['name']

    return zarr_hash_plate_mapping


def test_train_split(converted_data_path: str, train_split_ratio: float = 0.8, zarr_hash_plate_mapping: dict = {}):
    zarr_dirs = [converted_data_path / d for d in os.listdir(converted_data_path)]

    for i in range(len(zarr_dirs)):
        hash_filepath = zarr_dirs[i]
        zarr_name = PurePath(hash_filepath).name
        zattrs = {}
        with open(f"{hash_filepath}/{zarr_name}/.zattrs") as f:
            zattrs = json.load(f)
        field_count = zattrs["plate"]["field_count"]
        os.makedirs(f"{converted_data_path}/train/", exist_ok=True)
        os.makedirs(f"{converted_data_path}/test/", exist_ok=True)
        for well_info in zattrs['plate']['wells']:
            well_path = well_info['path']
            for field_idx in range(field_count):
                if os.path.exists(f"{hash_filepath}/{zarr_name}/{well_path}/{field_idx}.png"):
                    well_path_clean = well_path.replace("/", "")

                    # TODO: Need to double check the logic below?
                    if random() < train_split_ratio:
                        os.rename(f"{hash_filepath}/{zarr_name}/{well_path}/{field_idx}.png",
                    f"{converted_data_path}/train/{zarr_hash_plate_mapping[zarr_name]}_{well_path_clean}_{field_idx}.png")
                    else:
                        os.rename(f"{hash_filepath}/{zarr_name}/{well_path}/{field_idx}.png",
                    f"{converted_data_path}/test/{zarr_hash_plate_mapping[zarr_name]}_{well_path_clean}_{field_idx}.png")
