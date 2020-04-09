# library used
import random as r
import simpy

# listperson in your simulation
global liste_pers
liste_pers = []
global stats
stats = {"healthful": [], "cont_without_s": [], "contaminated": [], "cured": [], "dead": []}

def decision(probability):
    if r.random() < probability:
        return True
    else:
        return False


class Person(object):
    def __init__(self, idd, contagious_time=0, health_status="healthful", liste_neighbour=[]):
        self.idd = idd
        self.health_status = health_status  # healthful/cont_without_s/contaminated/dead
        self.liste_neighbour = liste_neighbour
        self.contagious_time = contagious_time

    def infection(self, id_neighbour, proba_contamination):
        #print("{} va voir {} \n".format(self.idd, id_neighbour))
        # Si une des personnes qui se rendnent visite est contaminée (avec ou sans symptômes)
        # il y'a une proba de contamination
        if (self.health_status == "cont_without_s" or self.health_status == "contaminated") and \
                liste_pers[id_neighbour].health_status == "healthful":
            if decision(proba_contamination):
                # f.write("TERRRRRRIIIIBLE {} get coroned \n".format(id_neighbour))
                #print("TERRRRRRIIIIBLE {} get coroned \n".format(id_neighbour))
                liste_pers[id_neighbour].health_status = "cont_without_s"

        elif (liste_pers[id_neighbour].health_status == "cont_without_s" or liste_pers[
            id_neighbour].health_status == "contaminated") and self.health_status == "healthful":
            if decision(proba_contamination):
                # f.write("TERRRRRRIIIIBLE {} get coroned \n".format(person.idd))
                #print("TERRIBLE {} get coroned \n".format(self.idd))
                self.health_status = "cont_without_s"


class World(object):
    """
    this is your world (simulation)
    """
    def __init__(self, env, area_zone, meetime):
        self.env = env
        self.meet = simpy.Resource(env, area_zone)
        self.meetime = meetime

    def area(self, idd, num_person, timemeet, proba_conta):
        """
        propagation's area
        in this area , one person can meet an other person
        """


        id_neighbour = liste_pers[idd].liste_neighbour[r.randint(0, len(liste_pers[idd].liste_neighbour) - 1 )]

        ##print("Person {} : Enter the meeting zone {}".format(id_neighbour, self.env.now))
        liste_pers[idd].infection(id_neighbour, proba_conta)
        yield self.env.timeout(timemeet)
        #print("Person {} : Enter the meeting zone {}".format(id_neighbour, self.env.now))


def meet(env, name, cw, idd, num_person, timemeet, proba_conta):
    """
    create meet between person (in the area)
    """
    #print("{} : wait in order to leave house at {}".format(name, env.now))
    with cw.meet.request() as request:
        yield request
        # meeting zone
        #print("{} : Enter in the meeting zone {}".format(name, env.now))
        yield env.process(cw.area(idd, num_person, timemeet, proba_conta))
        # exit the meeting
        #print('%s exit the meeting zone %.2f.' % (name, env.now))


def gestion(proba_mort, time_contaminated, proba_guerison, time_without_s, time_too_much):
    for person in liste_pers:
        if person.health_status == "cont_without_s" or person.health_status == "contaminated":
            person.contagious_time += 1

        # A bout de X unités de temps elle commence à développer des symptômes
        if person.contagious_time > time_without_s and person.health_status == "cont_without_s":
            # pour simuler si la personne meurt rapidement
            if decision(proba_mort):
                person.health_status = "dead"
            else:
                person.health_status = "contaminated"
            # f.write("MINCE {} développe des symptomes \n".format(person.idd))
            #print("MINCE {} développe des symptomes \n".format(person.idd))


        # A bout de X temps la personne contaminée est gueri avec une proba de guerison
        elif person.contagious_time > time_contaminated and person.health_status == "contaminated":
            if decision(proba_guerison):
                person.health_status = "cured"
                # f.write("YOUPI {} a guéri \n".format(person.idd))
                #print("YOUPI {} a guéri \n".format(person.idd))

        # Si apres X temps elle n'est pas guéri elle a de grande chance de mourir
        elif person.contagious_time > time_too_much and decision(proba_mort) and person.health_status == "contaminated":
            person.health_status = 'dead'
            # f.write("DOMMAGE {} à manger le pissenlit par la racine \n".format(person.idd))
            #print("DOMMAGE {} à manger le pissenlit par la racine \n".format(person.idd))

def add_stats():
    count_healthful = 0
    count_cont_without_s = 0
    count_contaminated = 0
    count_cured = 0
    count_dead = 0

    for person in liste_pers:
        if person.health_status == "healthful":
            count_healthful += 1
        elif person.health_status == "cont_without_s":
            count_cont_without_s += 1
        elif person.health_status == "contaminated":
            count_contaminated += 1
        elif person.health_status == "cured":
            count_cured += 1
        elif person.health_status == "dead":
            count_dead += 1

    stats["healthful"].append(count_healthful)
    stats["cont_without_s"].append(count_cont_without_s)
    stats["contaminated"].append(count_contaminated)
    stats["cured"].append(count_cured)
    stats["dead"].append(count_dead)


def setup(nber_person, max_neighbours):
    stats["healthful"].append(nber_person-1)
    stats["cont_without_s"].append(1)
    stats["contaminated"].append(0)
    stats["cured"].append(0)
    stats["dead"].append(0)

    for person in range(nber_person):
        # Création des voisins
        nbre_neighbours = r.randint(0, max_neighbours)  # Nbre aléatoire de voisins jusqu'à max_neighbours
        liste_neighbour = []
        for voisin in range(0, nbre_neighbours):
            n = r.randint(0, nber_person - 1)
            liste_neighbour.append(n)
        # Déclaration des personnes
        liste_pers.append(Person(idd=person, liste_neighbour=liste_neighbour))

    # random conta 1 pers
    id_conta = r.randint(0, nber_person)
    liste_pers[id_conta].health_status = 'cont_without_s'
    # f.write('la personne {} doit arreter de manger de la soupe de chauve souris \n'.format(id_conta))
    #print('la personne {} doit arreter de manger de la soupe de chauve souris \n'.format(id_conta))



def day(env, area_zone, meetime, nber_person, capacity_area, proba_conta,PROBA_MEET,MALUS):
    world = World(env, area_zone, meetime)

    # start the meet between person
    for i in range(len(liste_pers)):
        # rand = r.randint(0, nber_person-1)
        if len(liste_pers[i].liste_neighbour) == 0 :
            pass
        else :
            if liste_pers[i].health_status != "contaminated" and liste_pers[i].health_status != "dead":
                if decision(PROBA_MEET):
                    env.process(meet(env, 'Person %d' % i, world, i, nber_person, meetime, proba_conta))
                    #print("DEBUT MEETING {}".format(i))
                    yield env.timeout(r.randint(500 - 2 , 500 + 2) )
                    #print("FIN MEETING {}".format(i))
            elif liste_pers[i].health_status == "contaminated":
                if decision(PROBA_MEET/MALUS):
                    env.process(meet(env, 'Person %d' % i, world, i, nber_person, meetime, proba_conta))
                    #print("DEBUT MEETING {}".format(i))
                    yield env.timeout(r.randint(500 - 2 , 500 + 2) )
                    #print("FIN MEETING {}".format(i))






