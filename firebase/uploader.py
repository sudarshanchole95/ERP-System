#!/usr/bin/env python3
"""
uploader.py

Universal Firestore Importer (PDF / CSV / Excel)
------------------------------------------------
A robust ETL (Extract, Transform, Load) utility designed to ingest structured data 
from various file formats directly into Google Cloud Firestore.

Features:
- Universal Parsing: Handles PDF (JSON, Tables, Record-style), CSV, and Excel.
- Deduplication: Uses content hashing or natural keys to prevent duplicate entries.
- OCR Correction: Automatically repairs common OCR misreadings (e.g., 'skuld' -> 'skuId').
- Batch Processing: Supports bulk ingestion of entire directories.
- Error Logging: Logs failed transactions to 'ERP-System/firebase/logs/'.

"""

from __future__ import annotations

import os
import re
import csv
import json
import ast
import hashlib
import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
import pdfplumber
import tkinter as tk
from tkinter import filedialog
from google.cloud import firestore

# ==========================================
# CONFIGURATION & LOGGING
# ==========================================
# Define path: ERP-System -> firebase -> logs
LOG_DIR = os.path.join("ERP-System", "firebase", "logs")

# Ensure the directory exists (Create if missing)
os.makedirs(LOG_DIR, exist_ok=True)

