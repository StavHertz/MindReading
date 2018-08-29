import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from get_full_latency_dataframe import get_full_latency_dataframe
from get_all_crotical_regions import get_all_crotical_regions
from get_depth_thresh_dict import get_depth_thresh_dict

selected_frame = ''

latency_versions = ['latency_sdf', 'latency_sdf_v2']
# 'latency_sdf', 'latency_sdf_v2'
current_version = 'latency_sdf'
show_natural = True

if show_natural:
    stim_type = 'natural_scenes'
else:
    # 'natural_scenes', 'flash_250ms'
    stim_type = 'flash_250ms'
    selected_frame = '1' # 1:Gray->White, -1:Gray->Black

display_plot = True
split_layers = False
save_outputs = False

cortex_depth = get_depth_thresh_dict(stim_type)

full_latency_dataframe = get_full_latency_dataframe(stim_type)

all_exps = np.unique(full_latency_dataframe.experiment)
regions_in_all_exps = np.unique(full_latency_dataframe.region)

if display_plot:
    fig, ax = plt.subplots(1,1,figsize=(12,6))
else:
    fig, ax = plt.subplots(4,1,figsize=(12,6))

for c_v_ind, exp in enumerate(all_exps):
    current_latency_dataframe = full_latency_dataframe[(full_latency_dataframe['experiment'] == exp)]
    latencies_across_region = []
    mean_per_region = []
    all_region_names = []
    all_regions = np.unique(current_latency_dataframe['region'])
    for region in all_regions:
        if len(selected_frame) == 0:
            region_units = current_latency_dataframe[(current_latency_dataframe['region'] == region)]
        else:
            region_units = current_latency_dataframe[(current_latency_dataframe['region'] == region) & (current_latency_dataframe['frame'] == selected_frame)]

        all_latencies = region_units[current_version].values.astype(float)
        all_latencies = all_latencies[~np.isnan(all_latencies)]
        if len(all_latencies) == 0:
            all_latencies = np.zeros(1)
        latencies_across_region.append(all_latencies)
        mean_per_region.append(np.median(all_latencies))
        all_region_names.append(region)

    if display_plot:
        regional_medians = []
        for region_e in regions_in_all_exps:
            if region_e in all_region_names:
                regional_medians.append(mean_per_region[all_region_names.index(region_e)])
            else:
                regional_medians.append(0)
        ax.set_ylim([0, 200])
        x_axis_vals = range(1, len(regions_in_all_exps)+1)
        ax.set_xticks(x_axis_vals)
        ax.set_xticklabels(regions_in_all_exps)
        ax.plot(x_axis_vals, regional_medians, marker='o')
        print(exp)
        print(regional_medians)
    else:
        violin_data = ax[c_v_ind].violinplot(latencies_across_region)
        ax[c_v_ind].set_ylim([0, 300])
        x_axis_vals = range(1, len(all_region_names)+1)
        ax[c_v_ind].set_xticks(x_axis_vals)
        ax[c_v_ind].set_xticklabels(all_region_names)
        ax[c_v_ind].scatter(x_axis_vals, mean_per_region, marker='_')
        if len(selected_frame) > 0:
            title = exp + ' - ' + stim_type + ' - ' + selected_frame + ' - ' + current_version
        else:
            title = exp + ' - ' + stim_type + ' - ' + current_version
        # ax[c_v_ind].set_title(title)
        

plt.show()