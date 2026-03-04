import random

class EventManager:
    def __init__(self):
        # Ya no recibimos 'simulation' ni 'grid' en el constructor
        self.active_event = None
        self.event_duration = 0

    def update(self, game_state, current_season):
        if self.event_duration > 0:
            self.event_duration -= 1
            if self.event_duration == 0:
                self._reset_effects(game_state)
            return

        # Probabilidad según estación
        prob = 0.05 * (1.5 if current_season == "Invierno" else 1.0)
        if random.random() < prob:
            self._trigger_event(game_state)

    def _trigger_event(self, game_state):
        eventos = ["gran_deslave", "nevada_paralizante", "plaga_de_insectos"]
        self.active_event = random.choice(eventos)
        self.event_duration = random.randint(5, 10)
        
        print(f"📢 EVENTO: {self.active_event.upper()} por {self.event_duration} turnos.")
        # Notificamos al estado global que hay un evento activo
        game_state.current_event = self.active_event

    def _reset_effects(self, game_state):
        print("🌤️ El evento ha terminado.")
        self.active_event = None
        game_state.current_event = None
        
        # Corregir el DOBLE LOOP para limpiar la grilla
        for row in game_state.world.farm_grid.grid:
            for node in row:
                node.walkable = True
                node.cost = 1

    def apply_world_changes(self, game_state):
      
        grid = game_state.world.farm_grid

        if self.active_event == "gran_deslave":
            # Modificamos nodos (Doble Loop si fuera necesario, aquí es área)
            x, y = random.randint(0, grid.width-3), random.randint(0, grid.height-3)
            for i in range(x, x+3):
                for j in range(y, y+3):
                    grid.get_node(i, j).walkable = False
        
        elif self.active_event == "nevada_paralizante":
          
            for row in grid.grid:
                for node in row:
                    if random.random() < 0.3:
                        node.cost = 10 # El agente verá esto y decidirá si pasar