import os
import secrets

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(key: str | None = Security(api_key_header)):
    expected = os.environ.get("API_KEY")
    if not expected:
        # Fail closed: never run unprotected because the variable is missing.
        raise HTTPException(status_code=503, detail="API_KEY is not configured on the server")
    if key is None or not secrets.compare_digest(key, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
