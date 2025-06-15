import salabim as sim

class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            self.hold(sim.Uniform(5, 15).sample())

class Customer(sim.Component):
    def process(self):
        self.enter(cola_clientes)
        for clerk in clerks:
            if clerk.status() == sim.passive:
                clerk.activate()
                break
        self.passivate()
        

class Clerk(sim.Component):
    def process(self):
        while True:
            while len(cola_clientes) == 0:
                self.passivate()
            self.customer = cola_clientes.pop()
            self.hold(30)
            self.customer.activate()


env = sim.Environment(trace=False)
CustomerGenerator()
clerks = [Clerk() for _ in range(3)]
cola_clientes = sim.Queue("Cola de clientes")  

env.run(50000)

cola_clientes.print_histograms()
cola_clientes.print_info()