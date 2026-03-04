#movement.py
class Movement:

    def move_towards(self, agent, grid, goal):
        if not goal:
            return

        goal_x, goal_y = goal

        dx = goal_x - agent.x
        dy = goal_y - agent.y

        move_x = 0
        move_y = 0

        # Movimiento en X primero
        if dx != 0:
            move_x = int(dx / abs(dx))
        elif dy != 0:
            move_y = int(dy / abs(dy))

        new_x = agent.x + move_x
        new_y = agent.y + move_y

        # 🔥 VALIDACIÓN DE LÍMITES 80x72
        if 0 <= new_x < 80 and 0 <= new_y < 72:

            # Evitar obstáculos (1 = obstáculo)
            if grid[new_y][new_x] != 1:
                agent.x = new_x
                agent.y = new_y