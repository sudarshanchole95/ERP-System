"""
Lightweight validator with per-collection schema hook.
"""
from __future__ import annotations
from typing import Iterable, Mapping, List, Tuple, Callable, Dict

COLLECTION_VALIDATORS: Dict[str, Callable[[Mapping], Tuple[bool, str | None]]] = {}

def register_validator(collection: str, fn: Callable[[Mapping], Tuple[bool, str | None]]):
    COLLECTION_VALIDATORS[collection] = fn

def validate_documents(docs: Iterable[Mapping], collection: str | None = None) -> Tuple[List[Mapping], List[str]]:
    valid = []
    errors = []
    validator = COLLECTION_VALIDATORS.get(collection) if collection else None

    for i, d in enumerate(docs):
        if not isinstance(d, Mapping):
            errors.append(f"doc[{i}] is not a mapping")
            continue
        if validator:
            ok, msg = validator(d)
            if not ok:
                errors.append(f"doc[{i}] validation failed: {msg}")
                continue
        valid.append(d)
    return valid, errors