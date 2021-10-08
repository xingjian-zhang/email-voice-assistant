"""Backend development configuration."""

import pathlib

BACKEND_ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN_DIR = BACKEND_ROOT / "backend" / "token"
TOKEN_FILE = TOKEN_DIR / "token.json"
CREDENTIALS_FILE = TOKEN_DIR / "credentials.json"
NLP_SERVER_URL = None # Need NLP Group's api here, e.g. 172.26.10.187:5000