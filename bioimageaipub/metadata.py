import os
import re
import urllib
import subprocess
import BeautifulSoup
from typing import List, Optional

import pandas as pd


def flatten_extend(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list


def fetch_omero_metadata(omexcavator_src_dir: str) -> None:
    """Fetch OMERO metadata using omexcavator and save it to a JSON-LD file(s).
    Needs internal omexcavator configuration to work - refer to OMExcavator documentation.
    """
    cmd = [
        "python", f"{omexcavator_src_dir}/omero_fetch_jsons.py"
    ]

    subprocess.run(cmd, check=True)


def fetch_idr_annotation(idr_study_id: str) -> pd.DataFrame:
    """Fetch IDR annotation data for a given study ID as pandas dataframe."""

    data = urllib.urlopen(f'https://idr.openmicroscopy.org/study/{idr_study_id}/').read()
    soup = BeautifulSoup.BeautifulSoup(data)
    element = soup.find('a', text=re.compile(idr_study_id))

    anno = pd.read_csv(element["href"], sep=",")
    return anno


def produce_hf_anno(num_fields: int = 2, anno: pd.DataFrame = None) -> pd.DataFrame:
    plates_wells_all = anno[["Plate_Well"]].values
    field_filenames = list(map(lambda _l: [f"{_l[0]}_{i}.png" for i in range(num_fields)], plates_wells_all))
    filename_plate_well_df = pd.DataFrame(
        {
            "file_name": flatten_extend(field_filenames),
            "Plate_Well": [filename[:-6] for filename in flatten_extend(field_filenames)]
        }
    )
    huggingface_df = pd.merge(filename_plate_well_df, anno, on="Plate_Well")
    return huggingface_df


def save_hf_anno(
    huggingface_df: pd.DataFrame,
    converted_data_path: str,
    split_folder: str = "all",
    mixed_data_type_columns: Optional[List[str]] = None
) -> None:
    """Save metadata in Hugging Face format to a CSV file.
    :param huggingface_df: DataFrame containing the metadata
    :type huggingface_df: pd.DataFrame
    :param converted_data_path: Path to the converted data directory
    :type converted_data_path: str
    :param split_folder: Data split (e.g., "train/folder1", "test/folder4", "all"). If all, the general dataset metadata is saved to the converted_data_path/metadata folder. Default is "all".
    :type split_folder: str

    # TODO: Update docstrings.
    """  # noqa
    if mixed_data_type_columns:
        for col in mixed_data_type_columns:
            huggingface_df = huggingface_df.drop(columns=mixed_data_type_columns, errors="ignore")

    if split_folder == "all":
        os.makedirs(f"{converted_data_path}/metadata/", exist_ok=True)
        huggingface_df.to_csv(f"{converted_data_path}/metadata/metadata.csv", index=False)
    else:
        images_in_split = []
        for image_fname in os.listdir(f"{converted_data_path}/{split_folder}/"):
            images_in_split.append(image_fname)
            split_anno = pd.merge(pd.Series(images_in_split, name="file_name"), huggingface_df, how="left")
            split_anno.to_csv(f"{converted_data_path}/{split_folder}/metadata.csv", index=False)
