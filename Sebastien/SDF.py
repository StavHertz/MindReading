def SDF(array, sigma):
    """
    This function accepts a trial by time array of 0s and 1s and returns the spike density function of each trial. 
    It performs a gaussian convolution on each row of the array. Time bins should have milisecond resolution.
    The sigma input specifies the sigma of the gaussian used for convultion (in miliseconds).
    The convolution will produce edge effects. Select a larger than needed time window and cut manually.
    
    @author: SeB
    """
    
    #from __future__ import division #makes sure all divisions are not rounded to nearest integers
    import numpy as np
    import scipy as sp
    import time
    
    start = time.time() # tic Measures function running speed. Works only on Macs
    
    trials = array.shape[0]
    bins = array.shape[1]
    
    # Create fake data for testing purposes
#    array = np.random.randint(0,2,(trials,bins))
#    sigma = 45
    
    #Define kernel
    sigma = sigma/1000. #Define width of kernel (in sec)
    edges = np.arange(-3*sigma,3*sigma+.001,.001)
    kernel = sp.stats.norm.pdf(edges,0, sigma) #Use a gaussian function
    kernel = kernel*.001 #Time 1/1000 so the total area under the gaussian is 1
    
    #Compute Spike Density Function for all trials
    Sdf = np.zeros((trials,bins))
    Sdf = sp.signal.convolve(array, kernel[None, :] * 1000, mode='same') 
       
    print 'Run time for SDF function was ' + str(round(time.time()-start)) + 'seconds' # toc
     
    return Sdf

    """ End of function """