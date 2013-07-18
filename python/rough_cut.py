

# code for "Simulation Research on Data Stream Driven Decision Making in Dynamic Environments"
# code by Joseph W. Clark, University of Nebraska at Omaha, 2013
# joeclark77@hotmail.com


# TECHNICAL PARAMETERS
sims = 1000
turns = 200

# SIMULATION MODEL PARAMETERS
n = 2  # classes of individuals
p = (0.5,0.5)  # population proportions corresponding to classes of individuals
m = 5  # number of X variables for building classification models
q = 100  # number of new individuals that "arrive" each time period
z = 0.02  # probability of abrupt concept drift in any given time period

# DEPENDENCIES
from rough_cut_environment import *
from rough_cut_dsddm import *
import time

# EXPERIMENT DATA STRUCTURES
sim_turn_score = [[0 for t in range(turns)] for s in range(sims)]  # the score per turn, per simulation

experiment_start_time = time.clock() # for timing the program
print("beginning experiment")
# SIMULATION LOOP
# for each simulation
for s in range(sims):
    simulation_start_time = time.clock()
#   INITIALIZATION

    score = 0
    environment = BasicEnvironment(n,p,m,q,z)
    training_data = environment.generate_individuals(q)
    decisionmodel = BasicDSDDM(n,p,m,q,training_data)

#   for each turn
    for t in range(turns):
        turnscore = 0
#       concept drift
        environment.concept_drift()
#       generate individuals
#       pass individuals to DSDDM model, make decisions, and update model with the results
        chosen = decisionmodel.decide( environment.generate_individuals(q) )
        decisionmodel.update_model( chosen )
#       accumulate positive and negative rewards into the running score
        for indiv in chosen:
            turnscore += indiv.R
#       save turn data
        sim_turn_score[s][t] = turnscore
        score += turnscore
#       end of turn

#   save simulation data
#   end of simulation
    print("simulation",s+1,"of",sims,"completed in",round(time.clock()-simulation_start_time,2),"seconds")

# save/output experiment data
print("saving data...")
import csv
with open("rough_cut_output.csv","w",newline="") as csvfile:
    outfile = csv.writer(csvfile)
    outfile.writerows(sim_turn_score)

# end of experiment
print("experiment completed in",round(time.clock()-experiment_start_time,2),"seconds")

