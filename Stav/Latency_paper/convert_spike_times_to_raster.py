import numpy as np
from get_prestimulus_time import get_prestimulus_time
from get_window_size import get_window_size

def convert_time_to_ind(spike_time):
    ind = int(spike_time*1000 + get_prestimulus_time())
    return ind

def get_spike_train_from_time(spike_times_list):
    spike_train = np.zeros(get_window_size())
    for spike_time in spike_times_list:
        spike_ind = convert_time_to_ind(spike_time)
        if spike_ind < get_window_size():
            spike_train[spike_ind] = 1

    return spike_train

def convert_spike_times_to_raster(spike_times):
    spike_raster = np.zeros((len(spike_times), get_window_size()))
    for ind, spike_times_list in enumerate(spike_times):
        spike_raster[ind, :] = get_spike_train_from_time(spike_times_list)

    return spike_raster
