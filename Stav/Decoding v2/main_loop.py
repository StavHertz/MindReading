import sys
sys.path.append('../Latency_paper/')
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
from plot_all_mean_sdfs import plot_all_mean_sdfs
from get_resource_path import get_resource_path
from create_train_test_data import create_train_test_data
from get_all_regions import get_all_regions

resource_path = get_resource_path()
if not os.path.exists(resource_path):
    os.makedirs(resource_path)

manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
expt_info_df = pd.read_csv(manifest_file)
multi_probe_experiments = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

if get_run_on_server():
    run_short_version = False
else:
    run_short_version = True

# for multi_probe_id in range(len(multi_probe_experiments)):
multi_probe_id = 1
if True:
    print('Analyzing experiment number: ' + str(multi_probe_id))
    
    data_set, multi_probe_filename = load_exp_file(multi_probe_experiments, multi_probe_id, drive_path)

    print(multi_probe_filename)

    import numpy as np
    from sklearn import model_selection
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn import neighbors
    import matplotlib.pyplot as plt
    from scipy.stats import sem

    all_regions = get_all_regions()

    stim_types1 =  ['natural_scenes', 'natural_scenes', 'natural_scenes', 'natural_scenes', 'drifting_gratings']
    stim_types2 =  ['flash_250ms', 'natural_scenes', 'natural_scenes', 'drifting_gratings', 'drifting_gratings']
    stim_frames1 = [1., 1., 3., 4., 0.]
    stim_frames2 = [1, 2., 3., 0., 90.]
    stim_names = ['Natural vs. Flash', 'Natural vs. Natural', 'Sanity check', 'Natural vs. Drifting', 'Drifting vs. Drifting']

    fig, ax = plt.subplots(1,1,figsize=(12,6))
    for stim_ind in range(len(stim_types1)):
        print(stim_names[stim_ind] + ':')
        all_test_rates = []
        all_test_sems = []
        st1 = stim_types1[stim_ind]
        st2 = stim_types2[stim_ind]
        sf1 = stim_frames1[stim_ind]
        sf2 = stim_frames2[stim_ind]

        for region in all_regions:
            X1, num_of_probes = create_train_test_data(data_set, st1, region, sf1)
            X2, _ = create_train_test_data(data_set, st2, region, sf2)

            min_size = np.array([X1.shape[0], X2.shape[0]]).min()
            X1 = X1[:min_size, :]
            X2 = X2[:min_size, :]

            y1 = np.zeros(X1.shape[0])
            y2 = np.ones(X2.shape[0])

            X = np.concatenate((X1, X2))
            y = np.concatenate((y1, y2))


            classifier = LDA()

            cross_validate = True
            if cross_validate:
                scores = model_selection.cross_validate(classifier,X,y, return_train_score=True)
                print(region + ' (' + str(num_of_probes) + ') - Train score: ' + "{0:.2f}".format(np.mean(scores['train_score'])) + ', Test score: ' + "{0:.2f}".format(np.mean(scores['test_score'])))
                all_test_rates.append(np.mean(scores['test_score']))
                all_test_sems.append(sem(scores['test_score']))
                # print(scores['test_score'])
                # print(np.mean(scores['train_score']), np.mean(scores['test_score']))
            else:
                [X_train,X_test,y_train,y_test] = model_selection.train_test_split(X,y,test_size=0.2)
                print(X_train.shape)
                print(y_train)

                classifier.fit(X_train,y_train)
                y_hat = classifier.predict(X_test)
                success_rate = np.sum(y_test == y_hat)/float(y_test.shape[0])
                print(success_rate)

        # p = ax.plot(all_test_rates, marker='o')
        ax.errorbar(x=range(len(all_test_sems)), y=all_test_rates, yerr=all_test_sems, marker='o')

    ax.set_xticks(range(len(all_regions)))
    ax.set_xticklabels(all_regions)
    ax.set_xlabel('Region')
    ax.set_ylabel('Classification rate (%)')
    ax.legend(stim_names, loc='lower right')
    plt.show()

