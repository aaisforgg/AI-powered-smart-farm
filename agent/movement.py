import random
from core.logic import calcular_costo_movimiento_total


class Movement:

    BLOCKED_TILES = [1, 2, 3]  # agua, acantilado, edificio

    def move_towards(self, agent, state, goal):
        if not goal:
            return False

        goal_x, goal_y = goal

        dx = goal_x - agent.x
        dy = goal_y - agent.y

        move_x = 0
        move_y = 0

        if dx != 0:
            move_x = int(dx / abs(dx))
        elif dy != 0:
            move_y = int(dy / abs(dy))

        new_x = agent.x + move_x
        new_y = agent.y + move_y

        if not self._is_valid_position(new_x, new_y, state):
            return False

        return self._apply_movement(agent, state, new_x, new_y)

    def random_move(self, agent, state):
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        random.shuffle(directions)

        for dx, dy in directions:
            new_x = agent.x + dx
            new_y = agent.y + dy

            if self._is_valid_position(new_x, new_y, state):
                if self._apply_movement(agent, state, new_x, new_y):
                    return True

        return False

    # =========================
    # MÉTODOS INTERNOS
    # =========================

    def _is_valid_position(self, x, y, state):

        # Validar límites
        if not (0 <= x < len(state.grid[0]) and 0 <= y < len(state.grid)):
            return False

        tile = state.grid[y][x]

        # Caso 1: Grid numérico
        if isinstance(tile, int):
            return tile not in self.BLOCKED_TILES

        # Caso 2: Grid con Node objects
        if hasattr(tile, "walkable"):
            return tile.walkable

        return True

    def _apply_movement(self, agent, state, new_x, new_y):

        tile = state.grid[new_y][new_x]

        # ---------------------------
        # CASO 1: Grid numérico
        # ---------------------------
        if isinstance(tile, int):

            if tile in self.BLOCKED_TILES:
                return False

            # Costos simples por tipo
            costo = 1.0

            if tile == 4:      # cultivo
                costo = 1.5
            elif tile == 5:    # puente
                costo = 0.8
            elif tile == 6:    # puerta
                costo = 1.0

        # ---------------------------
        # CASO 2: Grid con Node
        # ---------------------------
        else:
            costo = calcular_costo_movimiento_total(state, new_x, new_y)

        # ---------------------------
        # Validar energía
        # ---------------------------
        if agent.energy < costo:
            print("Energía insuficiente.")
            return False

        # Aplicar movimiento
        agent.energy -= costo
        agent.x = new_x
        agent.y = new_y

        return True