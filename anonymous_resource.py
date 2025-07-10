import salabim as sim
import random

class Vehiculo(sim.Component):
    def process(self):
        print(f"{self.name()} necesita combustible en t={env.now():.1f}")
        
        # Solicitar 20 litros de combustible
        cantidad_necesaria = 20
        self.request((combustible, cantidad_necesaria))
        
        print(f"{self.name()} obtuvo {cantidad_necesaria}L combustible en t={env.now():.1f}")
        
        # Simular uso del combustible (viaje)
        tiempo_viaje = random.uniform(3, 8)
        self.hold(tiempo_viaje)
        
        # No es necesario liberar combustible en este caso
        # (se consume durante el viaje)
        print(f"{self.name()} completó viaje en t={env.now():.1f}")

class ReabastecedorCombustible(sim.Component):
    def process(self):
        while True:
            # Esperar un tiempo y reabastecer
            self.hold(random.uniform(5, 10))
            cantidad_reabasto = 50
            combustible.release(cantidad_reabasto)
            print(f"Reabastecido {cantidad_reabasto}L en t={env.now():.1f}")
            print(f"Combustible disponible: {combustible.available_quantity():.1f}L")

env = sim.Environment(trace=False)

# Crear resource anónimo: depósito de combustible con 100L iniciales
combustible = sim.Resource("combustible", capacity=200, anonymous=True)
combustible.release(100)  # Llenar inicialmente con 100L

# Crear componentes
for i in range(3):
    Vehiculo(name=f"Vehiculo_{i+1}", at=random.uniform(0, 5))

ReabastecedorCombustible()

# Ejecutar simulación
env.run(till=30)

print("\n--- Estadísticas del resource 'combustible' ---")
combustible.print_statistics()