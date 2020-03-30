# https://simpy.readthedocs.io/en/latest/simpy_intro/shared_resources.html

import random as r
import simpy


nbre_pers = 100
Xmax = 3  # Nbre max de personnes qu'un individu peut fréquenter
proba_contamination = 0.90
liste_pers = []
liste_dead = []
proba_guerison = 0.5
proba_meet = 0.8
malus_conta = 2  # Malus si personne conta divise la proba de meeting
nbre_jour = 10


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


def decision(probability):
    if r.random() < probability:
        return True
    else:
        return False


def initialisation(nbre_pers):
    liste_pers = []
    for personne in range(nbre_pers):
        # Création des voisins
        nbre_neighbours = r.randint(0, Xmax)  # Nbre aléatoire de voisins jusqu'à Xmax
        liste_neighbour = []
        for voisin in range(0, nbre_neighbours):
            n = r.randint(0, nbre_pers - 1)
            liste_neighbour.append(n)

        # Déclaration des personnes
        liste_pers.append(Person(env=env, id_person=personne, liste_neighbour=liste_neighbour))

    # random conta 1 pers
    id_conta = r.randint(0, nbre_pers)
    liste_pers[id_conta].health_status = 'cont_without_s'
    f.write('la personne {} doit arreter de manger de la soupe de chauve souris \n'.format(id_conta))
    return liste_pers


# ===================================================================================================
# Fonction pour simuler un meeting
# ===================================================================================================
def meeting(person, id_neighbour):
    f.write("{} va voir {} \n".format(person.id_person, id_neighbour))
    # with meeting_point.request() as req:

    # Si une des personnes qui se rendnent visite est contaminée (avec ou sans symptômes) il y'a une proba de contamination
    if (person.health_status == "cont_without_s" or person.health_status == "contaminated") and \
            liste_pers[id_neighbour].health_status == "healthful":
        if decision(proba_contamination):
            f.write("TERRRRRRIIIIBLE {} get coroned \n".format(id_neighbour))
            liste_pers[id_neighbour].health_status = "cont_without_s"
        # yield req
    elif (liste_pers[id_neighbour].health_status == "cont_without_s" or liste_pers[
        id_neighbour].health_status == "contaminated") and person.health_status == "healthful":
        if decision(proba_contamination):
            f.write("TERRRRRRIIIIBLE {} get coroned \n".format(person.id_person))
            person.health_status = "cont_without_s"
        # yield req


def gestion(person):
    if person.health_status == "cont_without_s" or person.health_status == "contaminated":
        person.contagious_time += 1

    # A bout de X unités de temps elle commence à développer des symptômes
    if person.contagious_time > 3 and person.health_status == "cont_without_s":
        person.health_status = "contaminated"
        f.write("MINCE {} développe des symptomes \n".format(person.id_person))

    # A bout de X temps la personne contaminée est gueri avec une proba de guerison
    elif person.contagious_time > 5 and person.health_status == "contaminated":
        if decision(proba_guerison):
            person.health_status = "cured"
            f.write("YOUPI {} a guéri \n".format(person.id_person))

    # Si apres X temps elle n'est pas guéri la personn meurt
    if person.contagious_time > 7 and person.health_status == "contaminated":
        person.health_status = 'dead'
        f.write("DOMMAGE {} à manger le pissenlit par la racine \n".format(person.id_person))


# ===================================================================================================
# Fonction globale d'une journee
# ===================================================================================================
def vie(env, liste_pers, nbre_jour):
    # Une personne voit avec une probabilité forte son entrourage (ses voisins, ses collègues de travail)
    # Gestion rencontre et contagion
    for journee in range(nbre_jour):
        for person in liste_pers:
            # On check si la personne est encore en vie
            if person.health_status != "dead":
                for id_neighbour in person.liste_neighbour:
                    # La personne va voir dans ses voisins qui n'est pas mort et lui rend visite
                    if liste_pers[id_neighbour].health_status == "dead":
                        f.write("IL a sonné mais PERSONNE a rep \n")
                    # Si aucun des 2 n'a de symptomes, le meeting reste normal
                    elif (liste_pers[id_neighbour].health_status != "contaminated" or person.health_status != "contaminated") and decision(proba_meet):
                        meeting(person, id_neighbour)
                    # Si une des 2 a des symptomes, la proba de rencontre est grandement diminué
                    elif (liste_pers[id_neighbour].health_status == "contaminated" or person.health_status == "contaminated") and decision(proba_meet/malus_conta):
                        meeting(person, id_neighbour)
                    else:
                        f.write("pas de rencontre NON NON NON \n")

            # Partie gestion de temporalité. Chaque personne à un compteur de temps de contamination.
            gestion(person)
        f.write("\n Trop bien fin de la journée {} \n".format(journee + 1))
        yield env.timeout(1)


env = simpy.Environment()
meeting_point = simpy.Resource(env, capacity=2)  # Seulement 2 personnes peuvent se rencontrer
f = open("result.txt", "r+")
f.truncate(0)
liste_pers = initialisation(nbre_pers)

env.process(vie(env, liste_pers, nbre_jour))

env.run()

f.close()
