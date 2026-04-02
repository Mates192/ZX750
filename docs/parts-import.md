# Import part listu pro ZX750 A1 (OEMMotorparts)

Cíl: mít part listy lokálně a distribuovat je přímo s aplikací.

## Co je připravené

- `tools/scrape_oemmotorparts.py`
  - stáhne model URL,
  - najde odkazy na jednotlivé výkresy (`/drawing/...`),
  - uloží raw HTML (pro audit/debug),
  - vytáhne part čísla a názvy,
  - vyrobí normalizovaný JSON pro entity `Part`.
- `tools/bundle_parts_to_assets.py`
  - vezme normalizovaný JSON,
  - uloží ho do `app/src/main/assets/parts/...`,
  - díky tomu se dataset distribuuje přímo s APK/AAB.
- `app/src/main/assets/parts/zx750a1_1983_drawings.json`
  - offline seed index 61 výkresů (kategorie + počet položek),
  - můžeš používat hned, i bez online fetch.

## Spuštění (full import + bundling)

```bash
python tools/scrape_oemmotorparts.py \
  --model-url "https://www.oemmotorparts.com/en/model/kawasaki/zx-750-a-gpz-750-a1-a2-gpz-750/1983" \
  --out-dir data/raw/oemmotorparts \
  --json-out data/processed/zx750a1_parts.json

python tools/bundle_parts_to_assets.py \
  --input-json data/processed/zx750a1_parts.json \
  --asset-path app/src/main/assets/parts/zx750a1_parts.json
```

## Výstupy

- `data/raw/oemmotorparts/model_page.html`
- `data/raw/oemmotorparts/drawing_*.html`
- `data/processed/zx750a1_parts.json`
- `app/src/main/assets/parts/zx750a1_parts.json` (pro distribuci v appce)

## Napojení do Android app

1. Číst asset soubor při prvním startu appky.
2. Naimportovat do Room (`Part`, `Assembly`, `PartRelation`).
3. Použít `modelNodeName` pro mapování raycast výběru z GLB na detail dílu.

## Poznámka k prostředí

V tomto CI/container prostředí je přímé stažení z OEMMotorparts blokované proxy tunelem (`403 Forbidden`).
Importer i tak zůstává připravený pro běh v běžném lokálním prostředí (u tebe na PC / build runneru bez blokace).
