import numpy as np
import pandas as pd
from get_full_latency_dataframe import get_full_latency_dataframe
from get_all_crotical_regions import get_all_crotical_regions
import matplotlib.pyplot as plt

full_latency_dataframe = get_full_latency_dataframe()
all_regions = np.unique(full_latency_dataframe['region'])
print(all_regions)
all_cortical_regions = get_all_cortical_regions()
all_exps = np.unique(full_latency_dataframe['experiment'])

fig, ax = plt.subplots(1,1,figsize=(12,6))
c_ind = 0
all_lables = []
for exp in all_exps:
	all_probes = np.unique(full_latency_dataframe[full_latency_dataframe['experiment'] == exp]['probe'])
	for probe in all_probes:
		all_depths = full_latency_dataframe[(full_latency_dataframe['experiment'] == exp) & (full_latency_dataframe['probe'] == probe) & (full_latency_dataframe['region'].isin(all_cortical_regions))]['depth'].values.astype(int)
		ax.plot([c_ind, c_ind], [all_depths.max(), all_depths.min()], marker='_')
		# ax.scatter(c_ind, all_depths.max())
		# ax.scatter(c_ind, all_depths.min())
		all_lables.append(exp[-2:]+'_'+probe[-1])
		c_ind += 1
	ax.axvline(x=c_ind-0.5, color='black')

ax.set_xticks(range(len(all_lables)))
ax.set_xticklabels(all_lables)
ax.set_xlabel('Probe ID')
ax.set_ylabel('Depth')
ax.set_title('Spread of unit depth in cortex across probes')
plt.show()