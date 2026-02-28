# agent/decision.py

class DecisionMaker:
    def __init__(self, agent):
        self.agent = agent
        self.simulation = agent.simulation # Referencia al mundo/simulación

    def decide_action(self):
        # 1. ANALIZAR EL ENTORNO (Observación)
        current_event = self.simulation.event_manager.active_event
        current_season = self.simulation.season_manager.current_season
        
        # 2. TOMAR DECISIONES BASADAS EN REGLAS (Lógica)
        
        # --- SOLUCIÓN DE PROBLEMAS ---
        if current_event == "plaga_de_insectos":
            return self.action_combatir_plaga()
        
        elif current_event == "helada":
            return self.action_buscar_refugio()
            
        elif self.agent.energy < 20: # Energía crítica
            return self.action_buscar_comida()
            
        # --- COMPORTAMIENTO POR TEMPORADA ---
        if current_season == "Invierno":
            return self.action_estrategia_invierno()
        elif current_season == "Primavera":
            return self.action_estrategia_primavera()
            
        # --- COMPORTAMIENTO POR DEFECTO ---
        return self.action_explorar()

    # --- IMPLEMENTACIÓN DE ACCIONES ---

    def action_combatir_plaga(self):
        print(" Agente: Detecto plaga. Buscaré pesticida natural...")
        # Lógica para encontrar un recurso especial en el mapa
        return "buscar_recurso_especial"

    def action_buscar_refugio(self):
        print(" Agente: Hace demasiado frío. Buscando un árbol...")
        # Lógica para moverse a un nodo específico tipo "árbol"
        return "moverse_a_refugio"

    def action_estrategia_invierno(self):
        # En invierno, el agente debe priorizar ahorrar energía
        print(" Agente: Estrategia de invierno activa.")
        if self.agent.energy < 50:
            return "buscar_comida"
        return "quedarse_quieto" # Ahorrar energía