# Focus on image 1 and 2
# Can the first 50 ms decode?

import sys
from get_run_on_server import get_run_on_server
import os
import pandas as pd
if get_run_on_server():
    basic_path = '/data/dynamic-brain-workshop/'
else:
    basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')

from load_exp_file import load_exp_file
from create_early_train_test_data import create_early_train_test_data
from get_all_regions import get_all_regions
from get_all_frames import get_all_frames
from get_resource_path import get_resource_path
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
expt_info_df = pd.read_csv(manifest_file)
multi_probe_experiments = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

# for multi_probe_id in range(len(multi_probe_experiments)):
# 0 -> 84
# 1 -> 58
# 2 -> 10
# 3 -> 21
sub_sample = False
units_per_exp = [0, 12, 83, 39]
multi_probe_id = 2
if True:
# for multi_probe_id in [1, 2, 3]:
    print('Analyzing experiment number: ' + str(multi_probe_id))
    
    data_set, multi_probe_filename = load_exp_file(multi_probe_experiments, multi_probe_id, drive_path)

    print(multi_probe_filename)

    import numpy as np
    from sklearn import model_selection
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn import neighbors
    from scipy.stats import sem
    from sklearn.neighbors import KNeighborsClassifier

    all_regions = get_all_regions()

    stim_type1 = 'natural_scenes'
    stim_type2 = 'natural_scenes'
    stim_frame1 = 1.
    stim_frame2 = 2.
    pre_stimulus_time = 0.00
    stimulus_length = 0.00
    s_frames1 = get_all_frames(stim_type1)
    s_frames2 = get_all_frames(stim_type2)

    num_of_time_windows = 30
    information_table = np.zeros((len(all_regions), num_of_time_windows))
    sems_table = np.zeros((len(all_regions), num_of_time_windows))
    all_x_axis = []

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(3,2,figsize=(12,6))

    region = 'VISp'

    if True:
        create_early_train_test_data(data_set, stim_type1, region, 2., 0.05, 0.15)
        create_early_train_test_data(data_set, stim_type1, region, 12., 0.05, 0.15)

    pre_stimulus_time = 0.00
    stimulus_length = 0.05
    X1, num_of_probes = create_early_train_test_data(data_set, stim_type1, region, stim_frame1, pre_stimulus_time, stimulus_length)
    X2, _ = create_early_train_test_data(data_set, stim_type2, region, stim_frame2, pre_stimulus_time, stimulus_length)

    # X1 = X1.T
    # X2 = X2.T

    print(X1.shape)
    ax[0, 0].imshow(X1[0:4, :])
    ax[0, 1].imshow(X2[0:4, :])
    ax[0, 0].set_xticks([])
    ax[0, 1].set_xticks([])
    ax[0, 0].set_yticks([])
    ax[0, 1].set_yticks([])

    pre_stimulus_time = 0.1
    stimulus_length = 0.05
    X1b, num_of_probes = create_early_train_test_data(data_set, stim_type1, region, stim_frame1, pre_stimulus_time, stimulus_length)
    X2b, _ = create_early_train_test_data(data_set, stim_type2, region, stim_frame2, pre_stimulus_time, stimulus_length)

    ax[1,0].imshow(X1b)
    ax[1,1].imshow(X2b)

    center = X1.shape[0]/float(2)

    print(X1.shape, X1b.shape, X1.mean(axis=0).shape, X1b.mean(axis=0).shape)
    diff1 = X1b.mean(axis=0)-X1.mean(axis=0)
    ax[1,0].plot(center + 10*diff1, color='black', alpha=0.5)
    diff2 = X2b.mean(axis=0)-X2.mean(axis=0)
    ax[1,1].plot(center + 10*diff2, color='black', alpha=0.5)

    ax[2,0].plot(diff1-diff2)
    ax[2,1].plot(diff1-diff2)
    fig.tight_layout()
    plt.show()

