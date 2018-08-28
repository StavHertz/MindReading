import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from get_full_latency_dataframe import get_full_latency_dataframe
from get_all_crotical_regions import get_all_crotical_regions
from get_depth_thresh_dict import get_depth_thresh_dict

full_latency_dataframe = get_full_latency_dataframe()

cortex_depth = get_depth_thresh_dict()
split_layers = False
current_version = 'latency_sdf'
latencies_across_region = []
mean_per_region = []
all_region_names = []
all_regions = np.unique(full_latency_dataframe['region'])
for region in all_regions:
    if split_layers and region in get_all_crotical_regions():
        region_units = full_latency_dataframe[full_latency_dataframe['region'] == region]
        all_top_latencies = []
        all_bottom_latencies = []
        for index, row in region_units.iterrows():
            if not np.isnan(row[current_version]):
                depth_thresh = cortex_depth[row['experiment'] + '_' + row['probe']]
                # print(row['depth'])
                # print(depth_thresh)
                # print('--')
                if int(row['depth']) > depth_thresh:
                    all_top_latencies.append(row[current_version])
                else:
                    all_bottom_latencies.append(row[current_version])
        latencies_across_region.append(np.asarray(all_top_latencies))
        mean_per_region.append(np.mean(all_top_latencies))
        all_region_names.append(region + '_T')

        latencies_across_region.append(np.asarray(all_bottom_latencies))
        mean_per_region.append(np.mean(all_bottom_latencies))
        all_region_names.append(region + '_B')
    else:
        region_units = full_latency_dataframe[full_latency_dataframe['region'] == region]
        all_latencies = region_units[current_version].values.astype(float)
        all_latencies = all_latencies[~np.isnan(all_latencies)]
        latencies_across_region.append(all_latencies)
        mean_per_region.append(all_latencies.mean())
        all_region_names.append(region)

# print(latencies_across_region)
fig, ax = plt.subplots(1,1,figsize=(12,6))
violin_data = ax.violinplot(latencies_across_region)
ax.set_ylim([0, 300])
x_axis_vals = range(1, len(all_region_names)+1)
ax.set_xticks(x_axis_vals)
ax.set_xticklabels(all_region_names)
ax.scatter(x_axis_vals, mean_per_region, marker='_')
fig.savefig('latency_analysis_v12.png')
plt.show()

import pickle
with open('latencies_across_region_v12.pkl', 'w') as f:
    pickle.dump(latencies_across_region, f)