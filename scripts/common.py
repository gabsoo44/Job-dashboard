"""Shared helpers: paths, normalization, status rules, encrypted store."""
import base64
import json
import os
import re
import unicodedata
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = Path(__file__).resolve().parent.parent
STORE_FILE = ROOT / "web" / "data" / "store.enc.json"
PBKDF2_ITERATIONS = 250_000

STATUSES = [
    "Offre", "Entretien", "En cours", "À relancer", "Relancée",
    "Envoyée", "Sans réponse", "Refus", "Incomplète",
]

# Status set by a classified email event
EVENT_STATUS = {
    "interview": "Entretien",
    "offer": "Offre",
    "rejection": "Refus",
    "viewed": "En cours",
    "recruiter_message": "En cours",
    "incomplete": "Incomplète",
    "confirmation": "Envoyée",
}

# Statuses that automatic escalation (7 d / 21 d without news) may touch
ESCALATABLE = {"Envoyée", "À relancer"}

EMPTY_STORE = {
    "generated_at": None,
    "applications": [],
    "overrides": {},
    "state": {"last_sync": None, "processed_ids": []},
}


def _b64(data):
    return base64.b64encode(data).decode()


def _key(password, salt, iterations):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    return kdf.derive(password.encode())


def load_store(password):
    """Decrypt web/data/store.enc.json (AES-256-GCM, PBKDF2) or return an empty store."""
    if not STORE_FILE.exists():
        return json.loads(json.dumps(EMPTY_STORE))
    blob = json.loads(STORE_FILE.read_text(encoding="utf-8"))
    key = _key(password, base64.b64decode(blob["salt"]), blob["iter"])
    plain = AESGCM(key).decrypt(base64.b64decode(blob["iv"]), base64.b64decode(blob["ct"]), None)
    return json.loads(plain)


def save_store(store, password):
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(_key(password, salt, PBKDF2_ITERATIONS)).encrypt(
        iv, json.dumps(store, ensure_ascii=False).encode(), None)
    STORE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STORE_FILE.write_text(json.dumps(
        {"v": 1, "iter": PBKDF2_ITERATIONS, "salt": _b64(salt), "iv": _b64(iv), "ct": _b64(ct)}) + "\n",
        encoding="utf-8")


def norm(text):
    """Lowercase, strip accents/H-F/contract tags and suffixes, for dedup keys."""
    t = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"\(?\b[hf]\s*/\s*[hf]\b\)?", " ", t)
    t = re.sub(r"\b(cdi|cdd|stage|alternance)\b", " ", t)
    t = re.split(r"\s-\s|\(", t)[0]
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def app_id(company, title):
    return f"{norm(company)}|{norm(title)}".replace(" ", "-")
