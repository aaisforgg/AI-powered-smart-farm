from .decision import DecisionSystem
from .movement import Movement


class Agent:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.energy = 100.0  # Energía inicial

        self.goal = None
        self.strategy = None

        self.decision_system = DecisionSystem()
        self.movement = Movement()

    def update(self, state):

        # -------------------------
        # 1️⃣ Si está descansando
        # -------------------------
        if self.strategy == "REST":
            self.energy += 2
            self.energy = min(self.energy, 100)
            print(f"Descansando... Energía: {self.energy}")

            # Cuando ya tenga suficiente energía, volverá a decidir
            if self.energy >= 40:
                self.goal = None
                self.strategy = None

            return

        # -------------------------
        # 2️⃣ Si está agotado
        # -------------------------
        if self.energy <= 0:
            print("Agente sin energía.")
            self.strategy = "EXHAUSTED"
            return

        # -------------------------
        # 3️⃣ Tomar decisión si no tiene meta
        # -------------------------
        if not self.goal:
            self.goal, self.strategy = self.decision_system.decide(state.grid, self)

        # -------------------------
        # 4️⃣ Ejecutar comportamiento
        # -------------------------
        if self.goal:

            if (self.x, self.y) == self.goal:
                print("Llegó al objetivo.")
                self.goal = None
                self.strategy = None

            else:
                moved = self.movement.move_towards(self, state, self.goal)

                if not moved:
                    self.movement.random_move(self, state)

        else:
            # Si no tiene meta y no está descansando
            self.movement.random_move(self, state)