def update(self):
    # 1. Actualizar lógica de movimiento/decisión
    # 2. Manejar clima/estaciones
    self.season_manager.update()
    
    # 3. Lanzar eventos aleatorios
    self.event_manager.check_for_random_events(self.season_manager.current_season)
    
    # 4. Renderizar
    self.renderer.render(self.state)