# https://simpy.readthedocs.io/en/latest/simpy_intro/shared_resources.html

import simpy
import random as r

def decision(probability):
    if r.random() < probability:
        return True
    else :
        return False

class Person(object):
    def __init__(self, env,
                 id_person,
                 contagious_time=None,
                 mortality_transmission_rate=None,
                 vaccine_efficiency=None,
                 health_status='healthful',
                 liste_neighbour=[]):

        # self.env = env
        # self.action = env.process(self.run())

        self.contagious_time = contagious_time
        self.mortality_transmission_rate = mortality_transmission_rate
        self.vaccine_efficiency = vaccine_efficiency  # 0 for no vaccine, 1 for total immunity after vaccination

        self.id_person = id_person
        self.health_status = health_status  # healthful/cont_without_s/contaminated/dead
        self.cured = False
        self.liste_neighbour = liste_neighbour

nbre_pers = 100
Xmax = 30  # Nbre max de personnes qu'un individu peut fréquenter
proba_contamination = 0.90
liste_pers = []


def initialisation(nbre_pers):
    liste_pers = []
    for person in range(nbre_pers):
        # Création des voisins
        nbre_neighbours = r.randint(0, Xmax)  # Nbre aléatoire de voisins jusqu'à Xmax
        liste_neighbour = []
        for voisin in range(0, nbre_neighbours):
            n = r.randint(1, nbre_pers)
            liste_neighbour.append(n)

        # Déclaration des personnes
        liste_pers.append(Person(env, id_person=person, liste_neighbour=liste_neighbour))

    # random conta 1 pers
    id_conta = r.randint(0, nbre_pers)
    liste_pers[id_conta].health_status = 'contaminated'
    print('la personne {} doit arreter de manger de la soupe de chauve souris'.format(id_conta))
    return liste_pers

def vie(env, person):
    # Une personne voit avec une probabilité forte son entrourage (ses voisins, ses collègues de travail)
    proba_meet = 0.75
    for neighbour in person.liste_neighbour:
        if decision(proba_meet):
            print('{} va voir {}'.format(person.id_person, neighbour.id_person))
            with meeting_point.request() as req:
                if decision(proba_contamination):
                    print('Terrrrriiiible {} get coroned'.format(neighbour.id_person))
                    neighbour.health_status = "cont_without_s"
                yield req


env = simpy.Environment()
meeting_point = simpy.Resource(env, capacity=2)  # Seulement 2 personnes peuvent se rencontrer
liste_pers = initialisation(nbre_pers)

for person in range(len(liste_pers)):
    env.process(vie(env, person))

env.run()


