"""What's in a wheel?    uv run inside.py dist/*.whl"""

import sys
import zipfile
from email.parser import Parser

SHOWN = {"Name", "Version", "Requires-Python", "Requires-Dist", "License-Expression"}

for path in sys.argv[1:]:
    with zipfile.ZipFile(path) as wheel:
        files = [item for item in wheel.infolist() if not item.is_dir()]
        print(f"{path}\n")
        for item in files:
            print(f"  {item.file_size:>6,}  {item.filename}")
        total = sum(item.file_size for item in files)
        print(f"  {total:>6,} bytes, in {len(files)} files\n")

        (metadata,) = [item for item in files if item.filename.endswith("/METADATA")]
        message = Parser().parsestr(wheel.read(metadata).decode("utf-8"))
        for name, value in message.items():
            if name in SHOWN:
                print(f"  {name + ':':<20}{value}")
        words = len((message.get_payload() or "").split())
        print(f"  ... and a README of {words} words")
