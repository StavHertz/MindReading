import numpy as np
import scipy.stats
import scipy.signal

def get_sdf_from_spike_train(spike_train, sigma):
    trials = spike_train.shape[0]
    bins = spike_train.shape[1]
    
    #Define kernel
    sigma = sigma/1000. #Define width of kernel (in sec)
    edges = np.arange(-3*sigma,3*sigma+.001,.001)
    kernel = scipy.stats.norm.pdf(edges,0, sigma) #Use a gaussian function
    kernel = kernel*.001 #Time 1/1000 so the total area under the gaussian is 1
    
    #Compute Spike Density Function for all trials
    Sdf = np.zeros((trials,bins))
    Sdf = scipy.signal.convolve(spike_train, kernel[None, :] * 1000, mode='same') 
       
    return Sdf