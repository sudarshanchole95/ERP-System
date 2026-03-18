from __future__ import annotations
import copy
import hashlib
import json
import time
import random
from typing import Iterable, Mapping, Optional, Tuple, Any
from google.cloud.firestore import Client
from core.config import get_firestore_client
from core.logger import logger

MAX_BATCH = 500
RETRY_ATTEMPTS = 5
BASE_BACKOFF = 0.5 

def _stable_hash(obj: Any) -> str:
    """Deterministic hash of JSON-compatible object."""
    dumped = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(dumped.encode("utf-8")).hexdigest()

def _normalize(value: Any) -> Any:
    """Normalize data for comparison (remove empty/null)."""
    if value is None: return None
    if isinstance(value, (int, float, bool, str)): return value

    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            nv = _normalize(v)
            if nv in (None, "", [], {}): continue
            out[k] = nv
        return out

    if isinstance(value, list):
        out_list = []
        for item in value:
            ni = _normalize(item)
            if ni in (None, "", [], {}): continue
            out_list.append(ni)
        return out_list

    return str(value)

class FirestoreWriter:
    def __init__(self, client: Client | None = None):
        self.client = client or get_firestore_client()

    def _commit_with_retry(self, batch):
        attempt = 0
        while True:
            try:
                batch.commit()
                return
            except Exception as exc:
                attempt += 1
                if attempt > RETRY_ATTEMPTS:
                    logger.exception("Batch commit failed after retries.")
                    raise
                time.sleep(BASE_BACKOFF * (2 ** attempt))

    def write_documents(
        self,
        collection: str,
        docs: Iterable[Mapping],
        id_field: Optional[str] = None,
        check_existing_and_skip_if_same: bool = False,
    ) -> Tuple[int, int]:
        
        docs = list(docs)
        if not docs: return 0, 0

        col_ref = self.client.collection(collection)
        batch = self.client.batch()
        written = 0
        skipped = 0
        count_in_batch = 0

        for raw in docs:
            doc = copy.deepcopy(dict(raw))

            # Ensure scannedSkus is list if present
            if "scannedSkus" in doc and not isinstance(doc["scannedSkus"], list):
                try: doc["scannedSkus"] = list(doc["scannedSkus"])
                except: pass

            # ID Logic
            if id_field and doc.get(id_field):
                doc_id = str(doc[id_field])
            else:
                doc_id = _stable_hash(_normalize(doc))

            doc_ref = col_ref.document(doc_id)

            if check_existing_and_skip_if_same:
                try:
                    snap = doc_ref.get()
                    if snap.exists:
                        if _stable_hash(_normalize(snap.to_dict())) == _stable_hash(_normalize(doc)):
                            skipped += 1
                            continue
                except: pass

            batch.set(doc_ref, doc)
            written += 1
            count_in_batch += 1

            if count_in_batch >= MAX_BATCH:
                self._commit_with_retry(batch)
                batch = self.client.batch()
                count_in_batch = 0

        if count_in_batch > 0:
            self._commit_with_retry(batch)

        return written, skipped