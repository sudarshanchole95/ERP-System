from __future__ import annotations
import sys
import json
import ast
import re
import hashlib
from pathlib import Path
import pdfplumber

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from core.firestore_writer import FirestoreWriter
from core.validator import validate_documents

def fix_value(value):
    if not isinstance(value, str): return value
    # --- FIX: Aggressive Whitespace Cleaning ---
    # Replaces newlines with space, and multiple spaces with single space
    v = " ".join(value.split())
    
    if v == "": return None
    
    # Try JSON/List
    if (v.startswith("{") and v.endswith("}")) or (v.startswith("[") and v.endswith("]")):
        try: return json.loads(v)
        except: 
            try: return ast.literal_eval(v)
            except: pass
            
    # Try Numbers
    if v.isdigit(): return int(v)
    try: 
        f = float(v)
        if f.is_integer(): return int(f)
        return f
    except: pass
    
    return v

def extract_tables_from_page(page):
    results = []
    tables = page.extract_tables()
    for table in tables:
        if not table: continue
        headers = [str(h).replace('\n', ' ').strip() for h in table[0]]
        for row in table[1:]:
            doc = {}
            for i, cell in enumerate(row):
                if i < len(headers):
                    val_str = str(cell) if cell else ""
                    doc[headers[i]] = fix_value(val_str)
            if any(doc.values()): results.append(doc)
    return results

def extract_json_blocks(text):
    blocks = []
    buf = ""; depth = 0
    for ch in text:
        if ch == "{":
            if depth == 0: buf = ""
            depth += 1
        if depth > 0: buf += ch
        if ch == "}":
            depth -= 1
            if depth == 0:
                try: blocks.append(json.loads(buf))
                except: 
                    try: blocks.append(ast.literal_eval(buf))
                    except: pass
    return blocks

def extract_kv_records(text):
    records = []
    chunks = re.split(r'(?:^|\n)(?:Record|ROW)\s+\d+', text, flags=re.IGNORECASE)
    if len(chunks) > 1:
        for chunk in chunks:
            if chunk.strip(): records.append(_parse_kv_lines(chunk.splitlines()))
    else:
        blocks = re.split(r'\n\s*\n', text) 
        for block in blocks:
            rec = _parse_kv_lines(block.splitlines())
            if len(rec) > 1: records.append(rec)
    return records

def _parse_kv_lines(lines):
    row = {}
    for line in lines:
        line = line.strip()
        if not line: continue
        if ":" in line:
            parts = line.split(":", 1)
            k = parts[0].strip(); v = parts[1].strip()
            if len(k) < 50: row[k] = fix_value(v)
        elif "=" in line:
            parts = line.split("=", 1)
            k = parts[0].strip(); v = parts[1].strip()
            if len(k) < 50: row[k] = fix_value(v)
    return row

def parse_pdf(path: str) -> list[dict]:
    all_text = ""
    table_docs = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            all_text += (pg.extract_text() or "") + "\n"
            table_docs.extend(extract_tables_from_page(pg))

    final_docs = []
    if table_docs: final_docs.extend(table_docs)
    json_docs = extract_json_blocks(all_text)
    if json_docs: final_docs.extend(json_docs)
    if len(final_docs) < 2:
        final_docs.extend(extract_kv_records(all_text))

    dedup = {}
    for d in final_docs:
        if not isinstance(d, dict): continue
        clean_d = {}
        for k, v in d.items():
            k_clean = k
            if isinstance(k, str) and k.endswith("ld") and not k.endswith("old"):
                k_clean = k[:-2] + "Id"
            clean_d[k_clean] = v
            
        # --- ID LOGIC ---
        if "id" in clean_d and clean_d["id"] is not None:
            clean_d["id"] = str(clean_d["id"])
            dedup[clean_d["id"]] = clean_d
        else:
            alias_id = next((clean_d[k] for k in ["sku", "skuId", "code", "email", "storeId"] if k in clean_d and clean_d[k]), None)
            if alias_id:
                clean_d["id"] = str(alias_id)
                dedup[clean_d["id"]] = clean_d
            else:
                h = hashlib.md5(json.dumps(clean_d, sort_keys=True, default=str).encode()).hexdigest()
                dedup[h] = clean_d

    return list(dedup.values())

def import_pdf_file(path: str, collection_name: str):
    docs = parse_pdf(path)
    if not docs:
        print(f"   ⚠️ Warning: No structured data extracted from {Path(path).name}")
        return

    valid, errors = validate_documents(docs, collection_name)
    writer = FirestoreWriter()
    written, skipped = writer.write_documents(
        collection_name,
        valid,
        id_field="id",
        check_existing_and_skip_if_same=True,
    )
    print(f"   📑 {Path(path).name:<30} -> {collection_name:<25} [Written: {written} | Skipped: {skipped}]")

if __name__ == "__main__":
    print("\n🚀 RUNNING STANDALONE PDF IMPORT...")
    pdf_dir = BASE_DIR.parent / "sample-data" / "pdf"
    
    if not pdf_dir.exists():
        print(f"❌ Error: Directory not found at {pdf_dir}")
        sys.exit(1)

    files = list(pdf_dir.glob("*.pdf"))
    if not files: print(f"⚠️ No PDF files found.")
    else:
        for f in files:
            coll = re.sub(r'[^a-zA-Z0-9]', '_', f.stem).strip('_')
            import_pdf_file(str(f), coll)
    print("\n✅ PDF Import Complete.")