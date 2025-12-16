from huggingface_hub import upload_large_folder
destination_dataset = "stefanches/idr0012-fuchs-cellmorph-S-BIAD845"
converted_folder_path = "/dev/sdb/S-BIAD845-converted"


def hf_upload_converted_folder(converted_folder_path, destination_dataset):
    upload_large_folder(
        folder_path=converted_folder_path,
        repo_id=destination_dataset,
        repo_type="dataset",
    )
