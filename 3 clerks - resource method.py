import salabim as sim

class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            self.hold(sim.Uniform(5, 15).sample())

class Customer(sim.Component):
    def process(self):
        self.request(clerks)
        self.hold(30)

env = sim.Environment(trace=False)


clerks = sim.Resource("Clerks", capacity=3)

CustomerGenerator()

env.run(till=50000)

clerks.print_statistics()
clerks.print_info()