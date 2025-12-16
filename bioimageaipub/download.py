import subprocess
from pathlib import Path
import s3fs


def list_available_data_s3(
    endpoint_url: str = "https://uk1s3.embassy.ebi.ac.uk",
    data_dir: str = "s3://bia-integrator-data/S-BIAD845/",
    file_type: str = ".zarr",
) -> list[str]:
    """
    Docstring for list_available_data    
    :param endpoint_url: S3 endpoint URL
    :type endpoint_url: str
    :param data_dir: Description
    :type data_dir: str
    :param file_type: Description
    :type file_type: str
    :return: Available bioimages
    """
    s3 = s3fs.S3FileSystem(anon=True, client_kwargs={
        'endpoint_url': endpoint_url
    })

    pattern = "**/*.{}".format(file_type.lstrip('.'))
    data_files = s3.glob(data_dir + pattern, maxdepth=3)
    return data_files


def download_zarrs_from_s3(output_path: str, list_path: str):
    with Path(list_path).open("r") as f:
        for line in f:
            p = line.strip()
            if not p:
                continue  # skip empty lines

            print(p)

            cmd = [
                "aws", "s3", "sync",
                "--endpoint-url", "https://uk1s3.embassy.ebi.ac.uk",
                "--no-sign-request",
                f"s3://{p}",
                f"{output_path}/{p}",
            ]

            # Run the command and raise an error if it fails
            subprocess.run(cmd, check=True)
