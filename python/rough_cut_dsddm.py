
# code for "Simulation Research on Data Stream Driven Decision Making in Dynamic Environments"
# code by Joseph W. Clark, University of Nebraska at Omaha, 2013
# joeclark77@hotmail.com

# this file contains the rough-cut data-stream-driven-decision-making functionality with the following features:
# 1. holds the data from past experience that the organization will use
# 2. does some kind of analysis to classify the individuals in the current turn
# 3. makes the decisions and returns the selected individuals


import random
        
class BasicDSDDM:
    # a very simple DSDDM model
    def __init__(self,n,p,m,q,training_data):
        # here we could initialize some strategy variable if needed
        self._database = []
        self._database.append(training_data)  # the elements of _database are lists of Individuals corresponding to distinct time periods; element zero is the pre-simulation training data. thus the indexes are out of line with the simulation ticks... the data from time period "t" is stored in _database[t+1]
        # now, build the initial model...
    def update_model(self,newdata):
        # newdata is the set of Individuals who were "chosen" this round, with the outcomes that resulted.
        # now, add them to "history" and update our models
        self._database.append(newdata)
        # update the model...
    def decide(self,new_individuals):
        # given the individuals who arrive, and using the existing model, "choose" some of them and
        # return only the ones that are chosen, i.e., classified as "good"
        # for now, we'll just pick half of them randomly
        return( random.sample( new_individuals, int(len(new_individuals)/2) ) )
        
        
        
        
        
# the following is test code; it will only run if this module is launched directly 
# and not when it is imported by another script
if __name__ == "__main__":
    import rough_cut_environment
    bd = BasicDSDDM()
    be = rough_cut_environment.BasicEnvironment(2,(0.5,0.5),3)
    bd.update_model( be.generate_individuals(10) )
    print(bd.decide())
