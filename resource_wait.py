import salabim as sim
import random

class EstacionDeCarga:
    def __init__(self, env, capacidad):
        self.env = env
        self.recurso = sim.Resource(capacity=capacidad)

class Auto(sim.Component):
    def __init__(self, estacion, nombre, prioridad, tiempo_max_espera):
        super().__init__(name=nombre, priority=prioridad)
        self.estacion = estacion
        self.tiempo_max_espera = tiempo_max_espera
        self.prioridad = prioridad

    def process(self):
        llegada = self.env.now()
        print(f"{llegada:.1f} - {self.name()} (prio {self.prioridad}) llega")

        try:
            yield self.request((self.estacion.recurso,), fail_at=llegada + self.tiempo_max_espera)
            print(f"{self.env.now():.1f} - {self.name()} obtiene estación")
            tiempo_carga = max(1, random.normalvariate(10, 2))
            yield self.hold(tiempo_carga)
            print(f"{self.env.now():.1f} - {self.name()} termina carga")
        except sim.Fail:
            print(f"{self.env.now():.1f} - {self.name()} falló (timeout)")

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
estacion = EstacionDeCarga(env, capacidad=2)
Generador(estacion).activate()
env.run(till=100)
