import numpy as np
from get_run_on_server import get_run_on_server
import os
import pandas as pd
if get_run_on_server():
    basic_path = '/data/dynamic-brain-workshop/'
else:
    basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'
import sys
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')
from plot_raster_sdf import plot_raster_sdf
from get_spike_trains_from_unit_id import get_spike_trains_from_unit_id
from get_full_latency_dataframe import get_full_latency_dataframe
from get_resource_path import get_resource_path
from get_mean_sdf_from_spike_train import get_mean_sdf_from_spike_train
from get_latency_from_sdf_v11 import get_latency_from_sdf_v11
from plot_raster_sdf import plot_raster_sdf
from get_resource_path import get_resource_path
from load_exp_file import load_exp_file

full_latency_dataframe = get_full_latency_dataframe()

manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
expt_info_df = pd.read_csv(manifest_file)
multi_probe_experiments = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

for multi_probe_id in range(len(multi_probe_experiments)):    
    data_set, multi_probe_filename = load_exp_file(multi_probe_experiments, multi_probe_id, drive_path)
    low_latency_units = full_latency_dataframe[(full_latency_dataframe.latency_sdf < 50) & (full_latency_dataframe.experiment == multi_probe_filename)]

    for index, row in low_latency_units.iterrows():
    	spike_trains = get_spike_trains_from_unit_id(data_set, row['probe'], row['unit_id'])
    	mean_sdf, spike_raster = get_mean_sdf_from_spike_train(spike_trains)
    	sdf_latency, response_type, pre_stim_dict = get_latency_from_sdf_v11(mean_sdf)
    	c_key = row['experiment'] + '_' + row['unit_id']
    	st_vals = {}
        st_vals['latency_sdf'] = sdf_latency
        st_vals['response_type'] = response_type
        st_vals['latency_sdf_v2'] = 0
        st_vals['response_type_v2'] = 0
        plot_raster_sdf(c_key, spike_trains, '', 
        	mean_sdf, st_vals, pre_stim_dict, 
        	get_resource_path() + row['experiment'] + '_' + row['unit_id'] + '.png')
        print('Saved file for: ' + c_key)