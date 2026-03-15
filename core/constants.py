"""Constantes globales de simulación compartidas entre módulos."""

# Cuántos ticks de simulación conforman un día de juego.
# A 15 FPS: 1 día = 1 segundo real. A 4 FPS (descanso): 1 día ≈ 3.75 s real.
TICKS_PER_DAY = 15

# Días de descanso máximo al recargar energía
REST_DAYS = 3

# Ticks totales de descanso (3 días × 15 ticks)
REST_TICKS_MAX = REST_DAYS * TICKS_PER_DAY
