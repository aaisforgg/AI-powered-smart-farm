class Pipeline:
    def __init__(self, *steps):
        self.steps = steps

    def run(self, state):
        """Ejecuta cada paso de forma independiente[cite: 41]."""
        for step in self.steps:
            state = step(state)
        return state