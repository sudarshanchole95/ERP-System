from __future__ import annotations

"""
Firestore ETL Orchestrator (Universal & Production Ready)
---------------------------------------------------------
Central command to auto-discover and import data from ANY CSV, Excel, or PDF.
Features:
- Dynamic Collection Naming (filename -> collectionName)
- Universal File Discovery (scans entire folder)
- Clean Console Output
"""

import argparse
import sys
import logging
import re
from pathlib import Path

# --------------------------------------------------------
# 1. SILENCE NOISY LOGS
# --------------------------------------------------------
logging.basicConfig(level=logging.WARNING)
logging.getLogger("importer").setLevel(logging.WARNING)

# --------------------------------------------------------
# PATH SETUP
# --------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent   # -> firebase/import-scripts
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from parsers.csv_parser import import_csv_file
    from parsers.excel_parser import import_excel_file
    from parsers.pdf_parser import import_pdf_file
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

# --------------------------------------------------------
# HELPER: Dynamic Name Sanitizer
# --------------------------------------------------------
def filename_to_collection(filename: str) -> str:
    """
    Converts 'My Sales Data 2024.csv' -> 'My_Sales_Data_2024'
    PRESERVES CASING.
    1. Remove extension
    2. Replace non-alphanumeric chars with underscores
    3. Keep upper/lower case exactly as is
    """
    stem = Path(filename).stem
    
    # Replace anything that isn't a letter or number with an underscore
    # This keeps "PromodizerAllocations" as "PromodizerAllocations"
    # And "My Data" becomes "My_Data"
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', stem)
    
    # Remove leading/trailing underscores just in case
    clean_name = clean_name.strip('_')
    
    if not clean_name: 
        return "genericCollection"

    return clean_name

# --------------------------------------------------------
# AUTO IMPORT (BATCH)
# --------------------------------------------------------
def auto_import_all():
    print("\n" + "="*60)
    print(" UNIVERSAL FIRESTORE IMPORTER ".center(60))
    print("="*60 + "\n")

    sample_root = BASE_DIR.parent / "sample-data"
    if not sample_root.exists():
        print(f"❌ Error: Data folder not found at {sample_root}")
        return

    # 1. CSV
    csv_files = sorted(list((sample_root / "csv").glob("*.csv")))
    if csv_files:
        print(f"--- Processing {len(csv_files)} CSV Files ---")
        for f in csv_files:
            coll = filename_to_collection(f.name)
            import_csv_file(str(f), coll)

    # 2. Excel
    xlsx_files = sorted(list((sample_root / "excel").glob("*.xlsx")))
    if xlsx_files:
        print(f"\n--- Processing {len(xlsx_files)} Excel Files ---")
        for f in xlsx_files:
            coll = filename_to_collection(f.name)
            import_excel_file(str(f), coll)

    # 3. PDF
    pdf_files = sorted(list((sample_root / "pdf").glob("*.pdf")))
    if pdf_files:
        print(f"\n--- Processing {len(pdf_files)} PDF Files ---")
        for f in pdf_files:
            coll = filename_to_collection(f.name)
            import_pdf_file(str(f), coll)

    print("\n" + "="*60)
    print(" ✅ AUTO IMPORT COMPLETED ".center(60))
    print("="*60 + "\n")

# --------------------------------------------------------
# MAIN ENTRY
# --------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Firestore Import")
    parser.add_argument("--type", help="csv | excel | pdf")
    parser.add_argument("--file", help="path to file")
    parser.add_argument("--collection", help="Override Firestore collection name")
    
    args = parser.parse_args()

    if not args.type:
        auto_import_all()
    else:
        # Manual Mode
        target_coll = args.collection if args.collection else filename_to_collection(args.file)
        
        if args.type == "csv":
            import_csv_file(args.file, target_coll)
        elif args.type == "excel":
            import_excel_file(args.file, target_coll)
        elif args.type == "pdf":
            import_pdf_file(args.file, target_coll)