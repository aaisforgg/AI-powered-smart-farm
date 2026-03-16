CELDA_PX  = 12
GRID_COLS = 80
GRID_ROWS = 65
GRID_W    = GRID_COLS * CELDA_PX
GRID_H    = GRID_ROWS * CELDA_PX
HUD_W     = 340
WINDOW_W  = GRID_W + HUD_W
WINDOW_H  = GRID_H

COLORES = {
    "pasto":      (118, 186,  27),
    "agua":       ( 74, 163, 223),
    "acantilado": (142, 112,  72),
    "edificio":   (180,  70,  50),
    "cultivo":    (220, 190,  50),
    "puente":     (150, 100,  50),
    "puerta":     (200, 160,  80),
    "casa":       (200, 200, 255),
}

CROP_COLORS = {
    0: ( 72,  35,  10),   # marrón oscuro — semilla
    1: ( 80, 200,  80),
    2: (255,  80,  80),
}

SEASON_TINTS = {
    "Invierno":  (150, 200, 255,  60),
    "Verano":    (255, 200,   0,  25),
    "Otoño":     (180, 100,   0,  40),
    "Primavera": (  0, 200,  80,  15),
}

EVENT_TINTS = {
    "sequia":             (180,  80,   0,  60),
    "tormenta":           ( 50,  50, 150,  80),
    "nevada":             (200, 200, 255,  70),
    "inundacion":         (  0,  50, 180,  70),
    "plaga":              (  0, 150,   0,  60),
    "gran_deslave":       (100,  60,   0,  80),
    "nevada_paralizante": (200, 200, 255, 110),
    "plaga_de_insectos":  (  0, 180,   0,  80),
    "lluvia_suave":       (100, 150, 255,  30),
    "sol_ideal":          (255, 230, 100,  25),
    "cosecha_doble":      (255, 200,  50,  20),
}

C = {
    "bg": (245, 226, 182),        # Fondo crema (se mantiene)
    "divider": (140, 100, 60),    # Más oscuro para definir mejor los límites

    "accent": (45, 100, 45),      # Verde bosque profundo (en lugar de verde claro)
    "accent2": (160, 80, 0),      # Ocre quemado para resaltar sobre el crema

    "txt_hi": (40, 25, 15),       # Casi negro/café muy oscuro para máxima lectura
    "txt_mid": (80, 55, 35),      # Café medio
    "txt_dim": (110, 85, 65),     # Grisáceo oscuro

    "energy_hi": (30, 130, 50),   # Verde vibrante pero oscuro
    "energy_mid": (180, 120, 0),  # Ámbar oscuro
    "energy_lo": (180, 40, 40)    # Rojo sangre para alertar
}

SEASON_COLORS = {
    "Primavera": (30, 150, 60),   # Verde esmeralda
    "Verano":    (200, 140, 0),   # Dorado oscuro
    "Otoño":     (160, 60, 20),   # Terracota
    "Invierno":  (50, 100, 160),  # Azul acero (el azul claro se pierde en crema)
}

EVENT_COLORS = {
    "sequia":             (150, 70, 0),    # Café rojizo
    "tormenta":           (40, 60, 150),   # Azul profundo
    "nevada":             (80, 120, 160),  # Azul grisáceo
    "inundacion":         (0, 80, 180),    # Azul fuerte
    "plaga":              (60, 110, 30),   # Verde oliva oscuro
    "gran_deslave":       (100, 50, 20),   # Marrón oscuro
    "nevada_paralizante": (60, 90, 130),   # Azul sombra
    "plaga_de_insectos":  (80, 130, 20),   # Verde tóxico oscuro
    "lluvia_suave":       (70, 130, 180),  # Cerúleo
    "sol_ideal":          (170, 130, 0),   # Mostaza
    "cosecha_doble":      (180, 90, 0),    # Naranja oscuro
}

GOAL_LABELS = {
    "HARVEST":  "Cosechar",
    "WATER":    "Regar",
    "PLANT":    "Plantar",
    "EXPLORE":  "Explorar",
    "REST":     "Descansar",
    "GO_HOME":  "Ir a casa",
    None:       "—",
}

EVENT_LABELS = {
    "sequia":             "Sequía",
    "tormenta":           "Tormenta",
    "nevada":             "Nevada",
    "inundacion":         "Inundación",
    "plaga":              "Plaga",
    "gran_deslave":       "Deslave",
    "nevada_paralizante": "Nevada intensa",
    "plaga_de_insectos":  "Plaga de insectos",
    "lluvia_suave":       "Lluvia suave",
    "sol_ideal":          "Sol ideal",
    "cosecha_doble":      "Cosecha doble",
}

CROP_PHASE_LABELS = {0: "Semilla", 1: "Creciendo", 2: "Lista"}
CROP_PHASE_COLORS = {
    0: (100, 70, 20),    # Semilla: Marrón tierra (contrasta con el crema)
    1: (40, 140, 40),    # Creciendo: Verde medio
    2: (200, 20, 20)     # Listo: Rojo vibrante (muy fácil de distinguir)
}

OBSTACLE_COLORS = {
    "nieve":    (200, 230, 255),   # azul hielo claro
    "charco":   ( 20,  80, 210),   # azul marino brillante
    "escombro": (190, 140,  60),   # naranja-marrón cálido
    "lodo":     ( 70,  40,  10),   # marrón muy oscuro
}

OBSTACLE_BORDER_COLORS = {
    "nieve":    (120, 170, 230),   # azul medio
    "charco":   (  0,  40, 160),   # azul oscuro
    "escombro": (130,  80,  20),   # naranja quemado
    "lodo":     (140,  90,  40),   # marrón claro contraste
}
