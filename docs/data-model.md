# Datový model pro díly a vazby

## Entity `Part`

- `id` (string, interní ID)
- `name` (string)
- `description` (string)
- `oemPartNumber` (string)
- `assemblyId` (string)
- `modelNodeName` (string)
- `modelUri` (string)
- `thumbnailUri` (string?)
- `tags` (array<string>)
- `updatedAt` (datetime)

## Entity `PartRelation`

- `id`
- `sourcePartId`
- `targetPartId`
- `relationType` (enum):
  - `ATTACHED_TO`
  - `CONTAINS`
  - `REQUIRES_FOR_REMOVAL`
  - `ELECTRICALLY_CONNECTED_TO`

## Entity `Assembly`

- `id`
- `name`
- `parentAssemblyId` (nullable)
- `orderIndex`

## Základní JSON příklad

```json
{
  "part": {
    "id": "zx750a1-front-brake-caliper-l",
    "name": "Front Brake Caliper Left",
    "description": "Levá přední brzdičová jednotka",
    "oemPartNumber": "43041-XXXX",
    "assemblyId": "front-brake",
    "modelNodeName": "ZX750A1_FRONT_BRAKE_CALIPER_L_001",
    "modelUri": "models/front_brake.glb"
  },
  "relations": [
    {
      "sourcePartId": "zx750a1-front-brake-caliper-l",
      "targetPartId": "zx750a1-front-fork-l",
      "relationType": "ATTACHED_TO"
    }
  ]
}
```

