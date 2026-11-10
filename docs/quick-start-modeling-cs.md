# Stručný návod: od CAD modelu k appce

## 1) Vytvoř díl (Inventor / FreeCAD)
- Modeluj 1 díl = 1 soubor.
- Drž reálné měřítko (mm), správnou orientaci os a pivot do místa montáže.

## 2) Exportuj model
- Preferovaný runtime formát pro appku: **GLB**.
- Pokud CAD neumí GLB přímo: export STEP/OBJ -> převod v Blenderu do GLB.

## 3) Kam soubor uložit
- Do app assets podle podsestavy:
  - `app/src/main/assets/models/parts/engine/13095-XXXX.glb`
  - `app/src/main/assets/models/parts/front_brake/43041-XXXX.glb`
- Název souboru ideálně podle OEM čísla dílu.

## 4) Doplň metadata
Do `app/src/main/assets/metadata/zx750a1_parts.json` přidej záznam:

```json
{
  "id": "zx750a1-13095xxxx",
  "oemPartNumber": "13095-XXXX",
  "name": "CLUTCH BASKET",
  "assemblyId": "engine-clutch",
  "modelNodeName": "ZX750A1_ENGINE_CLUTCH_BASKET_001",
  "modelUri": "models/parts/engine/13095-XXXX.glb"
}
```

## 5) Pokud skládáš celou motorku
- Full model dej do:
  - `app/src/main/assets/models/assemblies/full_bike/zx750a1_full.glb`
- Scénový manifest drž v:
  - `app/src/main/assets/scenes/zx750a1_scene_manifest.json`

## 6) Co udělat hned po uložení
- Ověř, že se model otevře v glTF vieweru.
- Zkontroluj počet polygonů (mobilně drž rozumný budget).
- Zkontroluj, že `modelUri` a `modelNodeName` sedí na skutečný GLB.
