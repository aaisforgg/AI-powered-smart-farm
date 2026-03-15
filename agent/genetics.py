import random

class Genes:

    def __init__(self,
                 energy_max=None,
                 energy_consumption=None,
                 rest_efficiency=None,
                 exploration_rate=None):

        self.energy_max = energy_max if energy_max else random.uniform(80, 150)

        self.energy_consumption = (
            energy_consumption if energy_consumption
            else random.uniform(0.8, 1.5)
        )

        self.rest_efficiency = (
            rest_efficiency if rest_efficiency
            else random.uniform(2.0, 6.0)
        )

        self.exploration_rate = (
            exploration_rate if exploration_rate
            else random.uniform(0.1, 0.6)
        )

    def mutate(self, strength=0.1):
        """
        Muta todos los genes multiplicando por un factor aleatorio.
        strength controla qué tan grandes pueden ser los cambios (0.0 - 1.0).
        """
        self.energy_max = max(
            40.0,
            self.energy_max * random.uniform(1 - strength, 1 + strength)
        )

        self.energy_consumption = max(
            0.1,
            self.energy_consumption * random.uniform(1 - strength, 1 + strength)
        )

        self.rest_efficiency = max(
            0.5,
            self.rest_efficiency * random.uniform(1 - strength, 1 + strength)
        )

        self.exploration_rate = min(
            1.0,
            max(
                0.01,
                self.exploration_rate * random.uniform(1 - strength, 1 + strength)
            )
        )

    def crossover(self, other):

        child = Genes(
            energy_max=random.choice([self.energy_max, other.energy_max]),
            energy_consumption=random.choice(
                [self.energy_consumption, other.energy_consumption]
            ),
            rest_efficiency=random.choice(
                [self.rest_efficiency, other.rest_efficiency]
            ),
            exploration_rate=random.choice(
                [self.exploration_rate, other.exploration_rate]
            )
        )

        child.mutate()

        return child