"""
Firestore configuration and client setup.

This version does NOT use environment variables.
It directly loads the firebase-key.json file from the config folder.
"""

from __future__ import annotations

import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Absolute path to firebase-key.json
SERVICE_ACCOUNT_PATH = (
    Path(__file__).resolve().parents[3] / "firebase" / "config" / "firebase-key.json"
)

_FIRESTORE_CLIENT = None


def get_firestore_client() -> firestore.Client:
    """Initialize and return a single Firestore client instance."""
    global _FIRESTORE_CLIENT

    if _FIRESTORE_CLIENT is not None:
        return _FIRESTORE_CLIENT

    if not SERVICE_ACCOUNT_PATH.exists():
        raise FileNotFoundError(f"Firebase key not found at: {SERVICE_ACCOUNT_PATH}")

    cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    _FIRESTORE_CLIENT = firestore.client()
    return _FIRESTORE_CLIENT
