class Pipeline:
    """
    Ejecuta una secuencia de pasos sobre GameState.
    Cada paso es una función que recibe state y lo muta in-place.
    """

    def __init__(self, *steps):
        self.steps = list(steps)

    def run(self, state):
        for step in self.steps:
            step(state)