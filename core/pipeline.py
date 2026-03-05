# core/pipeline.py

class Pipeline:
    def __init__(self, *steps):
        # Pedro: Limpiar comentarios de tipo <cite> o similares
        self.steps = list(steps)

    def run(self, state):
        """
        Ejecuta los pasos de procesamiento y actualiza el estado de la granja.
        """
        # 1. Ejecutamos los pasos lógicos (movimiento, recolección, etc.)
        for step in self.steps:
            state = step(state)
        
        # 2. Pedro: "método actualizar()" en animales
        # Aquí es donde hacemos que el hambre de los animales aumente
        if hasattr(state, 'animales'):
            for animal in state.animales:
                animal.actualizar()
                
        return state