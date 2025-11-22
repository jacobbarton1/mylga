import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

from django.conf import settings


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def generate_login_token(email: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    expiry_seconds = settings.EMAIL_LOGIN_JWT_EXPIRY_DAYS * 24 * 60 * 60
    payload: Dict[str, Any] = {
        "sub": email,
        "iat": now,
        "exp": now + expiry_seconds,
        "scope": "email_login",
    }

    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        signing_input,
        hashlib.sha256,
    ).digest()
    signature_b64 = _b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


class InvalidToken(Exception):
    pass


def verify_login_token(token: str) -> str:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise InvalidToken("Malformed token") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_sig = hmac.new(
        settings.SECRET_KEY.encode(),
        signing_input,
        hashlib.sha256,
    ).digest()
    actual_sig = _b64url_decode(signature_b64)

    if not hmac.compare_digest(expected_sig, actual_sig):
        raise InvalidToken("Invalid signature")

    try:
        payload_raw = _b64url_decode(payload_b64)
        payload: Dict[str, Any] = json.loads(payload_raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise InvalidToken("Invalid payload") from exc

    if payload.get("scope") != "email_login":
        raise InvalidToken("Invalid scope")

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        raise InvalidToken("Token expired")

    email = payload.get("sub")
    if not isinstance(email, str):
        raise InvalidToken("Invalid subject")

    return email


