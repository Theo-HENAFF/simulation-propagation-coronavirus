import simpy
import yaml
import matplotlib.pyplot as plt
import numpy as np
import features

# main of the simulation
if __name__ == "__main__":

    # Load the config file
    with open("configuration.yml", "r") as ymlfile:
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
    TIME_VACCINE_DISCOVER = cfg['config']["TIME_VACCINE_DISCOVER"]
    NUM_VACC_PER_DAY = cfg['config']["NUM_VACC_PER_DAY"]
    VACCINE_EFFECT = cfg['config']["VACCINE_EFFECT"]

    # =================================================================================
    # Simulation
    # =================================================================================
    # Setup the simulation
    features.setup(nber_person=NUM_PERSON, max_neighbours=MAX_NEIGHBOURS)

    # Run the simulation
    for day in range(NUM_DAY):
        # Create an environment and start the setup process
        env = simpy.Environment()

        # Setup and start the simulation
        env.process(features.day(env=env,
                                 area_zone=NUM_AREA,
                                 meetime=TIMEMEET,
                                 nber_person=NUM_PERSON,
                                 proba_conta=proba_conta,
                                 proba_meet=PROBA_MEET,
                                 malus=MALUS))

        # Add temporality to the simulation
        features.gestion(proba_death=PROBA_DEATH,
                         time_contaminated=TIME_CONTAMINATED,
                         proba_heal=PROBA_HEAL,
                         time_without_s=TIME_WITHOUT_S,
                         time_too_much=TIME_TOO_MUCH,
                         proba_death_during_rea=PROBA_DEATH_DURING_REA,
                         time_disco_vac=TIME_VACCINE_DISCOVER,
                         num_vac=NUM_VACC_PER_DAY,
                         effect_vac=VACCINE_EFFECT)
        # Get stats for the visualization
        features.add_stats()

        # Execute
        env.run(until=NUM_PERSON * 800)
        print("END OF DAY {} OUT OF {}".format(day+1, NUM_DAY))
        features.log.write("END OF DAY {} OUT OF {} \n".format(day, NUM_DAY))

    # =================================================================================
    # Visualization
    # =================================================================================

    # Nb_new_cont[1:] = [Nb_new_cont[i]-Nb_new_cont[i-1] for i in range(1, len(Nb_new_cont))]
    # Nb_new_cont = [i if i > 0 else 0 for i in Nb_new_cont]
    # Nb_new_cont.insert(0, 0)

    stats = features.stats
    stats["rate"].insert(0, 0)
    stats["rate"] = [i/NUM_PERSON for i in stats["rate"]]
    Nb_new_cont = stats["cont_without_s"]
    Nb_new_cont[1:] = [Nb_new_cont[i]-Nb_new_cont[i-1] for i in range(1, len(Nb_new_cont))]
    Nb_new_cont = [i if i > 0 else 0 for i in Nb_new_cont]

    x = np.linspace(0, NUM_DAY, NUM_DAY + 1)
    labels = ["cont_without_s ", "contaminated", "dead", "cured", "vaccinated"]
    pal = ["#f1c40f", "#e67e22", "#e74c3c", "#27ae60", "#47e9ff"]

    plt.plot(x, stats["rate"])
    plt.title("Rate of current infected and dead person")
    plt.savefig("Rate_of_current_infected_and_dead_person")

    plt.plot(x, Nb_new_cont)
    plt.title("Number of new infected person per day")
    plt.savefig("Number_of_new_infected_person_per_day")

    fig, ax = plt.subplots()
    ax.stackplot(x, stats["cont_without_s"], stats["contaminated"], stats["dead"], stats["cured"], stats["vaccinated"],
                 colors=pal, alpha=0.8, labels=labels)
    ax.legend(loc='upper left')
    plt.suptitle('Propagation of the virus through time')
    plt.xlabel("Days")
    plt.ylabel('Number of persons')
    plt.hlines(NUM_PERSON, 0, NUM_DAY)
    plt.savefig("Propagation_of_the_virus_through_time")

    # Print stats in the log file
    features.log.write("Total: {} \n".format(NUM_PERSON))
    features.log.write("Contaminated without symptoms: {} \n".format(str(stats["cont_without_s"])))
    features.log.write("Contaminated: {} \n".format(str(stats["contaminated"])))
    features.log.write("Dead: {} \n".format(str(stats["dead"])))
    features.log.write("Vaccinated: {} \n".format(str(stats["vaccinated"])))
    features.log.write("cured: {} \n".format(str(stats["cured"])))

    # End of simulation we close the file
    features.log.close()
