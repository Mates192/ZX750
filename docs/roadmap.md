# Roadmap (od nuly)

## Fáze 0 — Příprava dat

- Sehnat parts list + servisní manuál pro ZX750 A1.
- Definovat taxonomy podsestav.
- Potvrdit naming konvence.

## Fáze 1 — Android MVP

- Nový Android projekt (Kotlin + Compose).
- Integrace SceneView/Filament.
- Načtení jednoho testovacího GLB.
- Picking dílu a detail panel.

## Fáze 2 — Data vrstva

- Room schéma pro `Part`, `Assembly`, `PartRelation`.
- Import JSON dat.
- Fulltext vyhledávání podle PN/názvu.

## Fáze 3 — Viewer funkce

- Exploded view.
- Zobrazení vazeb (graph highlight).
- Režim krokové demontáže/montáže.

## Fáze 4 — Produkční pipeline

- LOD strategie.
- Texture compression.
- Asset versioning + CI validace.

## Fáze 5 — Škálování katalogu

- Pokrytí 100 % dílů ZX750 A1.
- QA kontrola PN, umístění, vazeb.
- Beta test na reálných zařízeních.

