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
from get_resource_path import get_resource_path
from create_train_test_data import create_train_test_data
from get_all_regions import get_all_regions
from get_all_frames import get_all_frames

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
multi_probe_id = 3
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

    stim_names = ['Natural vs. Natural', 'Drifting vs. Drifting', 'Static vs. Static']
    stim_types1 = ['natural_scenes', 'drifting_gratings', 'static_gratings']
    stim_types2 = ['natural_scenes', 'drifting_gratings', 'static_gratings']

    all_region_labels = []

    if not get_run_on_server():
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,1,figsize=(12,6))

    test_rates_over_regions = []
    test_sems_over_regions = []
    for stim_ind in range(len(stim_types1)):
        print(stim_names[stim_ind] + ':')
        all_test_rates = []
        all_test_sems = []
        st1 = stim_types1[stim_ind]
        st2 = stim_types2[stim_ind]

        s_frames1 = get_all_frames(st1)
        s_frames2 = get_all_frames(st2)
        print('Comparing ' + str(len(s_frames1)) + ' with ' + str(len(s_frames2)))

        for region in all_regions:
            all_pair_test_rates = []
            for sf1_ind in range(len(s_frames1)):
                for sf2_ind in range(sf1_ind+1, len(s_frames2)):
                    sf1 = s_frames1[sf1_ind]                    
                    sf2 = s_frames2[sf2_ind]
                    X1, num_of_probes = create_train_test_data(data_set, st1, region, sf1)
                    X2, _ = create_train_test_data(data_set, st2, region, sf2)

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

                    sanity_check = False
                    if sanity_check:
                        np.random.shuffle(y)

                    classifier = LDA()
                    # classifier = KNeighborsClassifier(n_neighbors=5)
                    try:
                        scores = model_selection.cross_validate(classifier,X,y, return_train_score=True)
                        print(region + ' (' + str(num_of_probes) + ') - Train score: ' + "{0:.2f}".format(np.mean(scores['train_score'])) + ', Test score: ' + "{0:.2f}".format(np.mean(scores['test_score'])))
                        all_pair_test_rates.append(np.mean(scores['test_score']))
                    except:
                        print('Error in ' + region + ' stims: ' + str(sf1) + ', ', str(sf2))
                    # all_test_sems.append(sem(scores['test_score']))
            all_test_rates.append(np.mean(all_pair_test_rates))
            all_test_sems.append(sem(all_pair_test_rates))
            if stim_ind == 0:
                all_region_labels.append(region + ' (' + str(X1.shape[1]) + ')')

        if not get_run_on_server():
            print(all_test_sems)
            print(all_test_rates)
            ax.errorbar(x=range(len(all_test_sems)), y=all_test_rates, yerr=all_test_sems, marker='o')
        else:
            test_rates_over_regions.append(all_test_rates)
            test_sems_over_regions.append(all_test_sems)

    if not get_run_on_server():
        ax.set_xticks(range(len(all_region_labels)))
        ax.set_xticklabels(all_region_labels)
        ax.set_xlabel('Region')
        ax.set_ylabel('Classification rate (%)')
        ax.legend(stim_names, loc='lower right')
        plt.show()
    else:
        import pickle
        resource_path = get_resource_path()
        if not os.path.exists(resource_path):
            os.makedirs(resource_path)

        with open(resource_path + multi_probe_filename + '_decoding_table.pkl', 'w') as f:
            pickle.dump([test_rates_over_regions, test_sems_over_regions, all_region_labels], f)