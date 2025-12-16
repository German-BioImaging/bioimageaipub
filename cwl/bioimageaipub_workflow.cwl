cwlVersion: v1.2
class: Workflow
label: "bioimageaipub multi-step IDR → HF workflow"

inputs:
  list_path: File

  endpoint_url: string?
  data_dir: string?
  file_type: string?

  train_ratio: float?
  study_id: string?
  hf_num_fields: int?
  omexcavator_path: string?
  mixed_data_type_columns: string?

  destination_dataset: string

steps:
  step1_download_and_convert:
    run: download_and_convert.cwl
    in:
      list_path: list_path
      endpoint_url: endpoint_url
      data_dir: data_dir
      file_type: file_type
    out:
      - converted_dir

  step2_split_and_annotate:
    run: split_and_annotate.cwl
    in:
      converted_dir: step1_download_and_convert/converted_dir
      train_ratio: train_ratio
      study_id: study_id
      hf_num_fields: hf_num_fields
      omexcavator_path: omexcavator_path
      mixed_data_type_columns: mixed_data_type_columns
    out:
      - converted_dir

  step3_upload_to_hf:
    run: upload_to_hf.cwl
    in:
      converted_dir: step2_split_and_annotate/converted_dir
      destination_dataset: destination_dataset
    out: []

outputs:
  final_converted_dir:
    type: Directory
    outputSource: step2_split_and_annotate/converted_dir
