import xml.etree.ElementTree as ET

def load_map_from_svg(filename, width, height, tile_size):
    tree = ET.parse(filename)
    root = tree.getroot()

    # Inicializar mapa vacío
    map_data = [[0 for _ in range(width)] for _ in range(height)]

    # Buscar rectángulos
    for rect in root.findall(".//{http://www.w3.org/2000/svg}rect"):
        x = int(float(rect.get("x", 0))) // tile_size
        y = int(float(rect.get("y", 0))) // tile_size
        fill = rect.get("fill")

        if fill == "#0000ff":  # Agua
            map_data[y][x] = 1
        elif fill == "#8B4513":  # Puerta (ejemplo)
            map_data[y][x] = 6

    return map_data