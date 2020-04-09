####################################
# Version : python 3.6.9 64bits    #
####################################

####################################
# pip3 install sympy               #
####################################

####################################
# run this commande in the shell   #
# python3 simulation.py > log.txt  #
####################################

# import this library

import random
import simpy
import yaml

# simulation function
import utils



# main of the simulation
if __name__ == "__main__":

    #load the config file
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)

    # define simulation's values
    RANDOM_SEED = cfg['config']['RANDOM_SEED']
    NUM_AREA = cfg['config']['NUM_AREA']
    TIMEMEET = cfg['config']['TIMEMEET']
    NUM_PERSON = cfg['config']['NUM_PERSON']
    NUM_DAY = cfg['config']['NUM_DAY']
    CAPACITY_AREA = cfg['config']['CAPACITY_AREA']
    SIM_TIME = cfg['config']['SIM_TIME']
    proba_conta = cfg['config']['PROBA_CONTAMINATION']
    MAX_NEIGHBOURS = cfg['config']['MAX_NEIGHBOURS']
    PROBA_HEAL = cfg['config']["PROBA_HEAL"]
    PROBA_DEATH = cfg['config']["PROBA_DEATH"]
    TIME_WITHOUT_S = cfg['config']["TIME_WITHOUT_S"]
    TIME_CONTAMINATED = cfg['config']["TIME_CONTAMINATED"]
    TIME_TOO_MUCH = cfg['config']["TIME_TOO_MUCH"]

    # This helps reproducing the results
    random.seed(RANDOM_SEED)

    # Setup the simulation
    utils.setup(nber_person=NUM_PERSON, max_neighbours=MAX_NEIGHBOURS)

    # cycle
    for day in range(NUM_DAY):

        # Create an environment and start the setup process
        env = simpy.Environment()

        # Setup and start the simulation
        env.process(utils.day(env=env,
                              area_zone=NUM_AREA,
                              meetime=TIMEMEET,
                              nber_person=NUM_PERSON,
                              capacity_area=CAPACITY_AREA,
                              proba_conta=proba_conta))

        # Add temporality to the simulation
        utils.gestion(proba_mort=PROBA_DEATH,
                      time_contaminated=TIME_CONTAMINATED,
                      proba_guerison=PROBA_HEAL,
                      time_without_s=TIME_WITHOUT_S,
                      time_too_much=TIME_TOO_MUCH)

        utils.add_stats()
        # Execute!
        env.run(until=SIM_TIME)

        print("====================== end day {} ======================".format(day))
    print("STATS : ", utils.stats)
