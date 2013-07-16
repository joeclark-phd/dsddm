# Simulation for "A Study of Endogenous Biases in Data Stream Driven 
# Decision Making Under Concept Drift".
#
# Code by Joseph W Clark: joeclark77@hotmail.com

cat("====================================[ program starting up ]\n") 
rm(list=ls()) # clear the workspace
starttime <- Sys.time() # the time the script started
graphics.off() # close graphics from previous runs
set.seed(12345) # set a random number seed for reproducability... could also specify RNG type to make this really sophisticated



#PARAMETERS
sims <- 10L  
turns <- 500L
m <- 5 # number of observable X variables
q <- 20 # number of individuals/cases that arrive each time period
fraction_bad <- 0.5 # fraction of cases in class C2
z <- 0.05 # probability of abrupt drift in any given time period



#DATA STRUCTURES
simturnperf <- array(0L, dim=c(sims,turns)) # performance per turn per sim
simturnfp <- array(0L, dim=c(sims,turns)) # false positives per turn per sim
simturnfn <- array(0L, dim=c(sims,turns)) # false negatives per turn per sim




#EACH SIMULATION
for(s in 1:sims) {
  cat("====================================[ simulation",s,"]\n"); simstart_time <- Sys.time()
  #DATA STRUCTURES
  turnperf <- rep(0L, turns) # performance per turn
  turnfp <- rep(0L,turns) # false positives per turn
  turnfn <- rep(0L,turns) # false negatives per turn
  driftturns <- c() # record turn numbers where drift occurred
  
  #INITIALIZATION
  M <- array( rbeta(2*m,2,2) , dim=c(2,m) )
  # generate fake history data
    h = 5*q #number of historical cases to generate
    cl = ( runif(h) < fraction_bad ) + 1L # individuals are of class 1 or 2
    rw = (-1)^(cl-1) # the payouts on the individuals, if selected
    X <- array( 0, dim=c(h,m) )
    for(i in 1:h) {
      X[i,] <- runif(m) < M[cl[i],]
    }
    t <- rep(0,h)
    history = data.frame(t,cl,rw,X)
  
  #EACH TURN
  for(t in 1:turns) {

    # apply concept drift (turbulence) and record the environment data (M)
    if (t>1) { #do nothing in turn 1
      if( runif(1)<z ) { # here we model sudden/abrupt drift: affects many environment variables (M) simultaneously but only occasionally
        driftturns <- c(driftturns,t)
        drifters <- (runif(2*m)<0.5) # approximately half of M will be redrawn (by indpendent coin flip)
        M[drifters] <- rbeta(sum(drifters),2,2) # new draws from same distribution as before (no munificence change)
      }
    }
    
    # generate q new individuals/cases, each manifesting m observable X variables
    cl = ( runif(q) < fraction_bad ) + 1L # individuals are of class 1 or 2
    rw = (-1)^(cl-1) # the payouts on the individuals, if selected
    X <- array( 0, dim=c(q,m) )
    for(i in 1:q) {
      X[i,] <- runif(m) < M[cl[i],]
    }
    
    # using present and past data, build a model to predict which cases have a positive expected value (algorithm A).
    # columns in the dataset: t (time period), cl, rw, X1, X2, ... Xm
    # the variables cl, rw, are only available for those options that were selected.
    model <- glm(rw ~ X1 + X2 + X3 + X4 + X5, data=history)
    expectations <- predict(model,data.frame(X)) # a super simple data mining model - a regression that predicts the payout 'rw'
    
    # decide which cases to select, and record the outcomes
    for(i in 1:q) {
      if(expectations[i]>0) { # the simplest possible decision rule: if expected value is positive, select the case, otherwise ignore
        history <- rbind(history,c(t,cl[i],rw[i],X[i,]))
        if(cl[i]==2) turnfp[t] <- turnfp[t]+1 # note if this is a false positive
        turnperf[t] = turnperf[t] + rw[i]
      }
      else if(cl[i]==1) turnfn[t] <- turnfn[t]+1 # note if this is a false positive
    }
    
    
  } #next turn

  simturnperf[s,] <- turnperf 
  simturnfp[s,] <- turnfp
  simturnfn[s,] <- turnfn
  
  simtime <- Sys.time() - simstart_time; cat("====================================[ sim",s,"finished in",simtime,units(simtime),"]\n") 
} #next sim






# end program
run_time <- (Sys.time()-starttime); cat("====================================[ program finished in",run_time,units(run_time),"]\n") 

#output results of one simulation
#cat( "Total score: ", sum(history[history$t>0,]$rw), "\n")
#plot(1:turns,turnperf,ylim=c(-20,20))

#output mean/ci of multiple simulations
library(plotrix)
plotCI(1:turns,apply(simturnperf,2,mean),(qnorm(.975)*apply(simturnperf,2,sd))/sqrt(sims),sfrac=0,pch=NA,scol="darkgray",xlab="Time",ylab="Performance (95% confidence)",main="Performance Degrades over Time")
abline(h=0,col="red")
