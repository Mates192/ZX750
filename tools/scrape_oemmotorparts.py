#!/usr/bin/env python3
"""Scrape OEMMotorparts model + drawing pages for Kawasaki part metadata.

Usage:
  python tools/scrape_oemmotorparts.py \
    --model-url "https://www.oemmotorparts.com/en/model/kawasaki/zx-750-a-gpz-750-a1-a2-gpz-750/1983" \
    --out-dir data/raw/oemmotorparts \
    --json-out data/processed/zx750a1_parts.json

Notes:
- Uses only Python stdlib (urllib + regex) to avoid dependency setup.
- Saves raw HTML and a normalized JSON output.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


@dataclass
class PartRecord:
    source_page: str
    drawing_slug: str
    oem_part_number: str
    name: str
    ref: str


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
        return resp.read().decode("utf-8", errors="replace")


def clean_text(html: str) -> str:
    text = re.sub(r"<script[\\s\\S]*?</script>", " ", html, flags=re.IGNORECASE)
    text = re.sub(r"<style[\\s\\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\s+", " ", text)
    return text.strip()


def extract_drawing_links(model_url: str, html: str) -> list[str]:
    links = set()
    patterns = [
        r'href="(/en/model/[^\"]+/drawing/[^\"]+)"',
        r'href="(/en/genuine-oem/[^\"]+)"',
    ]
    for pattern in patterns:
        for match in re.findall(pattern, html):
            abs_url = urllib.parse.urljoin(model_url, match)
            links.add(abs_url)
    return sorted(links)


def extract_records(page_url: str, html: str) -> list[PartRecord]:
    text = clean_text(html)
    drawing_slug = page_url.rstrip("/").split("/")[-1]

    records: list[PartRecord] = []

    triplet_pattern = re.compile(
        r"([0-9]{5}[A-Z]?)\s+[^0-9]{0,80}?([0-9]{5}-[0-9A-Z]{3,5})\s+([A-Z0-9,#\-\\(\\)\\.\s]{3,80})",
        flags=re.IGNORECASE,
    )
    for ref, pn, name in triplet_pattern.findall(text):
        name = re.sub(r"\\s+", " ", name).strip(" -")
        if len(name) < 3:
            continue
        records.append(
            PartRecord(
                source_page=page_url,
                drawing_slug=drawing_slug,
                oem_part_number=pn.upper(),
                name=name,
                ref=ref.upper(),
            )
        )

    # Fallback based on explicit "Kawasaki OEM: XXXXX-XXXX" snippets.
    oem_pattern = re.compile(r"Kawasaki OEM:\s*([0-9]{5}-[0-9A-Z]{3,5})", flags=re.IGNORECASE)
    for pn in oem_pattern.findall(text):
        records.append(
            PartRecord(
                source_page=page_url,
                drawing_slug=drawing_slug,
                oem_part_number=pn.upper(),
                name="UNKNOWN_FROM_SCRAPE",
                ref="UNKNOWN",
            )
        )

    dedup: dict[tuple[str, str], PartRecord] = {}
    for record in records:
        key = (record.oem_part_number, record.ref)
        if key not in dedup:
            dedup[key] = record
    return sorted(dedup.values(), key=lambda r: (r.oem_part_number, r.ref))


def to_domain_part(record: PartRecord) -> dict:
    part_id = f"zx750a1-{record.oem_part_number.lower().replace('-', '')}"
    return {
        "id": part_id,
        "name": record.name,
        "description": "Imported from OEM parts catalog",
        "oemPartNumber": record.oem_part_number,
        "assemblyId": record.drawing_slug,
        "modelNodeName": "TODO_MAP_NODE_NAME",
        "modelUri": "TODO_MAP_MODEL_URI",
        "source": record.source_page,
        "reference": record.ref,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-url", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--delay-sec", type=float, default=0.4)
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_html = fetch(args.model_url)
    except urllib.error.URLError as exc:
        print(f"ERROR: Cannot download model URL: {args.model_url}")
        print(f"DETAIL: {exc}")
        return 2
    (out_dir / "model_page.html").write_text(model_html, encoding="utf-8")

    drawing_links = extract_drawing_links(args.model_url, model_html)

    all_records: list[PartRecord] = []
    for idx, drawing_url in enumerate(drawing_links, start=1):
        try:
            html = fetch(drawing_url)
        except urllib.error.URLError as exc:
            print(f"WARN: Skipping drawing URL due to download error: {drawing_url}")
            print(f"DETAIL: {exc}")
            continue
        filename = f"drawing_{idx:03d}.html"
        (out_dir / filename).write_text(html, encoding="utf-8")
        all_records.extend(extract_records(drawing_url, html))
        time.sleep(args.delay_sec)

    dedup: dict[tuple[str, str, str], PartRecord] = {}
    for rec in all_records:
        key = (rec.oem_part_number, rec.ref, rec.drawing_slug)
        if key not in dedup:
            dedup[key] = rec

    parts = [to_domain_part(rec) for rec in sorted(dedup.values(), key=lambda r: (r.drawing_slug, r.oem_part_number, r.ref))]

    output = {
        "sourceModelUrl": args.model_url,
        "generatedAtEpoch": int(time.time()),
        "drawingCount": len(drawing_links),
        "partCount": len(parts),
        "parts": parts,
    }

    json_path = pathlib.Path(args.json_out)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Saved {len(drawing_links)} drawings, {len(parts)} parts -> {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
