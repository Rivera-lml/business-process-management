import salabim as sim

class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            self.hold(sim.Uniform(5, 15))

class Customer(sim.Component):
    def process(self):
        self.enter(waitingline)
        worktodo.trigger(max=1)
        self.passivate()
        

class Clerk(sim.Component):
    def process(self):
        while True:
            if len(waitingline) == 0:
                self.wait((worktodo, True, 1))
            self.customer = waitingline.pop()
            self.hold(30)
            self.customer.activate()
                

env = sim.Environment(trace=False)


worktodo = sim.State("Work to do")

waitingline = sim.Queue("Waiting Line")

for i in range(3):
    Clerk()

CustomerGenerator()

env.run(till=50000)

waitingline.print_histograms()
worktodo.print_histograms()