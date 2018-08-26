import numpy as np
from convert_spike_times_to_raster import convert_spike_times_to_raster
from get_sdf_from_spike_train import get_sdf_from_spike_train

def get_mean_sdf_from_spike_train(spike_train):
    spike_raster = convert_spike_times_to_raster(spike_train)
    sdfs = get_sdf_from_spike_train(spike_raster, 45)
    sdfs = np.zeros(spike_raster.shape)
    # for row_ind, single_train in enumerate(spike_raster):
    #     sdf = get_sdf_from_spike_train(single_train, 45)
    #     sdfs[row_ind, :] = sdf
    mean_sdf = sdfs.mean(axis=0)
    return mean_sdf