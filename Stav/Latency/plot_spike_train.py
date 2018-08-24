# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:37:00 2018

@author: Stav
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_spike_train(spike_trains, fig_path):
    fig,ax = plt.subplots(1,1,figsize=(6,3))
    print(len(spike_trains))
    print(spike_trains[0].shape)
    for r_ind, row in enumerate(spike_trains):
        ax.plot(row, r_ind*np.ones_like(row),'|',color='b')
    ax.invert_yaxis()
    ax.set_xlim([0, 0.25])

    fig.savefig(fig_path)