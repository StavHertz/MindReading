import numpy as np
import pandas as pd
from get_prestimulus_time import get_prestimulus_time
from get_time_window_buffer import get_time_window_buffer

def get_spike_trains_from_unit_id(data_set, probe, unit_id):
    stim_spikes = []
    c_spikes = data_set.spike_times[probe]
    unit_spike_train = c_spikes[unit_id]
    pre_stimulus_time = float(get_prestimulus_time())/1000
    time_window_buffer = float(get_time_window_buffer())/1000

    for ind, stim_row in data_set.stim_tables['natural_scenes'].iterrows():
        stimulus_train = unit_spike_train[(unit_spike_train > stim_row['start'] - pre_stimulus_time) & (unit_spike_train < stim_row['end'] + time_window_buffer)] - stim_row['start']
        stim_spikes.append(stimulus_train)

    return stim_spikes