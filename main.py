class Person(object):
    def __init__(self, env, contagious_time, mortality_transmission_rate):
        self.env = env
        self.action = env.process(self.run())
        self.contagious_time = contagious_time
        self.mortality_transmission_rate = mortality_transmission_rate
        self.vaccine_efficiency = vaccine_efficiency

def run(self):
    while True:
        print('Start parking and charging at %d' % self.env.now)
        charge_duration = 5
        # We may get interrupted while charging the battery
        try:
            yield self.env.process(self.charge(charge_duration))
        except simpy.Interrupt:
            # When we received an interrupt, we stop charging and
            # switch to the "driving" state
            print('Was interrupted. Hope, the battery is full enough ')

        print('Start driving at %d' % self.env.now)
        trip_duration = 2
        yield self.env.timeout(trip_duration)

def charge(self, duration):
    yield self.env.timeout(duration)
