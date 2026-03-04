print("Proyecto IA Granja iniciado")
from core.state import State
from core.pipeline import Pipeline
from entities.crop import Crop

def iniciar():
    estado = State()
    # Ejemplo: Poner agua en (1,1)
    estado.mapa[(1, 1)] = "AGUA"
    estado.cultivos.append(Crop("Trigo", 2, 2))
    
    motor = Pipeline(estado)
    print("Granja iniciada. Energía:", estado.granjero_energia)
    
    # El granjero intenta moverse al agua
    motor.ejecutar_paso((1, 1))
    print("Energía tras mover al agua:", estado.granjero_energia)

if __name__ == "__main__":
    iniciar()