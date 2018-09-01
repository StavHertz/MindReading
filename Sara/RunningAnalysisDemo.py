# -*- coding: utf-8 -*-
"""
Experiments with running speed anaysis

Created on Thu Aug 30 09:29:02 2018

@author: sarap
"""

import h5py
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set_context('talk', font_scale=1.6, rc={'lines.markeredgewidth': 2})
sns.plotting_context(rc={'font.size': 18})
sns.set_style('white')
sns.set_palette('deep')

#%% From Shawn's swdb_2018_tools folder
f = h5py.File(dataset.nwb_path, 'r') 

try:
    running_speed = f['acquisition']['timeseries']['RunningSpeed']['data'].value
    running_timestamps = f['acquisition']['timeseries']['RunningSpeed']['timestamps'].value
except:
    running_speed = []
    running_timestamps = []
    
f.close()

#%% 
fig, ax = plt.subplots()
plt.hist(running_speed, bins=75)
ax.set_xlim(0, 75)

#%% Check out the h5 file
list_of_names = []
f.visit(list_of_names)

#%% Plot the running speeds
fig, ax = plt.subplots(1,1,figsize=(8,4))
plt.plot(running_timestamps, running_speed, linewidth=0.5)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Running speed (cm/sec)')