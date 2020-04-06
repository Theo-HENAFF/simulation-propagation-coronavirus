# library used
import random as r
import simpy

# listperson in your simulation
global listperson
listperson = []
global liste_pers
liste_pers = []


def decision(probability):
    if r.random() < probability:
        return True
    else:
        return False


def number_infected():
    """
    calculate the number of infected in listperson
    """
    nb = 0
    for item in listperson:
        if item.status == "sick":
            nb+=1
    return nb


class Person(object):
    def __init__(self, idd, health_status="healthful", liste_neighbour=[]):
        self.idd = idd
        self.health_status = health_status  # healthful/cont_without_s/contaminated/dead
        self.liste_neighbour = liste_neighbour

    # def infected(self, id, p):
    #     if self.status == "sick" and listperson[id].status != "sick" :
    #         if r.random() <= p :
    #             listperson[id].status="sick"
    #             print("the person {} is infected by person {} ".format( self.idd, listperson[id].id ))
    #         else:
    #             print("you have a chance you are not infected")
    #     elif listperson[id].status == "sick" and self.status != "sick":
    #         if r.random() <= p :
    #             self.status = "sick"
    #             print("the person {} is infected by person {} ".format(listperson[id].id, self.idd))
    #         else:
    #             print("you have a chance you are not infected")
    #     else:
    #         print("nothing")
    #         pass

    def infection(self, id_neighbour, proba_contamination):
        # f.write("{} va voir {} \n".format(person.id_person, id_neighbour))
        # Si une des personnes qui se rendnent visite est contaminée (avec ou sans symptômes)
        # il y'a une proba de contamination
        if (self.health_status == "cont_without_s" or self.health_status == "contaminated") and \
                liste_pers[id_neighbour].health_status == "healthful":
            if decision(proba_contamination):
                # f.write("TERRRRRRIIIIBLE {} get coroned \n".format(id_neighbour))
                liste_pers[id_neighbour].health_status = "cont_without_s"
        elif (liste_pers[id_neighbour].health_status == "cont_without_s" or liste_pers[
            id_neighbour].health_status == "contaminated") and self.health_status == "healthful":
            if decision(proba_contamination):
                # f.write("TERRRRRRIIIIBLE {} get coroned \n".format(person.id_person))
                self.health_status = "cont_without_s"






class World(object):
    """
    this is your world (simulation)
    """
    def __init__(self, env, area_zone, meetime):
        self.env = env
        self.meet = simpy.Resource(env, area_zone)
        self.meetime = meetime

    def area(self, idd, num_person, timemeet, p):
        """
        propagation's area
        in this area , one person can meet an other person
        """
        id_neighbour = r.randint(0, len(Person.liste_neighbour))
        print("Person {} : Enter the meeting zone {}".format(id_neighbour, self.env.now))
        listperson[idd].infection(id_neighbour, p)
        yield self.env.timeout(timemeet)
        print("Person {} : Enter the meeting zone {}".format(id_neighbour, self.env.now))


def meet(env, name, cw, idd, num_person, timemeet,p):
    """
    create meet between person (in the area)
    """
    print("{} : wait in order to leave house at {}".format(name, env.now))
    with cw.meet.request() as request:
        yield request
        # meeting zone
        print("{} : Enter in the meeting zone {}".format(name, env.now))
        yield env.process(cw.area(idd, num_person, timemeet, ))
        # exit the meeting
        print('%s exit the meeting zone %.2f.' % (name, env.now))


def setup(env, area_zone, meetime, nber_person, num_tips, p):
    """
    init the simulation
    """
    # Create the World
    world = World(env, area_zone, meetime)

    # Create n person person in your world
    # patient zero ( infected )

    for person in range(nber_person):
        # Création des voisins
        nbre_neighbours = r.randint(0, Xmax)  # Nbre aléatoire de voisins jusqu'à Xmax
        liste_neighbour = []
        for voisin in range(0, nbre_neighbours):
            n = r.randint(0, nber_person - 1)
            liste_neighbour.append(n)
        # Déclaration des personnes
        liste_pers.append(Person(id_person=person, liste_neighbour=liste_neighbour))

    # random conta 1 pers
    id_conta = r.randint(0, nbre_pers)
    liste_pers[id_conta].health_status = 'cont_without_s'
    # f.write('la personne {} doit arreter de manger de la soupe de chauve souris \n'.format(id_conta))

    # start the meet between person
    for i in range(num_tips):
        rand = r.randint(0, nbre_pers)
        env.process(meet(env, 'Person %d' % rand, world, rand, nbre_pers, meetime, p))
    yield env.timeout(r.randint(500 - 2, 500 + 2))


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
        liste_pers.append(Person(id_person=personne, liste_neighbour=liste_neighbour))

    # random conta 1 pers
    id_conta = r.randint(0, nbre_pers)
    liste_pers[id_conta].health_status = 'cont_without_s'
    # f.write('la personne {} doit arreter de manger de la soupe de chauve souris \n'.format(id_conta))
    return liste_pers
