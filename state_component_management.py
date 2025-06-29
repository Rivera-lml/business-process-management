import salabim as sim

class Maquina(sim.Component):
    def process(self):
        print("Máquina trabajando...")
        self.hold(50)
        print("Máquina ha terminado de trabajar")
        self.passivate()

class Trabajador(sim.Component):
    def process(self):
        print("Trabajador activando la máquina...")
        maquina = Maquina() 
        maquina.activate() # activar la máquina para comenzar su proceso
        self.hold(10)
        
        print("Trabajador esperando que la máquina termine...") 
        self.hold(50) # el trabajador espera el tiempo que la máquina tarda en trabajar

        print("Trabajador continúa después que la máquina terminó")
        print("trabajador está en estado pasivo después de completar su tarea")
        self.passivate() # el trabajador pasa al estado pasivo después de terminar su tarea
        
        
sim_env = sim.Environment(trace=False)

trabajador1 = Trabajador()
trabajador1.activate()

sim_env.run()