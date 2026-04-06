# Architektura Android aplikace (návrh od nuly)

## Cíl aplikace

Aplikace zobrazí kompletní motocykl Kawasaki ZX750 A1 ve 3D s možností:

- přepínat mezi **celkem / podsestavami / jednotlivými díly**,
- vizuálně vidět, **kde díl patří a na co navazuje**,
- kliknout na díl a zobrazit **detail**: název, popis, výrobní číslo (part number), kompatibilita, poznámky.

## Doporučený technologický stack

- **Android Studio + Kotlin**
- **UI**: Jetpack Compose
- **3D render**: Google Filament přes knihovnu SceneView (Kotlin-friendly)
- **3D formát**: glTF/GLB (standard pro realtime)
- **Lokální data**: Room (cache/offline metadata)
- **Backend (volitelně v MVP lokálně)**: Firebase / Supabase / vlastní API

## Proč glTF/GLB

- Podporuje materiály, hierarchy (nodes), animace i metadata extension.
- Dobrá podpora v mobile runtime (Filament).
- Jednoduchá distribuce (`.glb` = jeden binární soubor).

## Vysoká architektura modulů

1. `app` (UI, navigace)
2. `feature-viewer` (3D scéna, výběr dílu, exploded view)
3. `feature-part-detail` (detail dílu)
4. `data-model` (Room entities, repositories)
5. `data-remote` (sync metadat/modelů)
6. `domain` (use-cases: load assembly, highlight part, find dependencies)

## Interakce v 3D scéně

- Tap na mesh -> raycast -> node id.
- Node id mapovat na `part_id`.
- Zvýraznění dílu (outline / emissive boost / ghost okolí).
- Volitelný režim:
  - **Exploded view** (odsazení dílů podle osy),
  - **Dependency mode** (zvýrazni nadřazené/podřazené vazby),
  - **Step-by-step assembly**.

## Výkonové cíle (mobil)

- Cíl 60 FPS na střední třídě, minimum 30 FPS.
- Jednotlivé scény držet ideálně do ~150k–300k triangles (podle zařízení).
- Použít LOD (Level of Detail): LOD0 detail, LOD1/2 pro vzdálené zobrazení.
- Textury preferovat KTX2/BasisU kompresi.

## Návrh navigace

- Dashboard
  - Vyhledávání dílu (PN/název)
  - Kategorie (motor, rám, elektro...)
- 3D Viewer
  - Full assembly / podsestava
  - Výběr dílu
- Detail dílu
  - Popis
  - Výrobní číslo
  - Vazby (kam patří, co drží)
  - Galerie / poznámky / servisní data

