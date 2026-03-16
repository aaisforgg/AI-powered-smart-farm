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
    "bg": (245, 226, 182),
    "divider": (170, 120, 80),
    "accent": (120, 170, 90),
    "accent2": (210, 160, 80),

    "txt_hi": (70,50,30),
    "txt_mid": (100,80,50),
    "txt_dim": (140,110,70),

    "energy_hi": (90,190,90),
    "energy_mid": (230,180,80),
    "energy_lo": (200,90,90)
}

SEASON_COLORS = {
    "Primavera": ( 80, 220, 100),
    "Verano":    (255, 200,  50),
    "Otoño":     (220, 120,  40),
    "Invierno":  (150, 200, 255),
}

EVENT_COLORS = {
    "sequia":             (220, 100,  40),
    "tormenta":           (100, 120, 255),
    "nevada":             (180, 210, 255),
    "inundacion":         ( 50, 130, 220),
    "plaga":              ( 80, 200,  80),
    "gran_deslave":       (150, 100,  50),
    "nevada_paralizante": (200, 220, 255),
    "plaga_de_insectos":  (120, 200,  60),
    "lluvia_suave":       (100, 180, 255),
    "sol_ideal":          (255, 220,  80),
    "cosecha_doble":      (255, 200,  50),
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
CROP_PHASE_COLORS = {0: (180, 140, 20), 1: (80, 200, 80), 2: (255, 80, 80)}

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
