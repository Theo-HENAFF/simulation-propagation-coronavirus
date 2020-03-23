# https://simpy.readthedocs.io/en/latest/simpy_intro/shared_resources.html

import simpy
import random as r

class Person(object):
    def __init__(self, env,
                 id,
                 contagious_time=None,
                 mortality_transmission_rate=None,
                 vaccine_efficiency=None,
                 health_status='healthful',
                 liste_neighbour = []):

        self.env = env
        self.action = env.process(self.run())

        self.contagious_time = contagious_time
        self.mortality_transmission_rate = mortality_transmission_rate
        self.vaccine_efficiency = vaccine_efficiency  # 0 for no vaccine, 1 for total immunity after vaccination

        self.id = id
        self.health_status = health_status  # healthful/contaminated/dead
        self.liste_neighbour = liste_neighbour

nbre_pers = 100
Xmax = 10  # Nbre max de personnes qu'un individu peut fréquenter
proba_contamination = 0.01
liste_pers = []


def initialisation(nbre_pers):
    for person in range(nbre_pers):
        # Création des voisins
        nbre_neighbours = r.randint(0, Xmax)  # Nbre aléatoire de voisins jusqu'à Xmax
        liste_neighbour = []
        for voisin in range(0, nbre_neighbours):
            n = r.randint(1, nbre_pers)
            liste_neighbour.append(n)

        # Déclaration des personnes
        liste_pers.append(Person(env, id=person, liste_neighbour=liste_neighbour))

    # random conta 1 pers
    id_conta = r.randint(0, nbre_pers)
    liste_pers[id_conta].health_status = 'contaminated'
    print('la personne {} doit arreter de manger de la soupe de chauve souris'.format(id_conta))



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
    env.process(vie(env, 'Car {}'.format(i), bcs, i * 2, 5))

env.run()
