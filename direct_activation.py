import salabim as sim

class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            self.hold(sim.Uniform(5, 15).sample())

class Customer(sim.Component):
    def process(self):
        self.enter(waitingline)
        if clerk_a.ispassive():
            clerk_a.activate()
        elif clerk_b.ispassive():
            clerk_b.activate()
        self.passivate()

class Clerk(sim.Component):
    def __init__(self, name, service_time, service_queue):
        super().__init__(name=name)
        self.service_time = service_time
        self.service_queue = service_queue 
    def process(self):
        while True:
            while len(waitingline) == 0:
                self.passivate()
            customer = waitingline.pop()
            customer.enter(self.service_queue)
            self.hold(self.service_time)
            customer.leave(self.service_queue)
            customer.activate()


env = sim.Environment(trace=False)

waitingline = sim.Queue("Waiting Line")

service_a = sim.Queue("Service A")

service_b = sim.Queue("Service B")

clerk_a = Clerk("Clerk A", sim.Exponential(30).sample(), service_a)
                 
clerk_b = Clerk("Clerk B", sim.Exponential(20).sample(), service_b)

CustomerGenerator()

env.run(till=2000)

waitingline.print_histograms()

waitingline.print_info()