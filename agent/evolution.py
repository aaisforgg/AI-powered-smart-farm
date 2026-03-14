import random


class FitnessEvaluator:
    """
    Calcula el puntaje de aptitud de un agente al final de su vida.

    La fórmula premia cosechar mucho y moverse eficientemente,
    y penaliza desperdiciar energía o quedarse sin ella.
    """

    HARVEST_REWARD   = 50.0   # puntos por cultivo cosechado
    STEP_PENALTY     = 0.05   # costo por cada paso dado (eficiencia de ruta)
    ENERGY_BONUS     = 0.2    # premio por energía sobrante al llegar a casa
    STARVE_PENALTY   = 30.0   # penalización si el agente se quedó sin energía

    @staticmethod
    def evaluate(agent) -> float:
        stats = agent.life_stats

        score = 0.0

        # Cosechas realizadas (lo más importante)
        score += stats["harvests"] * FitnessEvaluator.HARVEST_REWARD

        # Eficiencia de movimiento
        score -= stats["steps"] * FitnessEvaluator.STEP_PENALTY

        # Bonus por energía restante al descansar (no llegar agotado)
        energy_on_rest = stats["energy_on_rest"] or 0.0
        score += energy_on_rest * FitnessEvaluator.ENERGY_BONUS

        # Penalización si se quedó sin energía en campo
        if stats["starved"]:
            score -= FitnessEvaluator.STARVE_PENALTY

        return max(score, 0.0)  # el fitness nunca es negativo


class EvolutionEngine:
    """
    Gestiona el ciclo evolutivo de un agente de vida en vida.

    Al final de cada vida:
      1. Evalúa el fitness de la vida que acaba de terminar.
      2. Decide si conservar los genes actuales o mutar.
      3. Reinicia las estadísticas para la siguiente vida.
    """

    def __init__(self):
        self.generation       = 0
        self.best_fitness     = 0.0
        self.fitness_history  = []   # fitness de cada generación
        self.evaluator        = FitnessEvaluator()

    def end_life(self, agent):
        """
        Llamar cuando el agente termina de descansar (energy >= max_energy).
        Evalúa, evoluciona los genes y prepara la siguiente vida.
        """
        fitness = self.evaluator.evaluate(agent)
        self.fitness_history.append(fitness)

        print(f"\n{'='*40}")
        print(f"[Evolución] Generación {self.generation} terminó")
        print(f"  Fitness:   {fitness:.2f}")
        print(f"  Cosechas:  {agent.life_stats['harvests']}")
        print(f"  Pasos:     {agent.life_stats['steps']}")
        print(f"  Mejor histórico: {self.best_fitness:.2f}")
        print(f"{'='*40}\n")

        # Guardar mejor fitness y genes si mejoraron
        if fitness >= self.best_fitness:
            self.best_fitness = fitness
            print("[Evolución] ¡Nuevos mejores genes guardados!")

        # Evolucionar: mutar siempre, cruzar si hay historial suficiente
        self._evolve(agent, fitness)

        # Avanzar generación y resetear estadísticas
        self.generation += 1
        agent.reset_life_stats()

    def _evolve(self, agent, current_fitness):
        """
        Estrategia adaptativa:
        - Si el fitness mejoró respecto al promedio reciente → mutación suave
        - Si el fitness empeoró → mutación más agresiva para explorar
        """
        if len(self.fitness_history) >= 3:
            recent_avg = sum(self.fitness_history[-3:]) / 3
            if current_fitness >= recent_avg:
                # Va bien: mutación conservadora
                agent.genes.mutate(strength=0.05)
            else:
                # Va mal: sacudir más los genes
                agent.genes.mutate(strength=0.20)
        else:
            agent.genes.mutate(strength=0.10)

        # Aplicar los nuevos genes al agente
        agent.max_energy = agent.genes.energy_max
        agent.energy     = agent.genes.energy_max