cwlVersion: v1.2
class: CommandLineTool
label: "Step 2: Split data and create HF annotations"

requirements:
  DockerRequirement:
    dockerPull: "python:3.11"   # same image as above
  InitialWorkDirRequirement:
    listings:
      - entryname: run_step2.py
        entry: |
          import argparse
          from pathlib import Path
          import bioimageaipub as bp

          def main():
              parser = argparse.ArgumentParser()
              parser.add_argument("--train-ratio", type=float, default=0.8)
              parser.add_argument("--study-id", default="idr0012")
              parser.add_argument("--hf-num-fields", type=int, default=2)
              parser.add_argument("--omexcavator-path", default=None)
              parser.add_argument("--mixed-data-type-columns",
                                  default="Original GeneID Target")
              args = parser.parse_args()

              converted_data_path = Path("data/idr_converted")

              # 1) Train/test split
              bp.test_train_split(
                  converted_data_path=converted_data_path,
                  train_ratio=args.train_ratio,
              )

              bp.split_into_folders(
                  target=converted_data_path / "test",
                  max_files=10000,
              )
              bp.split_into_folders(
                  target=converted_data_path / "train",
                  max_files=10000,
              )

              # 2) Fetch IDR annotation + HF-style annotation
              anno = bp.fetch_idr_annotation(study_id=args.study_id)
              huggingface_df = bp.produce_hf_anno(
                  num_fields=args.hf_num_fields,
                  anno=anno,
              )

              # 3) OMERO metadata (optional)
              if args.omexcavator_path:
                  bp.fetch_omero_metadata(omexcavator_path=args.omexcavator_path)
                  bp.permute_metadata()

              # 4) Save HF annotation into converted_data_path
              bp.save_hf_anno(
                  huggingface_df,
                  converted_data_path=str(converted_data_path),
                  split_folder="all",
                  mixed_data_type_columns=[args.mixed_data_type_columns],
              )

          if __name__ == "__main__":
              main()
      - entry: $(inputs.converted_dir)
        entryname: data/idr_converted
        writable: true

baseCommand:
  - python
  - run_step2.py

inputs:
  converted_dir:
    type: Directory

  train_ratio:
    type: float?
    inputBinding:
      prefix: --train-ratio

  study_id:
    type: string?
    inputBinding:
      prefix: --study-id

  hf_num_fields:
    type: int?
    inputBinding:
      prefix: --hf-num-fields

  omexcavator_path:
    type: string?
    inputBinding:
      prefix: --omexcavator-path

  mixed_data_type_columns:
    type: string?
    inputBinding:
      prefix: --mixed-data-type-columns

stdout: step2.log

outputs:
  converted_dir:
    type: Directory
    outputBinding:
      glob: "data/idr_converted"
