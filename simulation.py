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
    NUM_CYCLE_OUTPUT = cfg['config']['NUM_CYCLE_OUTPUT']
    CAPACITY_AREA = cfg['config']['CAPACITY_AREA']
    SIM_TIME = cfg['config']['SIM_TIME']
    proba_conta = cfg['config']['PROBA_CONTAMINATION']
    MAX_NEIGHBOURS = cfg['config']['MAX_NEIGHBOURS']
    # This helps reproducing the results
    random.seed(RANDOM_SEED)

    # cycle
    for c in range(NUM_CYCLE_OUTPUT):

        # Create an environment and start the setup process
        env = simpy.Environment()

        # Setup and start the simulation
        env.process(utils.setup(env=env, area_zone=NUM_AREA, meetime=TIMEMEET, nber_person=NUM_PERSON, capacity_area=CAPACITY_AREA, max_neighbours=MAX_NEIGHBOURS, proba_conta=proba_conta))

        # Execute!
        env.run(until=SIM_TIME)
        print("====================== end cycle {} ======================".format(c))
