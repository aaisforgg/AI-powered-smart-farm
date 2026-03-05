class Pipeline:
    def __init__(self, *steps):
        self.steps = steps

    def run(self, state):
        for step in self.steps:
            state = step(state)
        return state