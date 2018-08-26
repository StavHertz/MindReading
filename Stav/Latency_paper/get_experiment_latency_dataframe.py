import numpy as np
import pandas as pd
from get_spike_train_values_from_key import get_spike_train_values_from_key
from get_mean_sdf_from_spike_train import get_mean_sdf_from_spike_train
from get_latency_from_sdf import get_latency_from_sdf
from get_latency_dataframe import get_latency_dataframe

def get_experiment_latency_dataframe(data_set, multi_probe_filename, short_version=False):
    latency_dataframe = get_latency_dataframe()

    pre_stimulus_time = 0.1
    probe_spikes = {}
    for c_probe in np.unique(data_set.unit_df['probe']):
        probe_units = data_set.unit_df[data_set.unit_df['probe'] == c_probe]
        c_spikes = data_set.spike_times[c_probe]
        for unit_id, unit in probe_units.iterrows():
            unit_spike_train = c_spikes[unit['unit_id']]
            for ind, stim_row in data_set.stim_tables['natural_scenes'].iterrows():
                stimulus_train = unit_spike_train[(unit_spike_train > stim_row['start'] - pre_stimulus_time) & (unit_spike_train < stim_row['end'])] - stim_row['start']
                inner_char_sep = '__'
                train_id = multi_probe_filename + inner_char_sep + c_probe + inner_char_sep + \
                unit['structure'] + inner_char_sep + unit['unit_id'] + inner_char_sep + str(unit['depth'])
                if not probe_spikes.has_key(train_id):
                    probe_spikes[train_id] = []
                probe_spikes[train_id].append(stimulus_train)
        if short_version:
            break

    for st_ind, spike_train_name in enumerate(probe_spikes.keys()):
        st_vals = get_spike_train_values_from_key(spike_train_name)
        # st_hist = get_hist_from_spike_train(st_vals)
        # hist_latency = get_latency_from_hist(st_hist)
        mean_sdf = get_mean_sdf_from_spike_train(probe_spikes[spike_train_name])
        sdf_latency = get_latency_from_sdf(mean_sdf)
        st_vals['latency_psth'] = 0
        st_vals['latency_sdf'] = sdf_latency
        latency_dataframe.loc[st_ind] = st_vals

    return latency_dataframe
