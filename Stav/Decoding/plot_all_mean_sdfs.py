import numpy as np
import pandas as pd
import datetime
import os
from get_resource_path import get_resource_path
from get_spike_train_values_from_key import get_spike_train_values_from_key
from get_mean_sdf_from_spike_train import get_mean_sdf_from_spike_train
from plot_meam_sdfs import plot_meam_sdfs
from get_time_window_buffer import get_time_window_buffer
from get_prestimulus_time import get_prestimulus_time

def plot_all_mean_sdfs(data_set, multi_probe_filename):
    pre_stimulus_time = float(get_prestimulus_time())/1000
    time_window_buffer = float(get_time_window_buffer())/1000
    selected_region = 'VISp'
    for c_probe in np.unique(data_set.unit_df['probe']):
        probe_units = data_set.unit_df[(data_set.unit_df['probe'] == c_probe) & (data_set.unit_df['structure'] == selected_region)]
        c_spikes = data_set.spike_times[c_probe]
        for unit_id, unit in probe_units.iterrows():
            unit_spike_train = c_spikes[unit['unit_id']]
            first_train_spikes = []
            for ind, stim_row in data_set.stim_tables['natural_scenes'].iterrows():
                stimulus_train = unit_spike_train[(unit_spike_train > stim_row['start'] - pre_stimulus_time) & (unit_spike_train < stim_row['end'] + time_window_buffer)] - stim_row['start']
                inner_char_sep = '__'
                first_train_id = multi_probe_filename + inner_char_sep + c_probe + inner_char_sep + \
                unit['structure'] + inner_char_sep + unit['unit_id'] + inner_char_sep + str(unit['depth'])
                first_train_spikes.append(stimulus_train)

            second_train_spikes = []
            for ind, stim_row in data_set.stim_tables['flash_250ms'].iterrows():
                if(stim_row['color'] == 1):
                    stimulus_train2 = unit_spike_train[(unit_spike_train > stim_row['start'] - pre_stimulus_time) & (unit_spike_train < stim_row['end'] + time_window_buffer)] - stim_row['start']
                    second_train_spikes.append(stimulus_train2)

            output_path = get_resource_path() + 'Decoding_results/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            c_output_path = output_path + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")) + '/'
            if not os.path.exists(c_output_path):
                os.makedirs(c_output_path)

            st_vals = get_spike_train_values_from_key(first_train_id)

            min_size = np.array([len(first_train_spikes), len(second_train_spikes)]).min()

            first_train_spikes = first_train_spikes[:min_size]
            second_train_spikes = second_train_spikes[:min_size]
            mean_sdf, spike_raster, all_sdfs = get_mean_sdf_from_spike_train(first_train_spikes)
            mean_sdf2, spike_raster2, all_sdfs2 = get_mean_sdf_from_spike_train(second_train_spikes)

            plot_meam_sdfs(st_vals, mean_sdf, mean_sdf2, first_train_spikes, second_train_spikes)
            # plot_raster_sdf(spike_train_name, probe_spikes[spike_train_name], probe_spikes_images[spike_train_name], mean_sdf, st_vals, pre_stim_dict, fig_path)
