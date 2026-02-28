# agent/agent.py

class Agent:
    def __init__(self):
        self.energy = 100
        # ... otras variables ...
        self.knowledge_base = {
            "plagas": "buscar_recurso_rojo",
            "helada": "quedarse_quieto",
            "sequia": "moverse_a_agua"
        }

    def learn(self, problem, solution):
        """Si una solución funcionó, el agente la guarda."""
        self.knowledge_base[problem] = solution
        print(f" Aprendizaje: Ahora sé cómo manejar {problem}")