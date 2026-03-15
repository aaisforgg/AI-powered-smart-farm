import random
import copy


class FitnessEvaluator:
    """
    Calcula el puntaje de aptitud de un agente al final de su vida.

    La fórmula premia cosechar mucho, moverse eficientemente,
    diversificar acciones y sobrevivir sin quedarse sin energía.
    """

    @staticmethod
    def evaluate(agent) -> float:
        stats = agent.life_stats
        score = 0.0

        harvests = stats["harvests"]
        steps = stats["steps"]
        energy_on_rest = stats["energy_on_rest"] or 0.0

        # 1. Cosechas (peso principal)
        score += harvests * 50.0

        # 2. Eficiencia de ruta: ratio cosechas/pasos
        #    Más cosechas con menos pasos = mejor
        if steps > 0:
            efficiency = harvests / steps
            score += efficiency * 200.0

        # 3. Energía al llegar a casa (no llegar al límite)
        score += energy_on_rest * 0.3

        # 4. Penalización por morir de hambre
        if stats["starved"]:
            score -= 40.0

        # 5. Diversidad de acciones (premiar hacer de todo, no solo harvest)
        actions = [a[0] for a in agent.memory.get("last_actions", [])]
        unique_actions = len(set(actions))
        score += unique_actions * 10.0

        # 6. Bonus por supervivencia (completar la vida sin starve)
        if not stats["starved"] and energy_on_rest and energy_on_rest > 0:
            score += 20.0

        return max(score, 0.0)


class EvolutionEngine:
    """
    Gestiona el ciclo evolutivo de un agente de vida en vida.

    Al final de cada vida:
      1. Evalúa el fitness de la vida que acaba de terminar.
      2. Decide si conservar los genes actuales o mutar/cruzar con elites.
      3. Reinicia las estadísticas para la siguiente vida.
    """

    def __init__(self):
        self.generation       = 0
        self.best_fitness     = 0.0
        self.fitness_history  = []   # fitness de cada generación
        self.evaluator        = FitnessEvaluator()
        self.elite_genes      = []   # Top 3 mejores genes de la historia
        self.MAX_ELITE        = 3

    def end_life(self, agent):
        """
        Llamar cuando el agente termina de descansar (energy >= max_energy).
        Evalúa, evoluciona los genes y prepara la siguiente vida.
        """
        fitness = self.evaluator.evaluate(agent)
        self.fitness_history.append(fitness)

        # Guardar genes si están entre los mejores
        gene_snapshot = copy.deepcopy(agent.genes)
        self.elite_genes.append((fitness, gene_snapshot))
        self.elite_genes.sort(key=lambda x: x[0], reverse=True)
        self.elite_genes = self.elite_genes[:self.MAX_ELITE]

        print(f"\n{'='*40}")
        print(f"[Evolución] Generación {self.generation} terminó")
        print(f"  Fitness:   {fitness:.2f}")
        print(f"  Cosechas:  {agent.life_stats['harvests']}")
        print(f"  Pasos:     {agent.life_stats['steps']}")
        print(f"  Mejor histórico: {self.best_fitness:.2f}")
        print(f"  Elites guardados: {len(self.elite_genes)}")
        print(f"{'='*40}\n")

        # Guardar mejor fitness
        if fitness >= self.best_fitness:
            self.best_fitness = fitness
            print("[Evolución] ¡Nuevos mejores genes guardados!")

        # Evolucionar con selección dirigida
        self._evolve(agent, fitness)

        # Avanzar generación y resetear estadísticas
        self.generation += 1
        agent.reset_life_stats()

    def _evolve(self, agent, current_fitness):
        """
        Estrategia evolutiva con selección real:
        - Si mejoró: mutación suave sobre genes actuales
        - Si empeoró: crossover con el mejor elite + mutación agresiva
        - Siempre aplica los nuevos genes al agente
        """
        if len(self.fitness_history) >= 3:
            recent_avg = sum(self.fitness_history[-3:]) / 3

            if current_fitness >= recent_avg:
                # Va bien: mutación conservadora
                agent.genes.mutate(strength=0.05)
            else:
                # Va mal: cruzar con el mejor elite si existe
                if self.elite_genes:
                    best_genes = self.elite_genes[0][1]
                    agent.genes = agent.genes.crossover(best_genes)
                    agent.genes.mutate(strength=0.10)
                else:
                    agent.genes.mutate(strength=0.20)
        else:
            agent.genes.mutate(strength=0.10)

        # Aplicar genes al agente
        agent.max_energy       = agent.genes.energy_max
        agent.energy           = agent.genes.energy_max
        agent.energy_threshold = agent.genes.energy_max * agent.genes.risk_tolerance
