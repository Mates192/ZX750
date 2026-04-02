#!/usr/bin/env python3
"""Copy normalized parts JSON into Android assets for app distribution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True, help="Path to normalized parts JSON")
    parser.add_argument(
        "--asset-path",
        default="app/src/main/assets/parts/zx750a1_parts.json",
        help="Destination file inside Android assets",
    )
    args = parser.parse_args()

    in_path = Path(args.input_json)
    if not in_path.exists():
        print(f"ERROR: Input does not exist: {in_path}")
        return 2

    payload = json.loads(in_path.read_text(encoding="utf-8"))

    out_path = Path(args.asset_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    part_count = len(payload.get("parts", [])) if isinstance(payload, dict) else 0
    print(f"Bundled {part_count} parts into {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
