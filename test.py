# https://simpy.readthedocs.io/en/latest/simpy_intro/shared_resources.html

import simpy


class Person(object):
    def __init__(self, env,
                 id,
                 contagious_time=None,
                 mortality_transmission_rate=None,
                 vaccine_efficiency=None,
                 is_contaminated=False):

        self.env = env
        self.action = env.process(self.run())

        self.contagious_time = contagious_time
        self.mortality_transmission_rate = mortality_transmission_rate
        self.vaccine_efficiency = vaccine_efficiency  # 0 for no vaccine, 1 for total immunity after vaccination

        self.id = id
        self.health_status = is_contaminated  # healthful/contaminated/dead


liste_pers = []


def initialisation(nbre_pers):
    for person in range(nbre_pers):
        liste_pers.append(Person(env, id=person))


def vie(env, name, person, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))
    with bcs.request() as req:
        yield req

        # Charge the battery
    print('%s starting to charge at %s' % (name, env.now))
    yield env.timeout(charge_duration)
    print('%s leaving the bcs at %s' % (name, env.now))


env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

for i in range(4):
    env.process(car(env, 'Car {}'.format(i), bcs, i * 2, 5))

env.run()
