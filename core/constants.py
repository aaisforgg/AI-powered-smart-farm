"""Constantes globales de simulación compartidas entre módulos."""

# Cuántos ticks de simulación conforman un día de juego.
# A 15 FPS: 1 día ≈ 0.67s real. A 6 FPS (descanso): 1 día ≈ 1.67s real.
TICKS_PER_DAY = 10

# Días de descanso máximo al recargar energía
REST_DAYS = 3

# Ticks totales de descanso (3 días × 15 ticks)
REST_TICKS_MAX = REST_DAYS * TICKS_PER_DAY
