import salabim as sim

env = sim.Environment(trace=False)

# Definir colas
cola_pedido = sim.Queue("cola_pedido")
cola_pago = sim.Queue("cola_pago")

monitor_tiempo = sim.Monitor(name="tiempo_total_en_sistema")

class GeneradorAutos(sim.Component):
    def process(self):
        while True:
            Auto()
            self.hold(sim.Normal(3, 0.5))

class Auto(sim.Component):
    def process(self):
        self.enter(cola_pedido)
        self.enter_time = env.now()
        if servidor1.ispassive():
            servidor1.activate()
        elif servidor2.ispassive():
            servidor2.activate()
        self.passivate()

        self.enter(cola_pago)
        if cajero.ispassive():
            cajero.activate()
        self.passivate()

        total = env.now() - self.enter_time
        monitor_tiempo.tally(total)

class TomaPedidos(sim.Component):
    def process(self):
        while True:
            while len(cola_pedido) == 0:
                self.passivate()
            cliente = cola_pedido.pop()
            self.hold(sim.Triangular(low=1, mode=2, high=4).sample())  

            cliente.activate()

class Cajero(sim.Component):
    def process(self):
        while True:
            while len(cola_pago) == 0:
                self.passivate()
            cliente = cola_pago.pop()
            self.hold(sim.Exponential(1.5))
            cliente.activate()

# Crear componentes
GeneradorAutos()
servidor1 = TomaPedidos()
servidor2 = TomaPedidos()
cajero = Cajero()

# Ejecutar simulación
env.run(till=600)

# Mostrar estadísticas
print(f"Tiempo promedio total en el sistema: {monitor_tiempo.mean():.2f} minutos")
cola_pedido.print_statistics()
cola_pago.print_statistics()