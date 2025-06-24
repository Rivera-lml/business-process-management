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

# Animation setup
sim.AnimateQueue(waitingline, x=100, y=100, title="Waiting Line")
sim.AnimateQueue(service_a, x=400, y=100, title="Clerk A Service")
sim.AnimateQueue(service_b, x=700, y=100, title="Clerk B Service")

sim.AnimateMonitor(waitingline.length, x=100, y=300, width=800, height=100, title="Waiting Line Length")
sim.AnimateMonitor(service_a.length, x=100, y=420, width=800, height=100, title="Service A Queue Length")
sim.AnimateMonitor(service_b.length, x=100, y=540, width=800, height=100, title="Service B Queue Length")

env.animate(True)
env.speed(50)

env.run(till=2000)