import salabim as sim

env = sim.Environment(trace=False)

cola_vacunacion = sim.Queue("cola_vacunacion")

abandono_adultos = sim.Monitor("Abandono adultos")
espera_adultos = sim.Monitor("Espera adultos")

abandono_ninos = sim.Monitor("Abandono niños")
espera_ninos = sim.Monitor("Espera niños")

enfermeras = []

# Contadores para estadísticas
atendidos_adultos = 0
atendidos_ninos_por_enfermera = 0
atendidos_ninos_por_pediatra = 0

class GeneradorAdultos(sim.Component):
    def process(self):
        while True:
            Adulto()
            self.hold(sim.Exponential(5).sample())

class GeneradorNinos(sim.Component):
    def process(self):
        while True:
            Nino()
            self.hold(sim.Uniform(3, 7).sample())

class Adulto(sim.Component):
    def process(self):
        global atendidos_adultos
        llegada = env.now()
        self.enter(cola_vacunacion, priority=1)
        for i in enfermeras:
            if i.status() == sim.passive:
                i.activate()
                break
        self.activate(delay=15, method=self.abandonar)
        self.passivate()
        if self in cola_vacunacion:
            self.leave(cola_vacunacion)
            abandono_adultos.tally(1)
        else:
            espera_adultos.tally(env.now() - llegada)
            atendidos_adultos += 1

    def abandonar(self):
        if self in cola_vacunacion:
            self.cancel()

class Nino(sim.Component):
    def process(self):
        global atendidos_ninos_por_enfermera, atendidos_ninos_por_pediatra
        self.tiempo_llegada = env.now()
        self.atendido_por_enfermera = False
        self.enter(cola_vacunacion, priority=0)
        if pediatra.status() == sim.passive:
            pediatra.activate()
        for i in enfermeras:
            if i.status() == sim.passive:
                i.activate()
                break
        self.activate(delay=15, method=self.abandonar)
        self.passivate()
        if self in cola_vacunacion:
            self.leave(cola_vacunacion)
            abandono_ninos.tally(1)       # a los Monitor se les agrega información con Tally
        else:
            espera_ninos.tally(env.now() - self.tiempo_llegada)    # a los Monitor se les agrega información con Tally
            if self.atendido_por_enfermera:
                atendidos_ninos_por_enfermera += 1
            else:
                atendidos_ninos_por_pediatra += 1

    def abandonar(self):
        if self in cola_vacunacion:
            self.cancel()

class Enfermera(sim.Component):
    def process(self):
        while True:
            while len(cola_vacunacion) == 0:
                self.passivate()

            paciente_atendido = False

            # Buscar niños que han esperado ≥6 min y que no puedan ser atendidos por el pediatra
            for paciente in cola_vacunacion:
                if isinstance(paciente, Nino):
                    espera = env.now() - paciente.tiempo_llegada
                    if espera >= 6 and pediatra.status() != sim.passive:   
                        continue  # Esperar al pediatra si está disponible
                    elif espera >= 6:
                        cola_vacunacion.remove(paciente)
                        paciente.atendido_por_enfermera = True
                        self.hold(sim.Exponential(5).sample())
                        paciente.activate()
                        paciente_atendido = True
                        break

            # Si no encontró niño atendible, buscar adulto
            if not paciente_atendido:
                for paciente in cola_vacunacion:
                    if isinstance(paciente, Adulto):
                        cola_vacunacion.remove(paciente)
                        self.hold(sim.Triangular(3, 6, 4).sample())
                        paciente.activate()
                        paciente_atendido = True
                        break

            if not paciente_atendido:
                self.passivate()

class Pediatra(sim.Component):
    def process(self):
        while True:
            while len(cola_vacunacion) == 0:
                self.passivate()
            for paciente in cola_vacunacion:
                if isinstance(paciente, Nino):
                    cola_vacunacion.remove(paciente)
                    self.hold(sim.Exponential(5).sample())
                    paciente.activate()
                    break
            else:
                self.passivate()

# Instanciar generadores
GeneradorAdultos()
GeneradorNinos()

# Instanciar enfermeras
for _ in range(2):
    e = Enfermera()
    enfermeras.append(e)

# Instanciar pediatra
pediatra = Pediatra()

# Ejecutar simulación por 600 minutos (10 horas)
env.run(till=600)

# Resultados finales
print("\n--- Resultados finales ---")
print(f"Adultos atendidos: {atendidos_adultos}")
print(f"Niños atendidos por pediatra: {atendidos_ninos_por_pediatra}")
print(f"Niños atendidos por enfermera: {atendidos_ninos_por_enfermera}")
print(f"Total abandonos adultos: {abandono_adultos.number_of_entries()}")
print(f"Total abandonos niños: {abandono_ninos.number_of_entries()}")
print(f"Tiempo promedio espera adultos: {espera_adultos.mean():.2f} min")
print(f"Tiempo promedio espera niños: {espera_ninos.mean():.2f} min")
cola_vacunacion.print_statistics()

