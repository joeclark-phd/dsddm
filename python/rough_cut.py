

# code for "Simulation Research on Data Stream Driven Decision Making in Dynamic Environments"
# code by Joseph W. Clark, University of Nebraska at Omaha, 2013
# joeclark77@hotmail.com


# TECHNICAL PARAMETERS
sims = 5
turns = 10

# SIMULATION MODEL PARAMETERS
n = 2  # classes of individuals
p = (0.5,0.5)  # population proportions corresponding to classes of individuals
m = 5  # number of X variables for building classification models
q = 100  # number of new individuals that "arrive" each time period


# DEPENDENCIES
from rough_cut_environment import *
from rough_cut_dsddm import *


print("beginning experiment")
# SIMULATION LOOP
# for each simulation
for s in range(sims):

#   INITIALIZATION

    score = 0
    environment = BasicEnvironment(n,p,m,q)
    training_data = environment.generate_individuals(q)
    decisionmodel = BasicDSDDM(n,p,m,q,training_data)

#   for each turn
    for t in range(turns):
#       concept drift
        environment.concept_drift()
#       generate individuals
#       pass individuals to DSDDM model, make decisions, and update model with the results
        chosen = decisionmodel.decide( environment.generate_individuals(q) )
        decisionmodel.update_model( chosen )
#       accumulate positive and negative rewards into the running score
        for indiv in chosen:
            score += indiv.R
#       save turn data
#       end of turn

#   save simulation data
    print("total score from simulation #",s,":",score)
#   end of simulation

# save/output experiment data
# end of experiment
print("experiment completed")