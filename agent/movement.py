import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agent import Agent

class Movement:

    def follow_path(self, agent: "Agent"):
        """
        Hace que el agente avance un paso en su ruta actual (current_path).

        current_path es un deque con posiciones (x,y) que el agente debe seguir.
        Cada tick se consume el siguiente nodo del path.
        """

        # Si no hay ruta, no hay nada que hacer
        if not agent.current_path:
            return

        # Miramos el siguiente nodo de la ruta
        # [0] solo lo observa, no lo elimina todavía
        nx, ny = agent.current_path[0]

        # Calculamos la dirección del movimiento
        # Esto se usa para saber hacia dónde se mueve el agente
        dx = nx - agent.x
        dy = ny - agent.y

        # Movemos al agente a la nueva posición
        agent.x = nx
        agent.y = ny

        # Guardamos la dirección para otros sistemas
        # (animación, exploración, decisiones, etc.)
        agent.dir = (dx, dy)

        # Ahora sí eliminamos el nodo del path
        # porque ya lo hemos alcanzado
        agent.current_path.popleft()

        # ---------------------------------------------------------
        # PATH SMOOTHING (suavizado del path)
        # ---------------------------------------------------------
        # Esta parte elimina pasos innecesarios si el agente
        # sigue moviéndose en la misma dirección.
        #
        # Ejemplo de path original:
        #
        # (5,5) -> (6,5) -> (7,5) -> (8,5)
        #
        # En lugar de caminar paso por paso,
        # eliminamos los nodos redundantes.
        # ---------------------------------------------------------

        while agent.current_path:

            # Miramos el siguiente nodo
            nnx, nny = agent.current_path[0]

            # Dirección hacia ese nodo
            ndx = nnx - agent.x
            ndy = nny - agent.y

            # Si la dirección es la misma que la anterior
            # significa que seguimos en línea recta
            if (ndx, ndy) == (dx, dy):

                # Eliminamos ese nodo porque es redundante
                agent.current_path.popleft()

            else:
                # Si cambia la dirección, paramos
                # porque aquí empieza un giro del path
                break

    def explore(self, agent, grid):

        rows = len(grid)
        cols = len(grid[0])

        directions = [
            agent.dir,        # seguir igual
            (1,0),(-1,0),(0,1),(0,-1)
        ]

        # quitar duplicados
        directions = list(dict.fromkeys(directions))

        # aleatoriedad controlada por el gen exploration_rate
        exploration_rate = getattr(agent.genes, 'exploration_rate', 0.3)
        if random.random() < exploration_rate:
            random.shuffle(directions)

# ---------- Buscar tiles no visitados ----------
        for dx, dy in directions:

            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < cols and 0 <= ny < rows:

                if not grid[ny][nx].walkable:
                    continue

                if (nx, ny) in agent.memory["visited_tiles"]:
                    continue

                agent.x = nx
                agent.y = ny

                agent.dir = (dx, dy)

                return
            
    # ---------- Si todo fue visitado ----------
        for dx, dy in directions:

            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < cols and 0 <= ny < rows:

                if not grid[ny][nx].walkable:
                    continue

                agent.x = nx
                agent.y = ny
                agent.dir = (dx, dy)

                return