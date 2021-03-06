import random as r
import simpy

# list_person and stats are core elements for the simulation
global list_pers, stats, day_count
list_pers = []
day_count = 0
stats = {"healthful": [],
         "cont_without_s": [],
         "contaminated": [],
         "cured": [],
         "vaccinated": [],
         "dead": [],
         "rate": []}

# Load the log file
log = open("logs.txt", "w")


# Simple function returning True or False when you input a number between 0 and 1
def decision(probability):
    if r.random() < probability:
        return True
    else:
        return False


class Person(object):
    def __init__(self, idd, contagious_time=0, vaccinated_time=0, health_status="healthful", list_neighbour=[]):
        self.idd = idd  # The idd is also the index in list_person

        # there is 6 health_status healthful/cont_without_s/contaminated/cured/vaccinated/dead
        self.health_status = health_status

        # list_neighbour contain the index of the persons this person can meet
        self.list_neighbour = list_neighbour

        # number of day the person has been contaminated
        self.contagious_time = contagious_time

        # number of day the person has been contaminated
        self.vaccinated_time = vaccinated_time

    # If one of the people meeting is infected (with or without symptoms)
    # there is a proba of contamination
    def infection(self, id_neighbour, proba_contamination):

        if (self.health_status == "cont_without_s" or self.health_status == "contaminated") and \
                list_pers[id_neighbour].health_status == "healthful":
            if decision(proba_contamination):
                list_pers[id_neighbour].health_status = "cont_without_s"
                log.write("Person {} has been contaminated by {} \n".format(list_pers[id_neighbour].idd, self.idd))

        elif (list_pers[id_neighbour].health_status == "cont_without_s"
              or list_pers[id_neighbour].health_status == "contaminated") and self.health_status == "healthful":
            if decision(proba_contamination):
                self.health_status = "cont_without_s"
                log.write("Person {} has been contaminated by {} \n".format(self.idd, list_pers[id_neighbour].idd))


class World(object):

    def __init__(self, env, area_zone, meetime):
        self.env = env
        self.meet = simpy.Resource(env, area_zone)
        self.meetime = meetime

    # The zone where 2 people meet
    def area(self, idd, num_person, timemeet, proba_conta):
        # We randomly choose an id of the list_neighbour of the person
        id_neighbour = list_pers[idd].list_neighbour[r.randint(0, len(list_pers[idd].list_neighbour) - 1)]

        list_pers[idd].infection(id_neighbour, proba_conta)
        yield self.env.timeout(timemeet)


# The meeting
def meet(env, cw, idd, num_person, timemeet, proba_conta):
    with cw.meet.request() as request:
        yield request
        # Insert one person in the meeting zone
        yield env.process(cw.area(idd, num_person, timemeet, proba_conta))


# Management of the health_status
def gestion(proba_death, time_contaminated,
            proba_heal,
            time_without_s,
            time_too_much,
            proba_death_during_rea,
            time_disco_vac,
            num_vac,
            effect_vac):

    global day_count
    day_count += 1
    if day_count >= time_disco_vac:
        for i in range(num_vac):
            idd_pers = r.randint(0, len(list_pers) - 1)
            if list_pers[idd_pers].health_status == "healthful" and list_pers[idd_pers].vaccinated_time == 0:
                list_pers[idd_pers].vaccinated_time = 1

    for person in list_pers:

        # The vaccine take time to be fully effective
        if 1 <= person.vaccinated_time < effect_vac:
            person.vaccinated_time += 1
            if person.vaccinated_time == effect_vac:
                person.health_status = "vaccinated"

        # for each person sick we add a day of contamination
        if person.health_status == "cont_without_s" or person.health_status == "contaminated":
            person.contagious_time += 1

        # After X units of time the person begins to develop symptoms.
        if person.contagious_time > time_without_s and person.health_status == "cont_without_s":
            # Everybody has a chance to die very fast (diabetes, obesity, elders ...)
            if decision(proba_death):
                person.health_status = "dead"
                log.write("Person {} is dead. \n".format(person.idd))
            else:
                person.health_status = "contaminated"
                log.write("Symptoms appeared for person {} \n".format(person.idd))

        # At the end of X time the infected person has a chance to be healed with a proba_heal each day
        elif person.contagious_time > time_contaminated and person.health_status == "contaminated":
            if decision(proba_heal):
                person.health_status = "cured"
                log.write("Person {} is now cured. \n".format(person.idd))

        # If she's not cured in time, she has a good chance of dying.
        elif person.contagious_time > time_too_much and decision(
                proba_death_during_rea) and person.health_status == "contaminated":
            person.health_status = 'dead'
            log.write("Person {} is dead. \n".format(person.idd))


# Each day we will count the number of people with each health_status to see the evolution
def add_stats():
    count_healthful = 0
    count_cont_without_s = 0
    count_contaminated = 0
    count_cured = 0
    count_vaccinated = 0
    count_dead = 0

    for person in list_pers:
        if person.health_status == "healthful":
            count_healthful += 1
        elif person.health_status == "cont_without_s":
            count_cont_without_s += 1
        elif person.health_status == "contaminated":
            count_contaminated += 1
        elif person.health_status == "cured":
            count_cured += 1
        elif person.health_status == "vaccinated":
            count_vaccinated += 1
        elif person.health_status == "dead":
            count_dead += 1

    stats["healthful"].append(count_healthful)
    stats["cont_without_s"].append(count_cont_without_s)
    stats["contaminated"].append(count_contaminated)
    stats["cured"].append(count_cured)
    stats["vaccinated"].append(count_vaccinated)
    stats["dead"].append(count_dead)
    stats["rate"].append(count_cont_without_s+count_contaminated+count_dead)


# Setup the simualtion by mainly adding nber_person to list_pers
def setup(nber_person, max_neighbours):
    stats["healthful"].append(nber_person - 1)
    stats["cont_without_s"].append(1)
    stats["contaminated"].append(0)
    stats["cured"].append(0)
    stats["vaccinated"].append(0)
    stats["dead"].append(0)

    for person in range(nber_person):
        # Creating the list_neighbour
        nbre_neighbours = r.randint(0, max_neighbours)  # Random number of neighbours up to max_neighbours
        list_neighbour = []
        for voisin in range(0, nbre_neighbours):
            n = r.randint(0, nber_person - 1)
            list_neighbour.append(n)
        # Declaration of Persons
        list_pers.append(Person(idd=person, list_neighbour=list_neighbour))

    # random contamination of 1 person
    id_conta = r.randint(0, nber_person)
    list_pers[id_conta].health_status = 'cont_without_s'
    print('la personne {} doit arreter de manger de la soupe de chauve souris \n'.format(id_conta))
    log.write("Person {} is patient zero  \n".format(id_conta))


def day(env, area_zone, meetime, nber_person, proba_conta, proba_meet, malus):
    world = World(env, area_zone, meetime)
    # start the meet between person, each person meet a random neighbour
    for i in range(len(list_pers)):
        if len(list_pers[i].list_neighbour) == 0:
            pass
        else:
            if list_pers[i].health_status != "contaminated" and list_pers[i].health_status != "dead":
                if decision(proba_meet):
                    env.process(meet(env, world, i, nber_person, meetime, proba_conta))
                    yield env.timeout(r.randint(500 - 2, 500 + 2))
            # If the person has symptom, it is more difficult to meet somebody
            elif list_pers[i].health_status == "contaminated":
                if decision(proba_meet / malus):
                    env.process(meet(env, world, i, nber_person, meetime, proba_conta))
                    yield env.timeout(r.randint(500 - 2, 500 + 2))
