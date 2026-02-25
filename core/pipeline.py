class Pipeline:
    def __init__(self, state):
        self.state = state

    def ejecutar_paso(self, nueva_pos):
        costo = self.state.costo_movimiento(nueva_pos[0], nueva_pos[1])
        
        if self.state.granjero_energia >= costo:
            self.state.granjero_pos = nueva_pos
            self.state.granjero_energia -= costo
            # Actualizar resto del mundo
            for c in self.state.cultivos: c.crecer()
            for a in self.state.animales: a.actualizar()
        else:
            print("Energía insuficiente")