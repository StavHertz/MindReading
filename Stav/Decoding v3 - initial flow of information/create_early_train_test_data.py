import numpy as np
import pandas as pd
from get_frames_name import get_frames_name

def create_early_train_test_data(data_set, stim_type, c_region, frame, pre_stimulus_time, stimulus_length):
    natural_scenes = data_set.stim_tables[stim_type]
    scene1 = natural_scenes[natural_scenes[get_frames_name(stim_type)] == frame]
    region_units = data_set.unit_df[(data_set.unit_df['structure'] == c_region)]
    num_of_probes = np.unique(region_units.probe.values).shape[0]
    num_of_trials = len(scene1)
    num_of_units = len(region_units)
    X = np.zeros((num_of_trials, num_of_units))
    row_i = 0
    for ind, stim_row in scene1.iterrows():
        col_i = 0
        for unit_r, unit in region_units.iterrows():
            c_probe = unit['probe']
            c_spikes = data_set.spike_times[c_probe]
            unit_spikes = c_spikes[unit['unit_id']]
            stimulus_train = unit_spikes[(unit_spikes > stim_row['start'] + pre_stimulus_time) & (unit_spikes < stim_row['start'] + pre_stimulus_time + stimulus_length)]
            X[row_i, col_i] = len(stimulus_train)
            col_i += 1
        row_i += 1

    if False:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,1,figsize=(12,6))
        # ax.imshow(X)
        ax.set_xlabel('Units', fontsize=22)
        ax.tick_params(axis='both', which='major', labelsize=16)
        ax.set_ylabel('Trials', fontsize=22)
        ax.set_title('Firing rate of units across trials', fontsize=24)
        plt.show()

        # # ax.imshow(X)
        # ax.imshow(np.expand_dims(X[0, :], axis=0))
        # ax.set_xlabel('Units', fontsize=22)
        # ax.set_yticks([])
        # ax.tick_params(axis='both', which='major', labelsize=16)
        # # ax.set_ylabel('Trials', fontsize=22)
        # # ax.set_title('Firing rate of units', fontsize=24)


    return X, num_of_probes