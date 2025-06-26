import salabim as sim 
sim.yieldless(False)

class Camion(sim.Component):
    def setup(self, peso):
        self.peso = peso
    def process(self):
        print(f"Se inicia la carga del camion que pesa {self.peso} libras")
        yield self.hold(50)
        print(f"Camión de peso {self.peso} libras cargado completamente")

class Grua(sim.Component):
    def process(self):
        print("Se inicia el proceso de descarga")
        yield self.hold(100)
        print("Descarga completada")

env = sim.Environment(trace=False)

camion1 = Camion(peso=6000)
camion2 = Camion(peso=5000)
grua1 = Grua()

camion1.activate()
camion2.activate(delay=50)
grua1.activate(at=100)

env.run()