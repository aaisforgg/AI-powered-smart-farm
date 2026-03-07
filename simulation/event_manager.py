import random

class EventManager:
    def __init__(self):
        # Esta es la variable que el main.py está buscando
        self.current_event = None
        self.event_timer = 0
        self.event_duration = 60 

    def update(self, state, season):
        if self.current_event:
            self.event_timer -= 1
            if self.event_timer <= 0:
                print(f"✅ El evento {self.current_event} ha terminado.")
                self.current_event = None
        else:
            # 1% de probabilidad de evento por cada tick de reloj
            if random.random() < 0.01:
                if season == "Verano":
                    self.current_event = "Sequía"
                elif season == "Invierno":
                    self.current_event = "Tormenta"
                else:
                    self.current_event = "Plaga"
                
                self.event_timer = self.event_duration
                print(f"⚠️ ¡ALERTA!: Ha comenzado: {self.current_event}")