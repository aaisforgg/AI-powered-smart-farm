import random

class EventManager:
    def __init__(self, simulation):
        self.sim = simulation
        self.grid = simulation.world.farm_grid  # Acceso a tu grilla de nodos
        self.active_event = None
        self.event_duration = 0

    def update(self, current_season):
        """Se llama en cada turno de la simulación."""
        if self.event_duration > 0:
            self.event_duration -= 1
            if self.event_duration == 0:
                self.reset_world_effects()
            return

        # Probabilidad de que ocurra un evento (ajustada por estación)
        prob = 0.05 * (1.5 if current_season == "Invierno" else 1.0)
        if random.random() < prob:
            self.trigger_combined_event(current_season)

    def trigger_combined_event(self, season):
        # Lista de eventos complejos (Mezcla de Energía + Mapa + Obstáculos)
        eventos = [
            "gran_deslave", "nevada_paralizante", "tormenta_electrica", 
            "sequia_extrema", "inundacion_repentina", "niebla_toxica",
            "viento_huracanado", "plaga_y_hambre", "oasis_temporal"
        ]
        
        self.active_event = random.choice(eventos)
        self.event_duration = random.randint(5, 15) # Turnos que dura el efecto
        self.apply_combined_effects(self.active_event)

    def apply_combined_effects(self, event):
        print(f" EVENTO GLOBAL: {event.upper()} activado por {self.event_duration} turnos.")
        
        # --- REFERENCIAS ---
        agente = self.sim.agent
        grid = self.grid

        if event == "gran_deslave":
            # COMBINA: Obstáculos físicos + Gasto de energía por susto/esfuerzo
            x, y = random.randint(0, grid.width-3), random.randint(0, grid.height-3)
            for i in range(x, x+3):
                for j in range(y, y+3):
                    grid.get_node(i, j).walkable = False
            agente.energy -= 20
            agente.recalculate_path() # Obliga a A* a buscar nueva ruta

        elif event == "nevada_paralizante":
            # COMBINA: Costo de movimiento x5 + Pérdida de energía por frío
            for node in grid.nodes:
                if random.random() < 0.4: node.cost = 5
            agente.energy_loss_per_turn += 2 

        elif event == "tormenta_electrica":
            # COMBINA: Rayos que quitan energía + Posibles incendios (bloqueos)
            if random.random() < 0.5:
                agente.energy -= 40
                print(" ¡Un rayo alcanzó al agente!")
            # Bloquea celdas aleatorias como "fuego"
            for _ in range(5):
                grid.get_node(random.randint(0, grid.width-1), random.randint(0, grid.height-1)).walkable = False

        elif event == "viento_huracanado":
            # COMBINA: Empuja al agente (cambia posición) + Gasta energía
            dir_x, dir_y = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            agente.force_move(dir_x * 2, dir_y * 2) # Lo empuja 2 celdas
            agente.energy -= 15

        elif event == "inundacion_repentina":
            # COMBINA: Destruye cultivos (menos comida) + Terreno difícil (costo)
            self.sim.world.destroy_random_crops(count=10)
            for node in grid.nodes:
                node.cost = 3

        elif event == "niebla_toxica":
            # COMBINA: Reduce visión (estrategia) + Quita energía cada turno
            agente.vision_range = 1
            agente.poisoned = True # Debes manejar esto en agent.py

    def reset_world_effects(self):
        """Limpia el mapa cuando el evento termina."""
        print(" El clima ha vuelto a la normalidad.")
        for node in self.grid.nodes:
            node.walkable = True
            node.cost = 1
        self.sim.agent.vision_range = 5 # O tu valor por defecto
        self.sim.agent.energy_loss_per_turn = 1