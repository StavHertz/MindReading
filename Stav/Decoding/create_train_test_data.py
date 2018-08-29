import numpy as np
import pandas as pd
from get_frames_name import get_frames_name
import matplotlib.pyplot as plt

def create_train_test_data(data_set, stim_type, c_region, frame):
    pre_stimulus_time = 0.05
    natural_scenes = data_set.stim_tables[stim_type]
    scene1 = natural_scenes[natural_scenes[get_frames_name(stim_type)] == frame]
    probe_units = data_set.unit_df[(data_set.unit_df['structure'] == c_region)]
    c_probe = probe_units.probe.values[0]
    num_of_trials = len(scene1)
    num_of_units = len(probe_units)
    X = np.zeros((num_of_trials, num_of_units))
    probe_spikes = data_set.spike_times[c_probe]
    c_spikes = data_set.spike_times[c_probe]
    row_i = 0
    for ind, stim_row in scene1.iterrows():
        col_i = 0
        for unit_r, unit in probe_units.iterrows():
            unit_spikes = c_spikes[unit['unit_id']]
            stimulus_train = unit_spikes[(unit_spikes > stim_row['start'] + pre_stimulus_time) & (unit_spikes < stim_row['end'] - pre_stimulus_time)]
            X[row_i, col_i] = len(stimulus_train)
            col_i += 1
        row_i += 1

    plt.imshow(X)
    plt.show()
    print X
    return X