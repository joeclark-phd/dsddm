

# code for "Simulation Research on Data Stream Driven Decision Making in Dynamic Environments"
# code by Joseph W. Clark, University of Nebraska at Omaha, 2013
# joeclark77@hotmail.com


# TECHNICAL PARAMETERS
sims = 1
turns = 100

# SIMULATION MODEL PARAMETERS
n = 2  # classes of individuals
m = 5  # number of X variables for building classification models
q = 100  # number of new individuals that "arrive" each time period





# SIMULATION LOOP
# for each simulation
#   initialization

# ENVIRONMENT
# contains: for each "class", an R prob. distribution and M prob distributions
# contains: a function to produce a random individual
# contains: a function/module/parameter for concept drift (D)

# DATA STREAM DRIVEN DECISION MAKING ("KNOWLEDGE" MODEL)
# contains: a database or data storage model of some kind
# contains: an algorithm or method for classification (A)
# may contain: a module/parameter for decision making (S)

#   for each turn
#       concept drift
#       generate individuals
#       pass individuals to DSDDM model
#       make decisions and calculate consequences
#       save turn data
#   save simulation data
# save/output experiment data