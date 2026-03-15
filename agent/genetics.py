import random

class Genes:

    def __init__(self,
                 energy_max=None,
                 energy_consumption=None,
                 rest_efficiency=None,
                 exploration_rate=None,
                 vision_radius=None,
                 water_efficiency=None,
                 risk_tolerance=None):

        self.energy_max = energy_max if energy_max else random.uniform(150, 250)

        self.energy_consumption = (
            energy_consumption if energy_consumption
            else random.uniform(0.35, 0.55)
        )

        self.rest_efficiency = (
            rest_efficiency if rest_efficiency
            else random.uniform(2.0, 6.0)
        )

        self.exploration_rate = (
            exploration_rate if exploration_rate
            else random.uniform(0.1, 0.6)
        )

        self.vision_radius = (
            vision_radius if vision_radius
            else random.randint(6, 14)
        )

        self.water_efficiency = (
            water_efficiency if water_efficiency
            else random.uniform(30.0, 70.0)
        )

        self.risk_tolerance = (
            risk_tolerance if risk_tolerance
            else random.uniform(0.15, 0.40)
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

        self.vision_radius = max(
            4,
            min(20, int(self.vision_radius * random.uniform(1 - strength, 1 + strength)))
        )

        self.water_efficiency = max(
            15.0,
            min(100.0, self.water_efficiency * random.uniform(1 - strength, 1 + strength))
        )

        self.risk_tolerance = max(
            0.05,
            min(0.60, self.risk_tolerance * random.uniform(1 - strength, 1 + strength))
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
            ),
            vision_radius=random.choice([self.vision_radius, other.vision_radius]),
            water_efficiency=random.choice([self.water_efficiency, other.water_efficiency]),
            risk_tolerance=random.choice([self.risk_tolerance, other.risk_tolerance]),
        )

        child.mutate()

        return child