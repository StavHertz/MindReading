# -*- coding: utf-8 -*-
"""
Testing out a new latency algorithm

See: https://github.com/NeuRowsATL/burst-detection
minsky

pdp books - boltzmann machine paper

santa fe - ertz - neural network theory 

Created on Mon Aug 27 20:42:25 2018

@author: sarap
"""
import math
import numpy as np
import scipy.optimize


runfile('D:/resources/mindreading_repo/mindreading/Sara/GetToWork.py', wdir='D:/resources/mindreading_repo/mindreading/Sara')

# Set your own dataset, no more of that code

# Get the spontaneous stimulus conditions
ns_table = data_set.stim_tables['spontaneous']


resp, centers = get_psth(ns_table, spike_train)
fig, ax = plt.subplots()
plt.plot(centers, resp[0])

# POISSON FIT
fitfunc = lambda p, x: p[0]*p[1]**x*np.exp**-p[1]/factorial(x) # Target function
errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
p0 = [1., 2.] # Initial guess for the parameters
p1, success = scipy.optimize.leastsq(errfunc, p0[:], args=(bins_mean, n))

probe_spikes = data_set.spike_times['probeC']
stim_train = []
pre_time = 0
spike_train = probe_spikes['1']
for j, stim_row in frame_table.iterrows():
            current_train = spike_train[(spike_train > stim_row['start'] - pre_time) & (spike_train <= stim_row['end'])] - stim_row['start']
            stim_train.append(current_train)

# Fit ISIs to Poisson
isi = get_isi(stim_train[0])
counts, bin_edges = np.histogram(isi, bins=20)
plt.plot(bin_edges[:-1], counts)
from scipy.stats import poisson


# Check out latency code
df = do_poisson(stim_train[1])

fig, ax = plt.subplots()
ax.plot(stim_train[1], np.ones_like(stim_train[1]), '|', color='b')
for b, burst_ind in enumerate(df['bursts']):
    ax.plot(burst_ind, np.ones_like(burst_ind), color='r')
