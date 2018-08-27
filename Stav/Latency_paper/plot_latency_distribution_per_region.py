import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from get_all_exp_file_names import get_all_exp_file_names
from get_resource_path import get_resource_path
from load_exp_dataframe import load_exp_dataframe
from get_latency_dataframe import get_latency_dataframe

resource_folder = get_resource_path()
all_exp_files = get_all_exp_file_names()

full_latency_dataframe = []
for exp_file in all_exp_files:
    latency_dataframe = load_exp_dataframe(exp_file, resource_folder)
    full_latency_dataframe.append(latency_dataframe)
full_latency_dataframe = pd.concat(full_latency_dataframe, ignore_index=True)

print(full_latency_dataframe[full_latency_dataframe.unit_id == 'noise'].unit_id)

latencies_across_region = []
mean_per_region = []
all_regions = np.unique(full_latency_dataframe['region'])
for region in all_regions:
    region_units = full_latency_dataframe[full_latency_dataframe['region'] == region]
    all_latencies = region_units['latency_sdf'].values.astype(float)
    all_latencies = all_latencies[~np.isnan(all_latencies)]
    # print(all_latencies)
    latencies_across_region.append(all_latencies)
    mean_per_region.append(all_latencies.mean())

fig, ax = plt.subplots(1,1,figsize=(6,3))
ax.violinplot(latencies_across_region)
ax.set_ylim([0, 300])
x_axis_vals = range(1, len(all_regions)+1)
ax.set_xticks(x_axis_vals)
ax.set_xticklabels(all_regions)
ax.scatter(x_axis_vals, mean_per_region, marker='_')
fig.savefig('latency_analysis_v11.png')
plt.show()