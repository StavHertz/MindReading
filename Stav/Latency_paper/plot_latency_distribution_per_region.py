import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from get_full_latency_dataframe import get_full_latency_dataframe
from get_all_cortical_regions import get_all_cortical_regions
from get_depth_thresh_dict import get_depth_thresh_dict

selected_frame = ''

latency_versions = ['latency_sdf', 'latency_sdf_v2']
# 'latency_sdf', 'latency_sdf_v2'
current_version = 'latency_sdf_v2'
show_natural = True

if show_natural:
    stim_type = 'natural_scenes'
else:
    # 'natural_scenes', 'flash_250ms'
    stim_type = 'flash_250ms'
    selected_frame = '1' # 1:Gray->White, -1:Gray->Black


split_layers = False
save_outputs = False

full_latency_dataframe = get_full_latency_dataframe(stim_type)

cortex_depth = get_depth_thresh_dict(stim_type)


fig, ax = plt.subplots(2,1,figsize=(12,6))
for c_v_ind, current_version in enumerate(latency_versions):
    latencies_across_region = []
    mean_per_region = []
    all_region_names = []
    all_regions = np.unique(full_latency_dataframe['region'])
    for region in all_regions:
        if split_layers and region in get_all_crotical_regions():
            if len(selected_frame) == 0:
                region_units = full_latency_dataframe[(full_latency_dataframe['region'] == region)]
            else:
                region_units = full_latency_dataframe[(full_latency_dataframe['region'] == region) & (full_latency_dataframe['frame'] == selected_frame)]
            all_top_latencies = []
            all_bottom_latencies = []
            for index, row in region_units.iterrows():
                if not np.isnan(row[current_version]):
                    depth_thresh = cortex_depth[row['experiment'] + '_' + row['probe']]
                    if int(row['depth']) > depth_thresh:
                        all_top_latencies.append(row[current_version])
                    else:
                        all_bottom_latencies.append(row[current_version])
            latencies_across_region.append(np.asarray(all_top_latencies))
            mean_per_region.append(np.median(all_top_latencies))
            all_region_names.append(region + '_T')

            latencies_across_region.append(np.asarray(all_bottom_latencies))
            mean_per_region.append(np.median(all_bottom_latencies))
            all_region_names.append(region + '_B')
        else:
            if len(selected_frame) == 0:
                region_units = full_latency_dataframe[(full_latency_dataframe['region'] == region)]
            else:
                region_units = full_latency_dataframe[(full_latency_dataframe['region'] == region) & (full_latency_dataframe['frame'] == selected_frame)]

            all_latencies = region_units[current_version].values.astype(float)
            all_latencies = all_latencies[~np.isnan(all_latencies)]
            latencies_across_region.append(all_latencies)
            mean_per_region.append(np.median(all_latencies))
            all_region_names.append(region)

    # fig, ax = plt.subplots(1,1,figsize=(12,6))
    violin_data = ax[c_v_ind].violinplot(latencies_across_region)
    ax[c_v_ind].set_ylim([0, 300])
    x_axis_vals = range(1, len(all_region_names)+1)
    ax[c_v_ind].set_xticks(x_axis_vals)
    ax[c_v_ind].set_xticklabels(all_region_names)
    ax[c_v_ind].scatter(x_axis_vals, mean_per_region, marker='_')
    if len(selected_frame) > 0:
        title = stim_type + ' - ' + selected_frame + ' - ' + current_version
    else:
        title = stim_type + ' - ' + current_version
    ax[c_v_ind].set_title(title)
    
    if save_outputs:
        fig.savefig('latency_analysis_v12.png')

        import pickle
        with open('latencies_across_region_v12.pkl', 'w') as f:
            pickle.dump(latencies_across_region, f)


    # plt.show(block=False)
plt.show()