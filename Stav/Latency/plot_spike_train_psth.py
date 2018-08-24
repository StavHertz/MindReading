# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:41:41 2018

@author: Stav
"""

import matplotlib.pyplot as plt

def plot_spike_train_psth(spike_train, fig_path):
    fig,ax = plt.subplots(1,1,figsize=(6,3))
    spike_times = []
    for row in spike_train:
        spike_times.extend(list(row))
    plt.hist(spike_times, bins=[x * 0.005 for x in range(0, 51)])
    
    fig.savefig(fig_path)