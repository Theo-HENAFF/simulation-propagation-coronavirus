import simpy


class Person(object):
    def __init__(self, env,
                 contagious_time=None,
                 mortality_transmission_rate=None,
                 vaccine_efficiency=None,
                 is_contaminated=False):
        self.env = env
        self.action = env.process(self.run())

        self.contagious_time = contagious_time
        self.mortality_transmission_rate = mortality_transmission_rate
        self.vaccine_efficiency = vaccine_efficiency  # 0 for no vaccine, 1 for total immunity after vaccination

        self.health_status = is_contaminated  # healthful/contaminated/dead

    # Code pas encore vraiment modifie
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

    # Code pas encore vraiment modifie
    def charge(self, duration):
        yield self.env.timeout(duration)

    def insert_vaccine(self, vaccine_efficiency):
        self.vaccine_efficiency = vaccine_efficiency

    def contaminate_neighbours(self, personne):
        personne.is_contaminated = True

        personne.contagious_time = self.contagious_time
        personne.mortality_transmission_rate = self.mortality_transmission_rate
        personne.vaccine_efficiency = self.vaccine_efficiency


env = simpy.Environment()
person = Person(env)


def driver(env, car):
    yield env.timeout(3)
    person.action.interrupt()


env.process(driver(env, person))
env.run(until=15)  # Run pdt 15
