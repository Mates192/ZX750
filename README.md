# ZX750 A1 3D Explorer (Android)

Tento repozitář obsahuje návrh startu projektu Android aplikace pro 3D rozpad/sestavu motorky Kawasaki ZX750 A1.

## Co zde najdeš

- `docs/architecture.md` — doporučená architektura aplikace, technologický stack, UX tok.
- `docs/pipeline.md` — end-to-end pipeline pro 3D modely (skenování/modelování, optimalizace, metadata, export).
- `docs/data-model.md` — návrh datového modelu pro díly, vazby mezi díly a vyhledávání.
- `docs/roadmap.md` — praktický plán kroků od nuly do prvního použitelného prototypu.
- `docs/parts-import.md` — implementovaný import part listu z OEMMotorparts do JSON.
- `docs/asset-layout.md` — kam ukládat 3D modely dílů, sestavy a metadata v Android app assets.

## První doporučení

1. Začni vytvořením **MVP datasetu**: 20–30 nejdůležitějších dílů (motor, rám, kola, brzdy).
2. Paralelně nastav Android projekt se SceneView + Filament.
3. U každého dílu drž stejnou strukturu: `3D model + metadata + vazby`.
4. Teprve pak škáluj na celý motocykl.


## Import part listu

Připravené skripty (stažení + bundling do assets):

```bash
python tools/scrape_oemmotorparts.py \
  --model-url "https://www.oemmotorparts.com/en/model/kawasaki/zx-750-a-gpz-750-a1-a2-gpz-750/1983" \
  --out-dir data/raw/oemmotorparts \
  --json-out data/processed/zx750a1_parts.json
```


Dataset pro distribuci s appkou ukládej do `app/src/main/assets/parts/`.


## Prostředí aplikace

Je připravený základ Android projektu (Gradle + app modul + Compose).

- Hlavní modely ukládej do `app/src/main/assets/models/`
- Metadata do `app/src/main/assets/metadata/`
- Scénové manifesty do `app/src/main/assets/scenes/`
