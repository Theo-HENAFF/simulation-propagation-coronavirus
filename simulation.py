import simpy
import yaml
import matplotlib.pyplot as plt
import numpy as np
import utils


# main of the simulation
if __name__ == "__main__":

    # Load the config file
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)

    # define simulation's values
    NUM_AREA = cfg['config']['NUM_AREA']
    TIMEMEET = cfg['config']['TIMEMEET']
    NUM_PERSON = cfg['config']['NUM_PERSON']
    NUM_DAY = cfg['config']['NUM_DAY']
    CAPACITY_AREA = cfg['config']['CAPACITY_AREA']
    proba_conta = cfg['config']['PROBA_CONTAMINATION']
    MAX_NEIGHBOURS = cfg['config']['MAX_NEIGHBOURS']
    PROBA_HEAL = cfg['config']["PROBA_HEAL"]
    PROBA_DEATH = cfg['config']["PROBA_DEATH"]
    TIME_WITHOUT_S = cfg['config']["TIME_WITHOUT_S"]
    TIME_CONTAMINATED = cfg['config']["TIME_CONTAMINATED"]
    TIME_TOO_MUCH = cfg['config']["TIME_TOO_MUCH"]
    PROBA_MEET = cfg['config']["PROBA_MEET"]
    MALUS = cfg['config']["MALUS"]
    PROBA_DEATH_DURING_REA = cfg['config']["PROBA_DEATH_DURING_REA"]


# =================================================================================
# Simulation
# =================================================================================
    # Setup the simulation
    utils.setup(nber_person=NUM_PERSON, max_neighbours=MAX_NEIGHBOURS)

    # Run the simulation
    for day in range(NUM_DAY):

        # Create an environment and start the setup process
        env = simpy.Environment()

        # Setup and start the simulation
        env.process(utils.day(env=env,
                              area_zone=NUM_AREA,
                              meetime=TIMEMEET,
                              nber_person=NUM_PERSON,
                              capacity_area=CAPACITY_AREA,
                              proba_conta=proba_conta,
                              proba_meet=PROBA_MEET,
                              malus=MALUS))

        # Add temporality to the simulation
        utils.gestion(proba_death=PROBA_DEATH,
                      time_contaminated=TIME_CONTAMINATED,
                      proba_heal=PROBA_HEAL,
                      time_without_s=TIME_WITHOUT_S,
                      time_too_much=TIME_TOO_MUCH,
                      proba_death_during_rea=PROBA_DEATH_DURING_REA)
        # Get stats for the visualization
        utils.add_stats()
        # Execute
        env.run(until=NUM_PERSON * 800)

        print("END OF DAY {} OUT OF {}".format(day, NUM_DAY))


# =================================================================================
# Visualization
# =================================================================================
    stats = utils.stats
    x = np.linspace(0, NUM_DAY, NUM_DAY+1)
    labels = ["cont_without_s ", "contaminated", "dead", "cured"]
    pal = ["#f1c40f", "#e67e22", "#e74c3c", "#27ae60"]

    fig, ax = plt.subplots()
    ax.stackplot(x, stats["cont_without_s"], stats["contaminated"], stats["dead"], stats["cured"],
                 colors=pal, alpha=0.8, labels=labels)
    ax.legend(loc='upper left')
    plt.hlines(NUM_PERSON, 0, NUM_DAY)
    plt.show()
