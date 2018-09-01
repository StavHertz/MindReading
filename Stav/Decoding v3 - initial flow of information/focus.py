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
# if True:
for multi_probe_id in [1, 2, 3]:
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
    # stim_frame1 = 1.
    # stim_frame2 = 2.
    pre_stimulus_time = 0.00
    stimulus_length = 0.00
    s_frames1 = get_all_frames(stim_type1)
    s_frames2 = get_all_frames(stim_type2)

    num_of_time_windows = 30
    information_table = np.zeros((len(all_regions), num_of_time_windows))
    sems_table = np.zeros((len(all_regions), num_of_time_windows))
    all_x_axis = []
    if not get_run_on_server():
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,1,figsize=(12,6))
    for stimulus_length_val in range(num_of_time_windows):
        stimulus_length = (stimulus_length_val+1)/float(100)
        for region_id, region in enumerate(all_regions):
            all_region_means = []
            for sf1_ind in range(len(s_frames1)):
                for sf2_ind in range(sf1_ind+1, len(s_frames2)):
                    sf1 = s_frames1[sf1_ind]                    
                    sf2 = s_frames2[sf2_ind]

                    X1, num_of_probes = create_early_train_test_data(data_set, stim_type1, region, sf1, pre_stimulus_time, stimulus_length)
                    X2, _ = create_early_train_test_data(data_set, stim_type2, region, sf2, pre_stimulus_time, stimulus_length)

                    np.random.shuffle(X1)
                    np.random.shuffle(X2)

                    col_perm = np.random.permutation(X1.shape[1])
                    X1 = X1[:, col_perm]
                    X2 = X2[:, col_perm]

                    min_size = np.array([X1.shape[0], X2.shape[0]]).min()
                    
                    if sub_sample:
                        column_size = units_per_exp[multi_probe_id]
                        X1 = X1[:min_size, :column_size]
                        X2 = X2[:min_size, :column_size]
                    else:
                        X1 = X1[:min_size, :]
                        X2 = X2[:min_size, :]

                    y1 = np.zeros(X1.shape[0])
                    y2 = np.ones(X2.shape[0])

                    X = np.concatenate((X1, X2))
                    y = np.concatenate((y1, y2))

                    classifier = LDA()
                    try:
                        scores = model_selection.cross_validate(classifier,X,y, return_train_score=True)
                        print(region + ' (' + str(num_of_probes) + ') - Train score: ' + "{0:.2f}".format(np.mean(scores['train_score'])) + ', Test score: ' + "{0:.2f}".format(np.mean(scores['test_score'])))
                        all_region_means.append(np.mean(scores['test_score']))
                    except:
                        print('Error in ' + region + ' stims: ' + str(sf1) + ', ', str(sf2))

            information_table[region_id, stimulus_length_val] = np.mean(all_region_means)
            sems_table[region_id, stimulus_length_val] = sem(all_region_means)
        all_x_axis.append(stimulus_length*1000)
    
    if not get_run_on_server():
        for row in information_table:
            ax.plot(all_x_axis, row, marker='o')
        ax.legend(all_regions)
        ax.set_xlabel('Window size (ms)')
        plt.show()
    else:
        import pickle
        resource_path = get_resource_path()
        if not os.path.exists(resource_path):
            os.makedirs(resource_path)

        with open(resource_path + multi_probe_filename + '_decoding_table.pkl', 'w') as f:
            pickle.dump([information_table, sems_table, all_x_axis, all_regions], f)