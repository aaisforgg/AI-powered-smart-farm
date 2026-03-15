
def calcular_costo_movimiento(grid, x, y):
    """Costo de moverse a la celda (x, y). Retorna inf si no es caminable."""
    nodo = grid[y][x]  # NOTA: grid se indexa [y][x], no [x][y]
    if not nodo.walkable:
        return float('inf')
    return nodo.cost