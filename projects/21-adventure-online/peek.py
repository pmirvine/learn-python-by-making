"""Read a Flask session cookie, without knowing the secret key."""

import base64
import json
import sys
import zlib

cookie = sys.argv[1]
squashed = cookie.startswith(".")
payload, stamp, signature = cookie.lstrip(".").split(".")

data = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
if squashed:
    data = zlib.decompress(data)

print(json.dumps(json.loads(data), indent=2))
print(f"\nThe signature, which you can't forge without the key: {signature}")
