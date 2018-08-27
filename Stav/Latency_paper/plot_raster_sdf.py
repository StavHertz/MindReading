import numpy as np
import matplotlib.pyplot as plt
from get_color_list import get_color_list

def plot_raster_sdf(unit_key, spike_times, probe_spikes_images, mean_sdf, sdf_latency, response_type, fig_path):
    fig,ax = plt.subplots(1,1,figsize=(12,6))
    color_list = get_color_list()

    max_sdf_val = mean_sdf.max()*1.1
    ax.set_ylim([0, max_sdf_val])
    num_of_trains = len(spike_times)
    y_spike_locations = [(max_sdf_val/float(num_of_trains))*x for x in range(num_of_trains)]

    sort_and_color = False
    if sort_and_color:
        probe_spikes_images_arr = np.array(probe_spikes_images)
        inds = probe_spikes_images_arr.argsort()
        sorted_spikes_images = probe_spikes_images_arr[inds]
        sorted_spike_times = [spike_times[i] for i in inds]

        for r_ind, row in enumerate(sorted_spike_times):
            ax.axhline(y=y_spike_locations[r_ind], color=color_list[sorted_spikes_images[r_ind]],alpha=0.01)
            ax.scatter(row, y_spike_locations[r_ind]*np.ones_like(row), color='blue', s=1)
    else:
        for r_ind, row in enumerate(spike_times):
            ax.scatter(row, y_spike_locations[r_ind]*np.ones_like(row), color='blue', s=1)

    start_window_in_ms = float(-100)
    end_window_in_ms = float(250)
    ms_f = float(1000)

    x_axis_values = [float(x)/ms_f for x in range(int(start_window_in_ms), int(end_window_in_ms))]

    ax.plot(x_axis_values, mean_sdf, color='black')
    
    if not np.isnan(sdf_latency):
        if response_type > 0:
            ax.axvline(x=float(sdf_latency)/ms_f, color='blue',alpha=0.9)
        else:
            ax.axvline(x=float(sdf_latency)/ms_f, color='orange',alpha=0.9)

    ax.axvline(x=0, color='red', alpha=0.9)
    # ax.axvspan(start_window_in_ms/ms_f,0,color='gray',alpha=0.8)
    ax.set_xlim([start_window_in_ms/ms_f, end_window_in_ms/ms_f])

    ax.set_title('Unit ' + str(unit_key) + ' - latency: ' + str(sdf_latency))
    fig.savefig(fig_path)
