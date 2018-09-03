# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 19:46:59 2018

@author: sarap
"""

import os
import sys
import numpy as np
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn import neighbors
import matplotlib.pyplot as plt
from scipy.stats import sem

#%%
sys.path.append(os.path.normpath('d:/resources/mindreading/sara'))
from neuropixel_decoding import create_test_train_running_data

#%%
sys.path.append(os.path.normpath('d:/resources/mindreading/stav/decoding'))
from get_all_frames import get_all_frames

#%%
running_timestamps, running_speed = get_running_speed(data_set)
running_timestamps = running_timestamps.astype(float)
running_speed = running_speed.astype(float)
#%%
all_regions = ['TH', 'SCs', 'DG', 'CA', 'VISl', 'VISp', 'VISrl', 'VISal', 'VISam', 'VISpm']

all_stim_frames = np.array([2., 12., 23., 35., 48., 62., 77., 93.])
s_frames1 = all_stim_frames
s_frames2 = all_stim_frames
# stim_names = ['Natural vs. Flash', 'Natural vs. Natural', 'Sanity check', 'Natural vs. Drifting', 'Drifting vs. Drifting']
# stim_names = ['Drifting vs. Drifting', 'Natural vs. Natural', 'Static vs. Static']
stim_names = ['Natural vs. Drifting']

stim_types1 = ['drifting_gratings']
stim_types2 = stim_types1

run_types = [True, False]
#%%
st1 = 'drifting_gratings'
  # tim_types1[stim_ind]
st2 = st1  # stim_types2[stim_ind]

s_frames1 = get_all_frames(st1)
s_frames2 = get_all_frames(st2)

#%%
fig, ax = plt.subplots(1,1,figsize=(12,6))
run_test_rates = []
run_test_sems = []
for i, run_mode in enumerate(run_types):
    for stim_ind in range(len(stim_types1)):
        print(stim_names[stim_ind] + ':')
        all_test_rates = []
        all_test_sems = []
        st1 = stim_types1[stim_ind]
        st2 = stim_types2[stim_ind]

        s_frames1 = get_all_frames(st1)
        s_frames2 = get_all_frames(st2)
        print('Comparing ' + str(len(s_frames1)) + ' with: ' + str(len(s_frames2)))

        for region in all_regions:
            all_pair_test_rates = []
            for sf1_ind in range(len(s_frames1)):
                for sf2_ind in range(sf1_ind+1, len(s_frames2)):
                    sf1 = s_frames1[sf1_ind]                    
                    sf2 = s_frames2[sf2_ind]
                    X1, num_of_probes = create_test_train_running_data(data_set, st1, region, sf1, run_mode, running_timestamps, running_speed)
                    print('Region {} - {} run'.format(region, X1.shape[0]))
                    X2, _ = create_test_train_running_data(data_set, st2, region, sf2, run_mode, running_timestamps, running_speed)
                    min_size = 50   #  np.array([X1.shape[0], X2.shape[0]]).min()
                    print('Region {}, IM {} using {} trials'.format(region, sf1_ind, X1.shape[0]+X2.shape[0]))
 

                    min_size = np.array([X1.shape[0], X2.shape[0]]).min()
                    X1 = X1[:min_size, :]
                    X2 = X2[:min_size, :]

                    y1 = np.zeros(X1.shape[0])
                    y2 = np.ones(X2.shape[0])

                    X = np.concatenate((X1, X2))
                    y = np.concatenate((y1, y2))

                    classifier = LDA()

                    scores = model_selection.cross_validate(classifier,X,y, return_train_score=True)
                    print(region + ' (' + str(num_of_probes) + ') - Train score: ' + "{0:.2f}".format(np.mean(scores['train_score'])) + ', Test score: ' + "{0:.2f}".format(np.mean(scores['test_score'])))
                    all_pair_test_rates.append(np.mean(scores['test_score']))
                    # all_test_sems.append(sem(scores['test_score']))
            all_test_rates.append(np.mean(all_pair_test_rates))
            all_test_sems.append(sem(all_pair_test_rates))
            print('------ {} = {} pm {} -----'.format(region, np.mean(all_pair_test_rates), sem(all_pair_test_rates)))

        ax.errorbar(x=range(len(all_test_sems)), y=all_test_rates, yerr=all_test_sems, marker='o')
        run_test_rates.append(all_test_rates)
        run_test_sems.append(all_test_sems)

ax.set_xticks(range(len(all_regions)))
ax.set_xticklabels(all_regions)
ax.set_xlabel('Region')
ax.set_ylabel('Classification rate (%)')
ax.legend(stim_names, loc='lower right')
plt.show()