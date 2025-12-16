cwlVersion: v1.2
class: CommandLineTool
label: "Step 1: Download ZARRs and convert to PNG"

requirements:
  DockerRequirement:
    dockerPull: "python:3.11"   # replace with your custom image with bioimageaipub installed
  InitialWorkDirRequirement:
    listings:
      - entryname: run_step1.py
        entry: |
          import argparse
          from pathlib import Path
          import bioimageaipub as bp

          def main():
              parser = argparse.ArgumentParser()
              parser.add_argument("--endpoint-url", default="https://uk1s3.embassy.ebi.ac.uk")
              parser.add_argument("--data-dir", default="s3://bia-integrator-data/S-BIAD845/")
              parser.add_argument("--file-type", default=".zarr")

              parser.add_argument("--list-path", required=True)

              args = parser.parse_args()

              root_data_path = Path("data/idr_zarrs")
              converted_data_path = Path("data/idr_converted")

              # 1) List available Zarrs (for logging)
              bp.list_available_data_s3(
                  endpoint_url=args.endpoint_url,
                  data_dir=args.data_dir,
                  file_type=args.file_type,
              )

              # 2) Download Zarrs
              root_data_path.mkdir(parents=True, exist_ok=True)
              bp.download_zarrs_from_s3(
                  path=str(root_data_path),
                  list_path=args.list_path,
              )

              # 3) Convert Zarr → PNG
              converted_data_path.mkdir(parents=True, exist_ok=True)
              bp.convert_zarr(
                  root_data_path=root_data_path,
                  converted_data_path=converted_data_path,
                  zarr_file_list=args.list_path,
                  output_format="png",
              )

          if __name__ == "__main__":
              main()

baseCommand:
  - python
  - run_step1.py

inputs:
  endpoint_url:
    type: string?
    inputBinding:
      prefix: --endpoint-url
  data_dir:
    type: string?
    inputBinding:
      prefix: --data-dir
  file_type:
    type: string?
    inputBinding:
      prefix: --file-type

  list_path:
    type: File
    inputBinding:
      prefix: --list-path

stdout: step1.log

outputs:
  converted_dir:
    type: Directory
    outputBinding:
      glob: "data/idr_converted"
