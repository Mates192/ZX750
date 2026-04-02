# ZX750 A1 3D Explorer (Android)

Tento repozitář obsahuje návrh startu projektu Android aplikace pro 3D rozpad/sestavu motorky Kawasaki ZX750 A1.

## Co zde najdeš

- `docs/architecture.md` — doporučená architektura aplikace, technologický stack, UX tok.
- `docs/pipeline.md` — end-to-end pipeline pro 3D modely (skenování/modelování, optimalizace, metadata, export).
- `docs/data-model.md` — návrh datového modelu pro díly, vazby mezi díly a vyhledávání.
- `docs/roadmap.md` — praktický plán kroků od nuly do prvního použitelného prototypu.

## První doporučení

1. Začni vytvořením **MVP datasetu**: 20–30 nejdůležitějších dílů (motor, rám, kola, brzdy).
2. Paralelně nastav Android projekt se SceneView + Filament.
3. U každého dílu drž stejnou strukturu: `3D model + metadata + vazby`.
4. Teprve pak škáluj na celý motocykl.

