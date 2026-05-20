#!/usr/bin/env python3
"""Fetch all faculty profile URLs from the Fred Hutch faculty directory."""

import json
import base64
import sys
import urllib.request


def fetch_faculty_urls():
    query = json.dumps({
        "type": "faculty",
        "keywords": "",
        "filters": [],
        "limit": 9999,
        "offset": 0,
        "sortDesc": "false",
        "currentPagePath": ""
    })
    encoded = base64.b64encode(query.encode()).decode()

    url = f"https://www.fredhutch.org/bin/fhcrc/faculty-labs?q={encoded}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.fredhutch.org/en/faculty-lab-directory.html"
    })

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    if not data.get("success"):
        print("Error: API returned unsuccessful response", file=sys.stderr)
        sys.exit(1)

    for entry in data["data"]:
        path = entry["path"]
        if not path.endswith(".html"):
            path += ".html"
        print(f"https://www.fredhutch.org{path}")

    print(f"Total: {len(data['data'])} faculty URLs", file=sys.stderr)


if __name__ == "__main__":
    fetch_faculty_urls()
