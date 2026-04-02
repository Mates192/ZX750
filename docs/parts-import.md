# Import part listu pro ZX750 A1 (OEMMotorparts)

Ano — je to implementované jako skript, který stáhne model stránku + všechny drawing stránky a vyrobí JSON připravený pro naši datovou vrstvu.

## Co je připravené

- `tools/scrape_oemmotorparts.py`
  - stáhne model URL,
  - najde odkazy na jednotlivé výkresy (`/drawing/...`),
  - uloží raw HTML (pro audit/debug),
  - vytáhne part čísla a názvy,
  - vyrobí normalizovaný JSON pro entity `Part`.

## Spuštění

```bash
python tools/scrape_oemmotorparts.py \
  --model-url "https://www.oemmotorparts.com/en/model/kawasaki/zx-750-a-gpz-750-a1-a2-gpz-750/1983" \
  --out-dir data/raw/oemmotorparts \
  --json-out data/processed/zx750a1_parts.json
```

## Výstupy

- `data/raw/oemmotorparts/model_page.html`
- `data/raw/oemmotorparts/drawing_*.html`
- `data/processed/zx750a1_parts.json`

## Napojení do aplikace

1. `zx750a1_parts.json` importovat do Room (`Part`, `Assembly`).
2. Pro každý díl doplnit mapování:
   - `modelNodeName` (uzel v GLB),
   - `modelUri` (cesta na GLB/podsestavu).
3. V aplikaci udělat lookup:
   - raycast `node_name` -> `Part` podle `modelNodeName`.

## Poznámka k robustnosti

Markup e-shopu se může měnit. Proto se ukládá raw HTML a skript je dělený na malé funkce (`extract_drawing_links`, `extract_records`) pro snadnou úpravu parseru.
