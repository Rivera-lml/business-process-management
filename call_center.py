import salabim as sim

# Crear entorno
env = sim.Environment(trace=False)

cola_clientes = sim.Queue("Cola Clientes")

# Monitores de tiempo de espera
espera_regular = sim.Monitor("Espera Regular")
espera_vip = sim.Monitor("Espera VIP")

# Contadores
atendidos_regular = 0
atendidos_vip = 0
abandonados_regular = 0
abandonados_vip = 0

representantes = []

class ClienteVIP(sim.Component):
    def process(self):
        global abandonados_vip, atendidos_vip
        llegada = env.now()
        self.enter(cola_clientes, priority=0)
        for r in representantes:
            if r.status() == sim.passive:
                r.activate()
                break
        self.activate(delay=10, method=self.abandonar)
        self.passivate()
        if self in cola_clientes:
            self.leave(cola_clientes)
            abandonados_vip += 1
        else:
            espera_vip.tally(env.now() - llegada)
            atendidos_vip += 1

    def abandonar(self):
        if self in cola_clientes:
            self.cancel()

class ClienteRegular(sim.Component):
    def process(self):
        global abandonados_regular, atendidos_regular
        llegada = env.now()
        self.enter(cola_clientes, priority=1)
        for r in representantes:
            if r.status() == sim.passive:
                r.activate()
                break
        self.activate(delay=10, method=self.abandonar)
        self.passivate()
        if self in cola_clientes:
            self.leave(cola_clientes)
            abandonados_regular += 1
        else:
            espera_regular.tally(env.now() - llegada)
            atendidos_regular += 1

    def abandonar(self):
        if self in cola_clientes:
            self.cancel()

class GeneradorVIP(sim.Component):
    def process(self):
        while True:
            ClienteVIP()
            self.hold(sim.Exponential(12))

class GeneradorRegular(sim.Component):
    def process(self):
        while True:
            ClienteRegular()
            self.hold(sim.Exponential(2))  # Más frecuencia para probar abandonos

class Representante(sim.Component):
    def process(self):
        while True:
            if len(cola_clientes) == 0:
                self.passivate()
            cliente = cola_clientes.pop()
            if isinstance(cliente, ClienteVIP):
                self.hold(sim.Exponential(8))
            else:
                self.hold(sim.Exponential(6))
            cliente.activate()

# Instanciar componentes
GeneradorVIP()
GeneradorRegular()
for _ in range(3):
    r = Representante()
    representantes.append(r)

# Ejecutar simulación
env.run(till=720)

# Mostrar estadísticas
print(f"Tiempo de espera promedio Regular: {espera_regular.mean():.2f} minutos")
print(f"Tiempo de espera promedio VIP: {espera_vip.mean():.2f} minutos")
print(f"Clientes REGULARES: Atendidos = {atendidos_regular}, Abandonados = {abandonados_regular}")
print(f"Clientes VIP:       Atendidos = {atendidos_vip}, Abandonados = {abandonados_vip}")
