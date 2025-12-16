cwlVersion: v1.2
class: CommandLineTool
label: "Step 3: Upload converted folder to Hugging Face"

requirements:
  DockerRequirement:
    dockerPull: "python:3.11"   # same image
  InitialWorkDirRequirement:
    listings:
      - entryname: run_step3.py
        entry: |
          import argparse
          from pathlib import Path
          import bioimageaipub as bp

          def main():
              parser = argparse.ArgumentParser()
              parser.add_argument("--destination-dataset", required=True)
              args = parser.parse_args()

              converted_folder_path = Path("data/idr_converted")

              bp.hf_upload_converted_folder(
                  str(converted_folder_path),
                  args.destination_dataset,
              )

          if __name__ == "__main__":
              main()
      - entry: $(inputs.converted_dir)
        entryname: data/idr_converted
        writable: false

baseCommand:
  - python
  - run_step3.py

inputs:
  converted_dir:
    type: Directory

  destination_dataset:
    type: string
    inputBinding:
      prefix: --destination-dataset

stdout: step3.log

outputs: {}
