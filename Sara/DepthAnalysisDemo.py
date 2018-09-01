# -*- coding: utf-8 -*-
"""
Depth analysis demos, data exploration

Created on Wed Aug 29 15:31:00 2018

@author: sarap
"""
import os
import pickle
import pandas as pd
import numpy as np
import seaborn as sns
sns.set_context('talk', font_scale=2, rc={'lines.markeredgewidth': 2})
sns.plotting_context(rc={'font.size': 18})
sns.set_style('white')
sns.set_palette('deep');

#%% Check out channel map
channel_positions_file = os.path.join(drive_path,'channel_positions.csv')
ch_map = pd.read_csv(channel_positions_file)

fig, ax = plt.subplots(1, 1, figsize=(4,8))
ax.plot(ch_map['horizontal_pos'], ch_map['vertical_pos'], marker='o', linestyle='none', alpha=0.2)
ax.set_title('Neuropixel channels')

#%% Load in a data frame and explore data/visualizations
latency_path = os.path.normpath('D:/Latencies/10/')
depth_df = pickle.load(open(os.path.join(latency_path, 'VISpm_natural_scenes_latency.pkl')))

#%% Joint histograms
fig, ax = plt.subplots()
g = sns.jointplot(depth_df['latency'], depth_df['depth'], kind="kde", height=7, space=0, stat_func=None, color=region_color('VISpm'))
#g.savefig(os.path.join(latency_path, 'VISpm_natural_scenes_joint.png'))

#%% Scatterplot
fig, ax = plt.subplots()
ax.plot(depth_df['latency'], depth_df['depth'], marker='o', alpha=0.2, linestyle='none')
ax.set_xlabel('latency (ms)')
ax.set_ylabel('depth (um)')
ax.set_title('')

#%% Single plot
counts, edges = np.histogram(depth_df['depth'], bins=10)
plt.plot(edges[:-1], counts)

latency_mean = np.zeros_like(counts)
latency_median = np.zeros_like(counts)
latency_std = np.zeros_like(counts)
latency_sem = np.zeros_like(counts)

depths = depth_df['depth'].values
latencies = depth_df['latency'].values
depths = depths[depth_df['latency'].notna()]
latencies = latencies[depth_df['latency'].notna()]

for i in range(len(edges)-1):
    ind = np.where((depths >= edges[i]) & (depths < edges[i+1]))
    latency_mean[i] = np.mean(latencies[ind])
    latency_median[i] = np.median(latencies[ind])
    latency_std[i] = np.std(latencies[ind])
latency_sem = latency_std/len(latency_std)
    
fig, ax = plt.subplots()
ax.plot(depths, latencies, marker='o', linestyle='none', color='k', alpha=0.2)
ax.errorbar(edges[:-1], latency_mean, yerr=latency_std, marker='o', label='mean')
ax.plot(edges[:-1], latency_median, marker='o', label='median')
ax.set_ylabel('Latency (ms)')
ax.set_xlabel('Depth (um)')

#%% Joint histogram, option #2
grid = sns.JointGrid(depth_df['latency'], depth_df['depth'], space=0, ratio=50)
grid.plot_joint(plt.scatter, color="g")
grid.plot_marginals(sns.rugplot, height=1, color="g")
