import salabim as sim
import random

# Activar modo con yield
sim.yieldless(False)

class EstacionDeCarga:
    def __init__(self, capacidad):
        self.recurso = sim.Resource(capacity=capacidad)

class Auto(sim.Component):
    def __init__(self, estacion, nombre, prioridad, tiempo_max_espera):
        super().__init__(name=nombre, priority=prioridad)
        self.estacion = estacion
        self.tiempo_max_espera = tiempo_max_espera
        self.prioridad = prioridad

    def process(self):
        print(f"Se inicia el proceso de llegada del {self.name()} con prioridad {self.prioridad}")

        try:
            yield self.request((self.estacion.recurso,), fail_at=self.env.now() + self.tiempo_max_espera)
            print(f"{self.name()} con prioridad {self.prioridad} ha obtenido la estación de carga")
            print(f"Se inicia el proceso de carga del {self.name()} con prioridad {self.prioridad}")
            
            tiempo_carga = max(1, random.normalvariate(10, 2))
            yield self.hold(tiempo_carga)
            
            print(f"Carga completada del {self.name()} con prioridad {self.prioridad}")
        except sim.Fail:
            print(f"El {self.name()} con prioridad {self.prioridad} no pudo cargar por exceder el tiempo máximo de espera")

class Generador(sim.Component):
    def __init__(self, estacion):
        super().__init__()
        self.estacion = estacion

    def process(self):
        for i in range(10):
            prio = random.randint(0, 5)
            max_espera = random.uniform(20, 40)
            Auto(self.estacion, f"Auto-{i+1}", prio, max_espera).activate()
            yield self.hold(3)

env = sim.Environment()
estacion = EstacionDeCarga(capacidad=2)
Generador(estacion).activate()
env.run(till=100)