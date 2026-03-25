"""
restamp - Re-stamp Accession Number and Patient ID in DICOM files.

Usage:
    restamp <STR> <src_folder> <dest_folder>

For every DICOM file found in <src_folder>:
  - Sets Accession Number to  A<STR>
  - Sets Patient ID        to  P<STR>
  - Writes the modified file into <dest_folder> (preserving the filename).

The destination folder is created automatically if it does not exist.
"""

import os
import sys
from pathlib import Path

import pydicom


def usage():
    print("Usage: restamp <STR> <src_folder> <dest_folder>")
    print()
    print("  STR         Identifier string. Accession Number becomes ASTR,")
    print("              Patient ID becomes PSTR.")
    print("  src_folder  Folder containing the source DICOM files.")
    print("  dest_folder Folder where modified DICOM files will be written.")
    sys.exit(1)


def is_dicom(filepath):
    """Return True if the file looks like a valid DICOM file."""
    try:
        pydicom.dcmread(filepath, stop_before_pixels=True, force=True)
        return True
    except Exception:
        return False


def process_file(src_path, dest_path, accession, patient_id):
    """Read a DICOM file, update the tags, and write to dest_path."""
    try:
        ds = pydicom.dcmread(src_path, force=True)
    except Exception as e:
        print(f"  WARNING: Could not read {src_path}: {e}")
        return False

    # Update the two tags
    ds.AccessionNumber = accession
    ds.PatientID = patient_id

    try:
        ds.save_as(dest_path)
    except Exception as e:
        print(f"  WARNING: Could not write {dest_path}: {e}")
        return False

    return True


def main():
    if len(sys.argv) != 4:
        usage()

    str_id = sys.argv[1]
    src_folder = sys.argv[2]
    dest_folder = sys.argv[3]

    accession = f"A{str_id}"
    patient_id = f"P{str_id}"

    # Validate source folder
    if not os.path.isdir(src_folder):
        print(f"ERROR: Source folder does not exist: {src_folder}")
        sys.exit(1)

    # Create destination folder if needed
    Path(dest_folder).mkdir(parents=True, exist_ok=True)

    print(f"Accession Number : {accession}")
    print(f"Patient ID       : {patient_id}")
    print(f"Source           : {src_folder}")
    print(f"Destination      : {dest_folder}")
    print()

    processed = 0
    skipped = 0

    for filename in sorted(os.listdir(src_folder)):
        src_path = os.path.join(src_folder, filename)

        # Skip directories
        if not os.path.isfile(src_path):
            continue

        # Check if it's a DICOM file
        if not is_dicom(src_path):
            print(f"  Skipping (not DICOM): {filename}")
            skipped += 1
            continue

        dest_path = os.path.join(dest_folder, filename)

        if process_file(src_path, dest_path, accession, patient_id):
            print(f"  OK: {filename}")
            processed += 1
        else:
            skipped += 1

    print()
    print(f"Done. {processed} file(s) processed, {skipped} skipped.")


if __name__ == "__main__":
    main()