# Set the full path for the log file
LOG_FILE = os.path.join(LOG_DIR, "import_errors.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_failed_record(filename: str, doc_id: str, error_msg: str, data: Dict[str, Any]):
    """
    Logs failed record insertion details to a local file for audit and debugging.
    """
    msg = f"FILE: {filename} | ID: {doc_id} | ERROR: {error_msg} | DATA: {json.dumps(data, default=str)}"
    logging.error(msg)


# ==========================================
# UTILITY FUNCTIONS: UI & HASHING
# ==========================================
def open_file_dialog(title: str, filetypes) -> str:
    """Opens a system-native file selection dialog."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return path

def open_folder_dialog(title: str) -> str:
    """Opens a system-native folder selection dialog."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askdirectory(title=title)
    root.destroy()
    return path

def generate_content_hash(record: Dict[str, Any]) -> str:
    """
    Generates a deterministic MD5 hash of a record dictionary.
    Used as a fallback ID when no natural primary key is present.
    """
    s = json.dumps(record, sort_keys=True, default=str)
    return hashlib.md5(s.encode("utf-8")).hexdigest()


# ==========================================
# FIRESTORE CLIENT INITIALIZATION
# ==========================================
def load_firestore_client() -> firestore.Client:
    """
    Initializes the Google Cloud Firestore client.
    Prompts user to select a service account key or uses the default configuration.
    """
    print("\n--- Firestore Authentication ---")
    print("1. Provide specific Service Account Key")
    print("2. Use default configuration")
    
    choice = input("Select option (1/2): ").strip()
    key_path = ""

    if choice == "1":
        key_path = open_file_dialog("Select serviceAccountKey.json", [("JSON Files", "*.json")])
        if not key_path:
            print("Error: No key selected. Terminating process.")
            exit(1)
    else:
        # Default configuration path
        key_path = "ERP-System/firebase/config/firebase-key.json"

    if not os.path.exists(key_path):
        print(f"Warning: Configuration file not found at {key_path}")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    print(f"Authenticated using: {os.path.basename(key_path)}")
    return firestore.Client()


# ==========================================
# DATA PARSING & NORMALIZATION
# ==========================================
def smart_parse(value: Any) -> Any:
    """
    Intelligently converts string inputs into appropriate Python native types 
    (int, float, list, dict, or ISO date strings).
    """
    if value is None: return None
    if pd.isna(value): return None 
    
    if not isinstance(value, str): 
        # Recursively clean nested structures
        if isinstance(value, list): return [smart_parse(v) for v in value]
        if isinstance(value, dict): return {k: smart_parse(v) for k, v in value.items()}
        return value

    # Remove PDF extraction artifacts (e.g., character ID tags)
    v = value.strip()
    v = re.sub(r'\(cid:\s*\d+\)', '', v) 
    if v == "": return None

    # Numeric conversion
    if v.isdigit(): return int(v)
    try: return float(v)
    except ValueError: pass

    # Preserve ISO 8601 Date Strings
    if re.search(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}', v): return v

    # Parse JSON strings (objects or arrays)
    if (v.startswith("{") and v.endswith("}")) or (v.startswith("[") and v.endswith("]")):
        try: return json.loads(v)
        except: 
            try: return ast.literal_eval(v)
            except: pass

    # Parse delimited lists (Pipe or Slash separated)
    if ("/" in v or "|" in v) and len(v) < 50:
        sep = "/" if "/" in v else "|"
        parts = [p.strip() for p in v.split(sep) if p.strip()]
        if len(parts) > 1: return parts

    return v

def fix_ocr_key(key: str) -> str:
    """
    Normalizes dictionary keys by correcting common OCR misinterpretations.
    Example: Converts 'skuld' -> 'skuId'.
    """
    if not isinstance(key, str): return str(key)
    
    # Clean quotes and PDF artifacts
    k = key.strip().replace('"', '').replace("'", "")
    k = re.sub(r'\(cid:\s*\d+\)', '', k).strip()
    
    # Fix common 'Id' misread as 'ld'
    if k.endswith("ld") and not k.endswith("old"):
        return k[:-2] + "Id"
    return k

def clean_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively cleans a record dictionary:
    - Normalizes keys
    - Parses values to native types
    """
    cleaned = {}
    for k, v in raw.items():
        if not k: continue
        if "Unnamed" in str(k): continue  # Skip empty CSV columns
        
        new_key = fix_ocr_key(str(k))
        if not new_key: continue
        
        if isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, dict): 
                    new_list.append(clean_record(item))
                else: 
                    new_list.append(smart_parse(item))
            cleaned[new_key] = new_list
        else:
            cleaned[new_key] = smart_parse(v)
            
    return cleaned


# ==========================================
# FIRESTORE OPERATIONS
# ==========================================
def generate_auto_id(collection: str, counter: int) -> str:
    """Generates a sequential human-readable ID (e.g., DOC-000001)."""
    letters = re.sub(r"[^A-Za-z]", "", collection)[:3].upper()
    prefix = letters if letters else "DOC"
    return f"{prefix}-{counter:06d}"

def write_document(db: firestore.Client, collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
    """
    Writes a single document to Firestore.
    Returns True if written, False if skipped (already exists).
    """
    ref = db.collection(collection).document(doc_id)
    if ref.get().exists:
        return False  # Skip existing
    ref.set(data)
    return True

def process_records(filename: str, records: List[Dict[str, Any]], db: firestore.Client, collection: str, store_duplicates: bool) -> Tuple[int, int, int]:
    """
    Orchestrates the processing, cleaning, and uploading of a list of records.
    """
    written = skipped = failed = 0
    auto_counter = 1
    
    # Minimal console output
    print(f"   Processing {filename} -> '{collection}'...", end="", flush=True)

    for raw in records:
        try:
            rec = clean_record(raw)
            if not rec: continue

            doc_id = None
            if store_duplicates:
                # Append Mode: Generate unique ID to ensure insertion
                while True:
                    candidate_id = generate_auto_id(collection, auto_counter)
                    if not db.collection(collection).document(candidate_id).get().exists:
                        doc_id = candidate_id
                        break
                    auto_counter += 1
            else:
                # Unique Mode: Derive ID from data
                natural_key = next((k for k in rec.keys() if k.lower() == 'id'), None)
                if not natural_key:
                    natural_key = next((k for k in rec.keys() if 'id' in k.lower() and 'submission' not in k.lower()), None)
                
                if natural_key and rec[natural_key]:
                    doc_id = str(rec[natural_key])
                else:
                    doc_id = generate_content_hash(rec)

            if write_document(db, collection, doc_id, rec):
                written += 1
            else:
                skipped += 1

        except Exception as e:
            failed += 1
            log_failed_record(filename, doc_id or "UNKNOWN", str(e), raw)

    # Print summary on the same line
    print(f" Done. (Inserted: {written}, Skipped: {skipped}, Failed: {failed})")
    return written, skipped, failed


# ==========================================
# FILE PARSERS (PDF/CSV/EXCEL)
# ==========================================
def _parse_broken_json_chunk(text: str) -> Dict[str, Any]:
    """
    Attempt to recover data from malformed JSON text chunks using regex heuristics.
    """
    # Attempt 1: Standard JSON with minor cleanup
    try:
        match = re.search(r'(\{.*\})', text.replace(')', '}'), re.DOTALL)
        if match:
            clean_json = match.group(1)
            return json.loads(clean_json)
    except: pass

    # Attempt 2: Regex extraction for key-value pairs
    data = {}
    pattern = r'"([a-zA-Z0-9_]+)"\s*:\s*(".*?"|\d+\.?\d*|true|false|null)'
    for match in re.finditer(pattern, text):
        k, v = match.groups()
        if v.startswith('"') and v.endswith('"'): v = v[1:-1]
        data[k] = smart_parse(v)
    return data

def _extract_by_splitting_records(text: str) -> List[Dict[str, Any]]:
    """Strategy: Splits text by 'Record X' delimiters."""
    chunks = re.split(r'(?:^|\n)Record\s+\d+', text)
    records = []
    
    for chunk in chunks:
        if not chunk.strip(): continue
        # Detect JSON-like content within chunk
        if "{" in chunk and ":" in chunk:
            rec = _parse_broken_json_chunk(chunk)
            if rec: records.append(rec); continue
        
        # Fallback to Line-by-Line parsing
        lines = chunk.splitlines()
        rec = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                if len(k.split()) < 3: rec[fix_ocr_key(k)] = smart_parse(v)
        if rec: records.append(rec)
    return records

def _extract_json_blocks_strict(text: str) -> List[Dict[str, Any]]:
    """Strategy: Extracts strictly valid JSON blocks from raw text."""
    blocks = []
    buf = ""; depth = 0
    for ch in text:
        if ch == "{":
            if depth == 0: buf = ""
            depth += 1
        if depth > 0: buf += ch
        if ch == "}":
            depth -= 1
            if depth == 0: blocks.append(buf)
    
    results = []
    for b in blocks:
        try:
            res = json.loads(b)
            if isinstance(res, dict): results.append(res)
            elif isinstance(res, list): results.extend(res)
        except: pass
    return results

def universal_pdf_parser(path: str) -> List[Dict[str, Any]]:
    """
    Parses PDF content using multiple strategies:
    1. Record Splitting (Text-based records)
    2. JSON Block Extraction
    3. Table Extraction
    """
    filename = os.path.basename(path)
    text = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages: text += (p.extract_text() or "") + "\n"

    t = text.strip()
    all_findings = []

    # Strategy 1: Record Split
    if "Record 1" in t:
        recs = _extract_by_splitting_records(t)
        if recs: all_findings.extend(recs)

    # Strategy 2: Full JSON
    if not all_findings:
        json_recs = _extract_json_blocks_strict(t)
        if json_recs: all_findings.extend(json_recs)

    # Strategy 3: Tables
    if not all_findings:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    headers = [str(h).strip() if h else f"col_{i}" for i, h in enumerate(table[0])]
                    for row in table[1:]:
                        safe_row = row + [None] * (len(headers) - len(row))
                        r = {headers[i]: smart_parse(cell) for i, cell in enumerate(safe_row) if i < len(headers)}
                        if any(r.values()): all_findings.append(r)

    # Local Deduplication (before upload)
    unique_map = {}
    for r in all_findings:
        if not isinstance(r, dict): continue
        id_key = next((k for k in r.keys() if 'id' in k.lower() and 'submission' not in k.lower()), None)
        if id_key and r[id_key]: key = str(r[id_key])
        else: key = generate_content_hash(r)
        
        # Keep the record with the most data fields
        if key not in unique_map or len(r) > len(unique_map[key]): 
            unique_map[key] = r

    final = list(unique_map.values())
    return final

def import_pdf(path: str, db: firestore.Client, collection: str, store_duplicates: bool) -> Tuple[int, int, int]:
    records = universal_pdf_parser(path)
    if not records:
        print(f"   Warning: No structured data found in {os.path.basename(path)}")
        return 0, 0, 0
    return process_records(os.path.basename(path), records, db, collection, store_duplicates)

def import_csv(path: str, db: firestore.Client, collection: str, store_duplicates: bool) -> Tuple[int, int, int]:
    filename = os.path.basename(path)
    try:
        df = pd.read_csv(path, dtype=str)
        if df.empty: return 0, 0, 0
        return process_records(filename, df.to_dict(orient="records"), db, collection, store_duplicates)
    except Exception as e:
        print(f"   Error reading CSV {filename}: {e}")
        return 0, 0, 1

def import_excel(path: str, db: firestore.Client, collection: str, store_duplicates: bool) -> Tuple[int, int, int]:
    filename = os.path.basename(path)
    try:
        df = pd.read_excel(path, dtype=str)
        if df.empty: return 0, 0, 0
        return process_records(filename, df.to_dict(orient="records"), db, collection, store_duplicates)
    except Exception as e:
        print(f"   Error reading Excel {filename}: {e}")
        return 0, 0, 1


# ==========================================
# MAIN EXECUTION FLOW
# ==========================================
def main():
    print("\n" + "="*40)
    print(" FIRESTORE DATA IMPORTER ".center(40, "="))
    print("="*40 + "\n")
    
    db = load_firestore_client()

    print("\n--- Import Mode ---")
    print("1. Single File")
    print("2. Batch Folder")
    mode = input("Select mode (1/2): ").strip()

    files = []
    if mode == "1":
        p = open_file_dialog("Select File", [("Data Files", "*.csv *.xlsx *.xls *.pdf")])
        if p: files.append(p)
    elif mode == "2":
        f = open_folder_dialog("Select Folder")
        if f:
            for n in os.listdir(f):
                if n.lower().endswith((".csv", ".xlsx", ".xls", ".pdf")):
                    files.append(os.path.join(f, n))

    if not files:
        print("No files selected. Exiting.")
        return

    print("\n--- Configuration ---")
    user_coll = input("Target Collection Name (Empty = Auto-detect from filename): ").strip()
    dupe_input = input("Store Duplicates? (y/N): ").strip().lower()
    store_duplicates = dupe_input == 'y'

    print("\n" + "-"*40)
    print(" STARTING IMPORT ".center(40, "-"))
    print("-"*40)

    grand_written = 0
    grand_skipped = 0
    grand_failed = 0

    for path in files:
        # Determine collection name
        if user_coll:
            coll = user_coll
        else:
            coll = Path(path).stem
            # Sanitize collection name (alphanumeric + underscore only)
            coll = re.sub(r'[^a-zA-Z0-9_]', '_', coll)

        ext = Path(path).suffix.lower()
        w = s = f = 0
        
        if ext == ".csv": 
            w, s, f = import_csv(path, db, coll, store_duplicates)
        elif ext in (".xlsx", ".xls"): 
            w, s, f = import_excel(path, db, coll, store_duplicates)
        elif ext == ".pdf": 
            w, s, f = import_pdf(path, db, coll, store_duplicates)
        
        grand_written += w
        grand_skipped += s
        grand_failed += f

    print("\n" + "="*40)
    print(" IMPORT SUMMARY ".center(40, "="))
    print("="*40)
    print(f"Total Inserted : {grand_written}")
    print(f"Total Skipped  : {grand_skipped}")
    print(f"Total Failed   : {grand_failed}")
    
    if grand_failed > 0:
        print(f"\nSee '{LOG_FILE}' for detailed error logs.")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()