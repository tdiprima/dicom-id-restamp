#!/usr/bin/env python3
"""
oops - Re-stamp Accession Number and Patient ID in DICOM files.

Usage:
    oops --pid <patient_id> --acc <accession> <src_folder> <dest_folder>

For every DICOM file found in <src_folder>:
  - Sets Patient ID        to the given value
  - Sets Accession Number  to the given value
  - Writes the modified file into <dest_folder> (preserving the filename).

The destination folder is created automatically if it does not exist.

Examples:
    oops --pid patient1 --acc acc1 /data2/patient1 /data2/dest/patient1
    oops --pid patient3 --acc acc3 /data2/patient3 /data2/dest/patient3
"""

import argparse
import os
import sys
from pathlib import Path

import pydicom


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

    ds.AccessionNumber = accession
    ds.PatientID = patient_id

    try:
        ds.save_as(dest_path)
    except Exception as e:
        print(f"  WARNING: Could not write {dest_path}: {e}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        prog="oops",
        description="Re-stamp Accession Number and Patient ID in DICOM files.",
    )
    parser.add_argument("--pid", required=True, help="Patient ID to set")
    parser.add_argument("--acc", required=True, help="Accession Number to set")
    parser.add_argument("src", help="Source folder containing DICOM files")
    parser.add_argument("dest", help="Destination folder for modified files")

    args = parser.parse_args()

    accession = args.acc
    patient_id = args.pid
    src_folder = args.src
    dest_folder = args.dest

    # Validate source folder
    if not os.path.isdir(src_folder):
        print(f"ERROR: Source folder does not exist: {src_folder}")
        sys.exit(1)

    # Create destination folder if needed
    Path(dest_folder).mkdir(parents=True, exist_ok=True)

    print(f"Patient ID       : {patient_id}")
    print(f"Accession Number : {accession}")
    print(f"Source           : {src_folder}")
    print(f"Destination      : {dest_folder}")
    print()

    processed = 0
    skipped = 0

    for filename in sorted(os.listdir(src_folder)):
        src_path = os.path.join(src_folder, filename)

        if not os.path.isfile(src_path):
            continue

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
