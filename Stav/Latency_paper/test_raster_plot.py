import matplotlib.pyplot as plt
import numpy as np
import pickle

with open('raster_temp.pkl') as f:
    [spike_times, y_spike_locations, x_axis_values, mean_sdf] = pickle.load(f)

fig,ax = plt.subplots(1,1,figsize=(12,6))

print len(spike_times)
for r_ind, row in enumerate(spike_times):
    ax.scatter(row, y_spike_locations[r_ind]*np.ones_like(row), color='blue', s=1)

start_window_in_ms = float(-100)
end_window_in_ms = float(250)
ms_f = float(1000)

x_axis_values = [float(x)/ms_f for x in range(int(start_window_in_ms), int(end_window_in_ms))]

ax.plot(x_axis_values, mean_sdf, color='black')
ax.axvline(x=0, color='red', alpha=0.9)
ax.set_xlim([start_window_in_ms/ms_f, end_window_in_ms/ms_f])
# ax2 = ax.twinx()
# ax2.set_yticks(y_spike_locations)
# ax2.set_yticklabels(str(y_spike_locations))
plt.show()
fig.savefig('raster_temp.png')