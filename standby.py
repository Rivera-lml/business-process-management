import salabim as sim

class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            self.hold(sim.Uniform(5, 15))

class Customer(sim.Component):
    def process(self):
        self.enter(waitingline)
        self.passivate()
        
class Clerk(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                self.standby()
            self.customer = waitingline.pop()  
            self.hold(sim.Uniform(20, 40))
            self.customer.activate()    


env = sim.Environment(trace=False)


waitingline = sim.Queue("Waiting Line")


for i in range(3):
    Clerk()

CustomerGenerator()


env.run(till=50000)

waitingline.print_histograms()

waitingline.length_of_stay.print_histogram(30,0,10)