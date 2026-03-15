CELDA_PX  = 12
GRID_COLS = 80
GRID_ROWS = 65
GRID_W    = GRID_COLS * CELDA_PX
GRID_H    = GRID_ROWS * CELDA_PX
HUD_W     = 290
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
    0: (180, 140,  20),
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
}

C = {
    "bg":           ( 13,  14,  23),   # near-black, blue tint
    "panel":        ( 18,  20,  34),
    "card":         ( 25,  28,  48),   # dark blue-grey
    "card_border":  ( 52,  58,  92),   # subtle, not loud
    "accent":       (139, 233, 253),   # Dracula cyan
    "accent2":      ( 80, 250, 123),   # Dracula green
    "divider":      ( 40,  46,  74),
    "txt_hi":       (248, 248, 242),   # near-white — max legibility
    "txt_mid":      (189, 196, 224),   # medium grey-blue
    "txt_dim":      (130, 142, 182),   # was (80,92,148) — much more readable
    "energy_hi":    ( 80, 250, 123),   # Dracula green
    "energy_mid":   (255, 184, 108),   # Dracula orange
    "energy_lo":    (255,  85,  85),   # Dracula red
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
}

CROP_PHASE_LABELS = {0: "Semilla", 1: "Creciendo", 2: "Lista"}
CROP_PHASE_COLORS = {0: (180, 140, 20), 1: (80, 200, 80), 2: (255, 80, 80)}
