import salabim as sim

env = sim.Environment(trace=False)

# Monitores y contadores
productos_enviados = 0
productos_retrabajados = 0

# Colas
cola_ensamblaje = sim.Queue("cola_ensamblaje")
cola_calidad = sim.Queue("cola_calidad")
cola_retrabajo = sim.Queue("cola_retrabajo") 

# Generador de materiales
class GeneradorMateriales(sim.Component):
    def process(self):
        while True:
            Producto()
            self.hold(sim.Uniform(2, 4))

# Producto que atraviesa todo el proceso
class Producto(sim.Component):
    def process(self):
        # Ensamblaje
        self.enter(cola_ensamblaje)
        ensamblador.activate()
        self.passivate()

        # Control de calidad
        self.enter(cola_calidad)
        controlador_calidad.activate()
        self.passivate()

        # Evaluación del resultado del control
        if self.necesita_retrabajo:
            global productos_retrabajados
            productos_retrabajados += 1

            # Retrabajo
            self.enter(cola_retrabajo)
            ensamblador.activate()
            self.passivate()

            # Volver a control de calidad
            self.enter(cola_calidad)
            controlador_calidad.activate()
            self.passivate()

        global productos_enviados
        productos_enviados += 1

# Estación de ensamblaje
class Ensamblador(sim.Component):
    def process(self):
        while True:
            while len(cola_ensamblaje) == 0 and len(cola_retrabajo) == 0:
                self.passivate()
            if len(cola_retrabajo) > 0:
                producto = cola_retrabajo.pop()
                self.hold(sim.Uniform(2, 3))  # Tiempo de retrabajo
            else:
                producto = cola_ensamblaje.pop()
                self.hold(sim.Uniform(3, 7))  # Tiempo de ensamblaje
            producto.activate()

# Estación de control de calidad
class ControladorCalidad(sim.Component):
    def process(self):
        while True:
            while len(cola_calidad) == 0:
                self.passivate()
            producto = cola_calidad.pop()
            self.hold(0.5)  # Tiempo de revisión corto (opcional)
            producto.necesita_retrabajo = sim.Uniform(0, 1).sample() < 0.1
            producto.activate()

# Instanciar componentes
GeneradorMateriales()
ensamblador = Ensamblador()
controlador_calidad = ControladorCalidad()

# Ejecutar simulación por 1000 minutos
env.run(till=1000)

# Mostrar estadísticas
cola_ensamblaje.print_statistics()
cola_calidad.print_statistics()
cola_retrabajo.print_statistics()

# Mostrar resultados finales
print(f"\nProductos enviados: {productos_enviados}")
print(f"Productos retrabajados: {productos_retrabajados}")
print(f"Rendimiento: {productos_enviados / (1000 / 60):.2f} productos por hora")
