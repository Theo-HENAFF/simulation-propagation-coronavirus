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
                 contagious_time=0,
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

nbre_pers = 150
Xmax = 3  # Nbre max de personnes qu'un individu peut fréquenter
proba_contamination = 0.90
liste_pers = []
liste_dead = []
proba_guerison = 0.0002
proba_meet = 0.99
nbre_jour = 11

def initialisation(nbre_pers):
    liste_pers = []
    for personne in range(nbre_pers):
        # Création des voisins
        nbre_neighbours = r.randint(0, Xmax)  # Nbre aléatoire de voisins jusqu'à Xmax
        liste_neighbour = []
        for voisin in range(0, nbre_neighbours):
            n = r.randint(0, nbre_pers-1)
            liste_neighbour.append(n)

        # Déclaration des personnes
        liste_pers.append(Person(env=env, id_person=personne, liste_neighbour=liste_neighbour))

    # random conta 1 pers
    id_conta = r.randint(0, nbre_pers)
    liste_pers[id_conta].health_status = 'cont_without_s'
    print('la personne {} doit arreter de manger de la soupe de chauve souris'.format(id_conta))
    f.write('la personne {} doit arreter de manger de la soupe de chauve souris \n'.format(id_conta))
    return liste_pers

def vie(env, liste_pers,nbre_jour):
    # Une personne voit avec une probabilité forte son entrourage (ses voisins, ses collègues de travail)
    for journee in range(nbre_jour) :
        for person in liste_pers:
            for id_neighbour in person.liste_neighbour:
                if decision(proba_meet) and liste_pers[id_neighbour].health_status != 'dead' :
                    print('{} va voir {}'.format(person.id_person, id_neighbour))
                    f.write('{} va voir {} \n'.format(person.id_person, id_neighbour))
                    # with meeting_point.request() as req:
                    if (person.health_status == 'cont_without_s' or person.health_status == 'contaminated') and liste_pers[id_neighbour].health_status == 'healthful':
                        if decision(proba_contamination):
                            print('Terrrrriiiible {} get coroned'.format(id_neighbour))
                            f.write('Terrrrriiiible {} get coroned \n'.format(id_neighbour))
                            liste_pers[id_neighbour].health_status = "cont_without_s"
                        #yield req
                    elif (liste_pers[id_neighbour].health_status == 'cont_without_s' or liste_pers[id_neighbour].health_status == 'contaminated') and person.health_status == 'healthful':
                        if decision(proba_contamination):
                            print('Terrrrriiiible {} get coroned'.format(person.id_person))
                            f.write('Terrrrriiiible {} get coroned \n'.format(person.id_person))
                            person.health_status = "cont_without_s"

                        #yield req
            if person.health_status == 'cont_without_s' or person.health_status == 'contaminated':
                person.contagious_time += 1
                if person.contagious_time > 3 and person.health_status == 'cont_without_s':
                    person.health_status = 'contaminated'
                    print('MINCE {} développe des symptomes'.format(person.id_person))
                    f.write('MINCE {} développe des symptomes \n'.format(person.id_person))
                elif person.contagious_time > 5 and person.health_status == "contaminated" :
                    if decision(proba_guerison) :
                        person.health_status = 'cured'
                        print('YOUPI {} a guéri'.format(person.id_person))
                        f.write('YOUPI {} a guéri \n'.format(person.id_person))
                if person.contagious_time > 7 and person.health_status == 'contaminated':
                    person.health_status = 'dead'
                    print('CHEH {} à claqué'.format(person.id_person))
                    f.write('CHEH {} à claqué \n'.format(person.id_person))

        print("\n Trop bien fin de la journée {} \n".format(journee +1))
        f.write("\n Trop bien fin de la journée {} \n".format(journee +1 ))
        yield env.timeout(1)






env = simpy.Environment()
meeting_point = simpy.Resource(env, capacity=2)  # Seulement 2 personnes peuvent se rencontrer
f = open("result.txt", "a")
liste_pers = initialisation(nbre_pers)


env.process(vie(env, liste_pers,nbre_jour))

env.run()
f.close()


