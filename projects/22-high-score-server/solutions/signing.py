"""Invent 1: signed scores, so that the server can tell a real game from an impostor.

The game and the server share a secret key. The game sends, with each score, a
signature: a hash of the score *and the key*. Anybody can see the score and the
signature. Nobody can make the signature for a different score without the key.
"""

import hashlib
import hmac
import json


def signature(body: dict[str, object], key: str) -> str:
    """Return the signature for a score, as hexadecimal."""
    message = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(key.encode(), message, hashlib.sha256).hexdigest()


def is_genuine(body: dict[str, object], offered: str, key: str) -> bool:
    """Was this body signed with our key? The comparison takes the same time either way."""
    return hmac.compare_digest(signature(body, key), offered)
