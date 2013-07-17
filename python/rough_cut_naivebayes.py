
# code for "Simulation Research on Data Stream Driven Decision Making in Dynamic Environments"
# code by Joseph W. Clark, University of Nebraska at Omaha, 2013
# joeclark77@hotmail.com

# this file is a crude implementation of a naive bayes classifier
# that simply uses a single time period's data as the training set

# based on a description of the NB algorithm by Krishnamurthy Viswanathan found at
# http://ebiquity.umbc.edu/blogger/2010/12/07/naive-bayes-classifier-in-50-lines/




class crudeNaiveBayes:
    def __init__(self,n,m,trainingdata):
        # n is the number of classes starting with #1, eg n=2 means the classes are #1 and #2
        self._n = n
        # m is the number of X variables on which to build the model
        self._m = m
        # trainingdata is a set of Individuals (see rough_cut_environment.py)
        # initialize variables to count instances of each class and observations of each X for each class
        classcounts = [0 for C in range(n)]
        Xcounts = [[0 for X in range(m)] for C in range(n)]
        # train the model
        for i in trainingdata:
            classcounts[int(i.C)-1] += 1  # it's C-1 because python indexes from zero but C are numbered from 1
            for x in range(m):
                if i.X[x]: Xcounts[int(i.C)-1][x] += 1
        # smoothing stage: add one to each Xcount so there are no zero counts
        Xcounts = [[ Xcounts[C][X]+1 for X in range(m) ] for C in range(n)]
        # conditional probabilities
        self._conditional_probs = [[ Xcounts[C][X]/(classcounts[C]+2) for X in range(m) ] for C in range(n)]
        # the +2 in the denominator is part of the smoothing method and I'm not sure it's the right way to do it. it seems to ensure that there are neither 0s nor 1s for conditional probability
        
    def classify(self,instance):
        # takes an Invidual and classifies it based on its X variables and the conditional probabilities estimated from the training data
        relative_probs = [1 for C in range(self._n)]
        for C in range(self._n):
            for x in range(self._m):
                if instance.X[x]: relative_probs[C] *= self._conditional_probs[C][x]
                else: relative_probs[C] *= (1-self._conditional_probs[C][x])
        classification = relative_probs.index(max(relative_probs)) + 1  # +1 because python indexes from zero but class labels start from 1
        return(classification)









        
        
        
        
        
# the following is test code; it will only run if this module is launched directly 
# and not when it is imported by another script
if __name__ == "__main__":
    from rough_cut_environment import *
    be = BasicEnvironment(2,(0.5,0.5),5,10,0.02)
    data = be.generate_individuals(10)
    for d in data: print(d)
    nb = crudeNaiveBayes(2,5,data)
    newdata = be.generate_individuals(1)[0]
    print(newdata)
    nb.classify( newdata )