"""
============
3D animation
============

A simple example of an animated plot... In 3D!
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from scipy.stats import gaussian_kde

def update_dots(num, data, sizes, dots, max_val):
    ax.clear()
    ax.set_xlim3d([0.0, 1.0])
    ax.set_xlabel('X')

    ax.set_ylim3d([0.0, 1.0])
    ax.set_ylabel('Y')

    ax.set_zlim3d([0.0, 1.0])
    ax.set_zlabel('Z')

    ax.set_title('Latency in regions')
    for d_id in range(len(data)):
        size = sizes[d_id]
        c_val = float(size[num])/max_val
        ax.scatter(data[d_id][0], data[d_id][1], data[d_id][2], s=[size[num]*30000]*3, c=[1-c_val, 0, 0])
    return dots

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

data = []
data.append(np.asarray([0.34, 0.2, 0.75]))
data.append(np.asarray([0.6, 0.26, 0.75]))
data.append(np.asarray([0.18, 0.41, 0.75]))
data.append(np.asarray([0.52, 0.5, 0.8]))
data.append(np.asarray([0.82, 0.34, 0.75]))
data.append(np.asarray([0.22, 0.68, 0.75]))
data.append(np.asarray([0.2, 0.6, 0.2]))
data.append(np.asarray([0.5, 0.5, 0.3]))
data.append(np.asarray([0.8, 0.3, 0.2]))

cm = plt.cm.get_cmap('Greens')
dots = [ax.scatter(dat[0], dat[1], dat[2], c=[0.5, 0.0, 0.0]) for dat in data]

# Setting the axes properties
ax.set_xlim3d([0.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('Latency in regions')

import pickle
with open('latencies_across_region.pkl') as f:
    latencies_across_regions = pickle.load(f)

sim_len = 50
sizes = []
max_val = 0
for lat_arr in latencies_across_regions:
    # vals, _ = np.histogram(lat_arr, bins=[x*5 for x in range(50)])
    density = gaussian_kde(lat_arr)
    x = range(250)
    d_vals = density(x)
    sizes.append(np.concatenate(([0]*20, d_vals), axis=0))
    if d_vals.max() > max_val:
        max_val = d_vals.max()
# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_dots, 249, fargs=(data, sizes, dots, max_val),
                                   interval=50, blit=False)

plt.show()