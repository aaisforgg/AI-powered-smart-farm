# main.py
print("Proyecto IA Granja iniciado")

from core.state import State
from core.pipeline import Pipeline
from entities.crop import Crop
# Se elimina el import de SmartAgent por limpieza

def iniciar():
    # Pedro: "construir_state_desde_grid"
    # Definimos un grid inicial (ejemplo 5x5) para inicializar el estado
    grid_ejemplo = [
        ["PASTO", "PASTO", "PASTO", "PASTO", "PASTO"],
        ["PASTO", "AGUA",  "PASTO", "PASTO", "PASTO"],
        ["PASTO", "PASTO", "TIERRA", "PASTO", "PASTO"],
        ["PASTO", "PASTO", "PASTO", "PASTO", "PASTO"],
        ["PASTO", "PASTO", "PASTO", "PASTO", "PASTO"]
    ]
    
    # Inicializamos usando el grid definido
    estado = State(grid=grid_ejemplo)
    
    # El mapa se actualiza según el grid, pero podemos añadir elementos extra
    estado.cultivos.append(Crop("Trigo", 2, 2))
    
    motor = Pipeline(estado)
    print(f"Granja iniciada. Energía inicial: {estado.granjero_energia}")
    
    # El granjero intenta moverse a la posición del agua (1, 1)
    motor.ejecutar_paso((1, 1))
    print(f"Energía tras mover al agua: {estado.granjero_energia}")

if __name__ == "__main__":
    iniciar()