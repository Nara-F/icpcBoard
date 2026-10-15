#!/usr/bin/env python3
"""Fetch the pinned OFL fonts once; subsequent builds are fully offline."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def install(item):
    path = ROOT / '.fonts' / item['name']
    if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']:
        return
    with urlopen(item['url'], timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        raise RuntimeError(f"Font checksum mismatch: {item['name']}")
    staging = path.with_suffix(path.suffix + '.download')
    staging.write_bytes(data)
    staging.replace(path)
    print('Installed ' + item['name'])


def main():
    (ROOT / '.fonts').mkdir(exist_ok=True)
    manifest = json.loads((ROOT / 'config/fonts.json').read_text())
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(install, manifest))
    print('Verified pinned fonts in .fonts/.')


if __name__ == '__main__':
    main()
