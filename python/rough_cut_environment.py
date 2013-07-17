
# code for "Simulation Research on Data Stream Driven Decision Making in Dynamic Environments"
# code by Joseph W. Clark, University of Nebraska at Omaha, 2013
# joeclark77@hotmail.com

# this file contains the rough-cut "Environment" object with the following features:
# 1. takes initialization parameters for the # of classes (n), # of x variables (m), and relative proportions of the population for each class (p, a list)
# 2. stores, for each class, a reward distribution R and m x-variable distributions M
# 3. implements some form of environmental change
# 4. can generate an individual or a list of individuals


import random

def weighted_choice(weights):
    "cribbed from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/"
    totals = []
    running_total = 0
    for w in weights:
        running_total += w
        totals.append(running_total)
    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i

            
            
           
class CClass:
    # one of the n classes/type of customers or agents in the environment
    def __init__(self,C,R,m):
        self._m = m # the number of X variables
        self._C = C  # the class knows its number/name
        self._R = R  # reward "distribution" -- in this case a reward fixed at initialization
        self._M = [ random.betavariate(2,2) for i in range(m) ]  # x variable distributions -- in this case randomly generated probabilities of a 1 or 0 value (aka Bernoulli distribution)
        #print( "CClass initialized with reward (", self._R, ") and x-variable distributions M1-Mn", self._M )
    def get_individual(self):
        # generate a random individual of this class
        xvars = [ 1 if random.random()<M else 0 for M in self._M ]
        return( Individual(self._C,self._R,xvars) )
    def concept_drift(self):
        # implement the effects of concept drift on this class
        # (only if the BasicEnvironment concept_drift method has determined that this should occur)
        for i in range(self._m):
            # each Bernoulli probability is redrawn from the initial Beta distribution with 50% probability
            if random.random() < 0.5: self._M[i] = random.betavariate(2,2)


        
class Individual:
    # one of the customers or agents encountered by the organization
    def __init__(self,C,R,X):
        self.C = C  # class label
        self.R = R
        self.X = X
    def __repr__(self):
        # overrides what the class looks like when it appears in a print() statement
        description = "< indiv of C-" + str(self.C) + " : reward " + str(self.R) + " : X-values " + str(self.X) + " >"
        return(description)

        
        
class BasicEnvironment:
    # the simple environment model described in the 2013 AMCIS paper
    def __init__(self,n,p,m,q,z):
        self._n = n
        self._p = p
        self._m = m
        self._z = z
        # initialize _C as a list of n CClass objects (in this case, two classes, one "good" one "bad")
        self._C = [ CClass("1",1,m), CClass("2",-1,m) ]
        # check for errors
        if len(self._p) != len(self._C): print("ERROR: there are",len(self._C),"CClasses but",len(self._p),"values of p given")
        #print( "Environment initialized with n =",self._n,", p =",self._p,", m =",self._m )   

    def generate_individuals(self,q):
        individuals = []
        for i in range(q):
            # based on population proportions (p), choose a class
            c = weighted_choice(self._p) 
            # return class number, reward, and x variables
            individuals.append( self._C[c].get_individual() )
        return(individuals)         

    def concept_drift(self):
        # implement the effects of concept drift on the environment
        # (calling the concept_drift() method of CClasses as needed)
        # print("concept drifting...")
        if random.random() < self._z:
            for c in self._C: c.concept_drift()
        
        
        
        
        
# the following is test code; it will only run if this module is launched directly 
# and not when it is imported by another script
if __name__ == "__main__":
    be = BasicEnvironment(2,(0.5,0.5),5,10,0.02)
    #data = be.generate_individuals(10)
    #print(data)
    for C in be._C: print(C._M)
    be.concept_drift()

