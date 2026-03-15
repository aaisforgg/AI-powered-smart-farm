# Assets

Coloca las imágenes aquí. Si no están, el juego usa colores sólidos como fallback.

## Tiles (assets/tiles/)
- `grass.png` — pasto
- `water.png` — agua
- `cliff.png` — acantilado
- `building.png` — edificio
- `farmland.png` — tierra de cultivo
- `bridge.png` — puente
- `door.png` — puerta
- `house.png` — casa

Tamaño recomendado: 12×12 px o múltiplo (se escala automáticamente).

## Crops (assets/crops/)
- `seed.png` — semilla (fase 0)
- `growing.png` — creciendo (fase 1)
- `ready.png` — listo para cosechar (fase 2)

Tamaño recomendado: 8×8 px (se escala a cell_size - 4).

## Agent (assets/agent/)
- `farmer.png` — sprite del agente

## Notas
- `AssetManager` carga estas imágenes una vez al inicio (`rendering/asset_manager.py`).
- Si un archivo no existe, el renderer usa el fallback de colores sólidos.
- Los archivos JPEG del mapa son assets de referencia del diseño original, no se usan en el rendering actual.
