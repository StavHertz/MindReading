import matplotlib.pyplot as plt
import numpy as np

def plot_meam_sdfs(st_vals, mean_sdf, mean_sdf2, st1, st2):
    fig,ax = plt.subplots(1,1,figsize=(12,6))
    start_window_in_ms = float(-100)
    end_window_in_ms = float(250)
    ms_f = float(1000)

    x_axis_values = [float(x)/ms_f for x in range(int(start_window_in_ms), int(end_window_in_ms))]

    ax.plot(x_axis_values, mean_sdf, color='black')
    ax.plot(x_axis_values, mean_sdf2, color='gray')
    ax.axvline(x=0, color='red', alpha=0.9)
    
    max_sdf_val = np.array([mean_sdf.max(), mean_sdf2.max()]).max()
    num_of_trains = len(st1)+len(st2)
    print('Here:')
    print(len(st1))
    print(len(st2))
    print(num_of_trains)
    y_spike_locations = [(max_sdf_val/float(num_of_trains))*x for x in range(num_of_trains)]

    for r_ind, row in enumerate(st1):
        ax.scatter(row, y_spike_locations[r_ind]*np.ones_like(row), color='blue', s=1)

    ax.axhline(y=y_spike_locations[len(st1)], color='black', alpha=0.9)

    for r_ind, row in enumerate(st2):
        ax.scatter(row, (y_spike_locations[r_ind+len(st1)])*np.ones_like(row), color='green', s=1)

    ax.set_xlim([start_window_in_ms/ms_f, end_window_in_ms/ms_f])

    plt.show()