import numpy as np
import pandas as pd
from get_full_latency_dataframe import get_full_latency_dataframe
from get_all_cortical_regions import get_all_cortical_regions

def get_depth_thresh_dict():
	full_latency_dataframe = get_full_latency_dataframe()
	all_regions = np.unique(full_latency_dataframe['region'])
	all_cortical_regions = get_all_cortical_regions()
	all_exps = np.unique(full_latency_dataframe['experiment'])

	c_ind = 0
	all_lables = []
	final_dict = {}
	for exp in all_exps:
		all_probes = np.unique(full_latency_dataframe[full_latency_dataframe['experiment'] == exp]['probe'])
		for probe in all_probes:
			all_depths = full_latency_dataframe[(full_latency_dataframe['experiment'] == exp) & (full_latency_dataframe['probe'] == probe) & (full_latency_dataframe['region'].isin(all_cortical_regions))]['depth'].values.astype(int)
			final_dict[exp+'_'+probe] = all_depths.min()+((all_depths.max() - all_depths.min())/2)

	return final_dict
		
