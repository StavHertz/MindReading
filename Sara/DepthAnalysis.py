# -*- coding: utf-8 -*-
"""
Depth analysis

Created on Tue Aug 28 21:45:02 2018

@author: sarap
"""
import pickle
import pandas as pd
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
g.savefig(os.path.join(latency_path, 'VISpm_natural_scenes_joint.png'))

#%% Scatterplot
fig, ax = plt.subplots()
ax.plot(depth_df['latency'], depth_df['depth'], marker='o', alpha=0.2, linestyle='none')
ax.set_xlabel('latency (ms)')
ax.set_ylabel('depth (um)')
ax.set_title('')

#%% Joint histogram, option #2
grid = sns.JointGrid(depth_df['latency'], depth_df['depth'], space=0, ratio=50)
grid.plot_joint(plt.scatter, color="g")
grid.plot_marginals(sns.rugplot, height=1, color="g")


#%% Cycle through areas
regions = {'VISpm', 'VISam', 'VISp', 'VISl', 'VISal', 'VISrl', 'TH', 'SCs', 'DG', 'CA'}
for region in regions:
    fpath = os.path.join(latency_path, '{}_natural_scenes_latency'.format(region))
    if not os.path.exists(fpath + '.pkl'):
        continue
    f = open(fpath+'.pkl')
    depth_df = pickle.load(f)
    f.close()
    not_nan = depth_df['latency'].notna()
    if len(np.where(not_nan.values == True)[0]) < 3:
        continue
    
    g = sns.jointplot(depth_df['latency'], depth_df['depth']*1e-3, kind='kde', space=0, stat_func=None, color=region_color(region))
    g.plot_marginals(sns.rugplot, height=0.12, color="k")
    g.set_axis_labels(xlabel='{} latency (ms)'.format(region), ylabel='{} depth (mm) '.format(region))
    g.savefig(fpath + '.png')
    
