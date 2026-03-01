# core/logic.py

def calcular_costo_movimiento_total(state, x, y):
    """
    Esta función reemplaza tu antiguo método. 
    Toma el costo del terreno del mapa y lo multiplica por la carga del granjero.
    """
    # 1. Obtenemos el nodo del grid
    nodo = state.grid[x][y]
    
    # 2. Si no es caminable, el costo es infinito
    if not nodo.walkable:
        return float('inf')
    
    # 3. Factor Terreno (Ya viene pre-configurado en el nodo)
    multiplicador_suelo = nodo.cost
    
    # 4. Factor Peso (Lógica de inventario)
    # Asumimos una capacidad máxima (ej. 100)
    capacidad_max = 100.0 
    peso_total = sum(item.peso for item in state.farmer_inventory)
    factor_carga = 1 + (peso_total / capacidad_max)
    
    # Resultado final
    return 1.0 * multiplicador_suelo * factor_carga