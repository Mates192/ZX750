# Jak ukládat 3D modely a sestavy (praktický layout)

## 1) Co distribuovat s aplikací

Vše dávej do `app/src/main/assets/`, aby se to zabalilo do APK/AAB:

- `app/src/main/assets/models/assemblies/` — celé sestavy (např. celá motorka, podsestavy)
- `app/src/main/assets/models/parts/` — jednotlivé díly
- `app/src/main/assets/metadata/` — JSON metadata (PN, názvy, vazby, node mapování)
- `app/src/main/assets/scenes/` — manifesty scén (co načíst jako default)

## 2) Doporučená strategie modelů

Použij kombinaci:

1. **Full assembly GLB** (`assemblies`) pro rychlé zobrazení celku.
2. **Part GLB files** (`parts`) pro detail dílů / výměnu / preload jen toho, co je potřeba.
3. **Metadata JSON** pro vazbu mezi klikem v 3D a daty dílu.

## 3) Konvence názvů

- Soubor dílu: ideálně podle OEM čísla, např. `13095-XXXX.glb`
- `part_id`: `zx750a1-13095xxxx`
- `assemblyId`: např. `engine-clutch`
- `modelNodeName`: název node uvnitř full assembly GLB

## 4) Jak skládat sestavy

### Varianta A (doporučené MVP)

- 1 full model: `models/assemblies/full_bike/zx750a1_full.glb`
- JSON metadata mapuje každý node na part data.
- Klik v modelu -> `node_name` -> lookup v metadata.

### Varianta B (pokročilá)

- Full model + separátní part modely.
- Při kliknutí jde načíst samostatný part GLB pro detail/AR/exploded animace.

## 5) Minimální metadata soubor

`app/src/main/assets/metadata/zx750a1_parts.json`

```json
{
  "parts": [
    {
      "id": "zx750a1-13095xxxx",
      "oemPartNumber": "13095-XXXX",
      "name": "CLUTCH BASKET",
      "assemblyId": "engine-clutch",
      "modelNodeName": "ZX750A1_ENGINE_CLUTCH_BASKET_001",
      "modelUri": "models/parts/engine/13095-XXXX.glb"
    }
  ]
}
```

## 6) Co dělat hned teď

1. Ulož full bike model do `models/assemblies/full_bike/`.
2. Připrav první várku 20–30 dílů do `models/parts/`.
3. Vygeneruj `metadata/zx750a1_parts.json` z importeru.
4. Drž konzistentní `modelNodeName` mezi GLB a JSON.
