# dicom-id-restamp

DICOM metadata batch edit

Batch-rewrite Accession Number and Patient ID in DICOM files without touching pixel data.

## When DICOM Identifiers Need a Fresh Start

Medical imaging workflows sometimes produce studies with placeholder, conflicting, or incorrect identifiers — especially during research, testing, or data migration. Manually correcting `AccessionNumber` and `PatientID` across dozens or hundreds of files is tedious and error-prone.

## What This Tool Does

`restamp` reads every DICOM file in a source folder, stamps a new Accession Number (`A<ID>`) and Patient ID (`P<ID>`) derived from a single identifier string you supply, and writes the updated files to a destination folder — leaving the originals untouched. Non-DICOM files are silently skipped. The destination directory is created automatically if it doesn't exist.

## Example

Given a folder of DICOM slices from a test study:

```
restamp 00123 /data/raw_study /data/restamped_study
```

Every DICOM file in `/data/raw_study` gets written to `/data/restamped_study` with:

- `AccessionNumber` → `A00123`
- `PatientID` → `P00123`

Output:

```
Accession Number : A00123
Patient ID       : P00123
Source           : /data/raw_study
Destination      : /data/restamped_study

  OK: CT.001.dcm
  OK: CT.002.dcm
  Skipping (not DICOM): Thumbs.db

Done. 2 file(s) processed, 1 skipped.
```

## Usage

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Install

```bash
uv sync
```

### Run

```bash
uv run restamp <STR> <src_folder> <dest_folder>
```

| Argument | Description |
|---|---|
| `STR` | Identifier string. Sets `AccessionNumber` to `A<STR>` and `PatientID` to `P<STR>`. |
| `src_folder` | Folder containing source DICOM files. |
| `dest_folder` | Output folder. Created automatically if it does not exist. |

### Without uv

```bash
pip install pydicom
python restamp.py <STR> <src_folder> <dest_folder>
```
