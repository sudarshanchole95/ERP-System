from __future__ import annotations
import sys
import json
import re
import hashlib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from core.firestore_writer import FirestoreWriter
from core.validator import validate_documents

# ---------------------------------------------------------------
# DATA CLEANING LOGIC
# ---------------------------------------------------------------
def fix_value(value):
    """Normalize values (int vs float vs string)."""
    if pd.isna(value) or value == "":
        return None
    
    # Handle numbers
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value.is_integer(): return int(value)
        return value

    # Handle Strings
    if isinstance(value, str):
        v = value.strip()
        # Try JSON
        if (v.startswith("{") and v.endswith("}")) or (v.startswith("[") and v.endswith("]")):
            try: return json.loads(v)
            except: pass
            
        # Try Numeric String
        if v.isdigit(): return int(v)
        try:
            f = float(v)
            if f.is_integer(): return int(f)
            return f
        except: pass
            
    return value

def generate_deterministic_id(row: dict) -> str:
    """Generates a consistent ID based on content if 'id' is missing."""
    row_str = json.dumps(row, sort_keys=True, default=str)
    return hashlib.md5(row_str.encode("utf-8")).hexdigest()

def transform_row(row: dict) -> dict:
    row = {k: fix_value(v) for k, v in row.items()}

    # Expand 'address.city' -> {'address': {'city': ...}}
    address = {}
    for key in list(row.keys()):
        if key.startswith("address."):
            sub = key.split(".", 1)[1]
            address[sub] = row[key]
            del row[key]
    if address: row["address"] = address

    # Handle scannedSkus
    if "scannedSkus" in row:
        val = row["scannedSkus"]
        if val in (None, ""): row["scannedSkus"] = []
        elif isinstance(val, str) and "," in val:
            row["scannedSkus"] = [x.strip() for x in val.split(",")]
        elif not isinstance(val, list):
            row["scannedSkus"] = [val]

    # --- ID LOGIC: Priority to 'id' column ---
    if "id" in row and row["id"] is not None:
        row["id"] = str(row["id"])
    else:
        # Fallback Aliases or Hash
        alias_id = next((row[k] for k in ["sku", "skuId", "code", "email", "storeId"] if k in row and row[k]), None)
        if alias_id:
            row["id"] = str(alias_id)
        else:
            row["id"] = generate_deterministic_id(row)

    return row

# ---------------------------------------------------------------
# IMPORT FUNCTION
# ---------------------------------------------------------------
def import_csv_file(path: str, collection_name: str, verbose: bool = False):
    try:
        df = pd.read_csv(path)
    except:
        df = pd.read_csv(path, sep=';')
        
    df = df.where(pd.notnull(df), None)

    docs = [transform_row(r) for r in df.to_dict(orient="records")]

    valid, errors = validate_documents(docs, collection_name)

    writer = FirestoreWriter()
    written, skipped = writer.write_documents(
        collection_name,
        valid,
        id_field="id",
        check_existing_and_skip_if_same=True
    )

    print(f"   📄 {Path(path).name:<30} -> {collection_name:<25} [Written: {written} | Skipped: {skipped}]")

if __name__ == "__main__":
    print("\n🚀 RUNNING STANDALONE CSV IMPORT...")
    csv_dir = BASE_DIR.parent / "sample-data" / "csv"
    
    if not csv_dir.exists():
        print(f"❌ Error: Directory not found at {csv_dir}")
        sys.exit(1)

    files = list(csv_dir.glob("*.csv"))
    if not files: print(f"⚠️ No CSV files found.")
    else:
        for f in files:
            coll = re.sub(r'[^a-zA-Z0-9]', '_', f.stem).strip('_')
            import_csv_file(str(f), coll)
    print("\n✅ CSV Import Complete.")