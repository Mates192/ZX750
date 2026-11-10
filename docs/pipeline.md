# Pipeline pro získání a zpracování 3D modelů

## Doporučení: kombinovaný přístup

Pro ZX750 A1 doporučuji nevsadit vše na jedinou metodu.

### 1) CAD/parametrické modelování (priorita pro přesnost)

Vhodné pro díly, kde potřebuješ:
- přesné rozměry,
- čisté hrany,
- budoucí export výkresů nebo výrobu/repliky.

Nástroje: Fusion 360, SolidWorks, FreeCAD, Onshape.

### 2) Fotogrammetrie / 3D scan (priorita pro rychlý sběr tvarů)

Vhodné pro:
- organičtější tvary,
- plasty, odlitky, detaily bez původní dokumentace.

Nástroje: RealityCapture, Metashape, Polycam, případně mobilní LiDAR.

### 3) Gaussian Splatting (doplněk, ne hlavní master formát)

Výborné pro fotorealistickou prezentaci, ale slabší pro:
- přesný picking jednotlivých technických dílů,
- čistou topologii,
- standardní CAD metadata.

**Doporučení**: Gaussian splat použít jako prezentační vrstvu (např. showroom), ale pro interaktivní servisní aplikaci držet hlavní pipeline v mesh + metadata (glTF).

## Master asset workflow

1. **Sběr dat**
   - fotky/skany + měření + servisní manuály + katalog dílů.
2. **Rekonstrukce/modelování**
   - vznikne high-poly master.
3. **Retopologie + UV**
   - low-poly pro mobilní rendering.
4. **Baking map**
   - normal/AO/roughness z high-poly na low-poly.
5. **Material setup (PBR)**
6. **Rozsekání podle logických dílů**
   - každý díl musí mít stabilní `part_id`.
7. **Pojmenování node konvencí**
   - např. `ZX750A1_ENGINE_CLUTCH_BASKET_001`.
8. **Export do GLB**
9. **Validace**
   - velikost, orientace os, pivoty, poly budget, textury.
10. **Registrace metadat**
   - mapování na PN, popis, vazby.

## Naming konvence (minimum)

- `part_id`: interní stabilní ID
- `oem_part_number`: originální výrobní číslo
- `assembly_id`: podsestava
- `node_name`: jméno uzlu v GLB

Příklad:
- `part_id`: `zx750a1-eng-clutch-basket`
- `oem_part_number`: `13095-XXXX`
- `assembly_id`: `engine-clutch`
- `node_name`: `ZX750A1_ENGINE_CLUTCH_BASKET_001`

