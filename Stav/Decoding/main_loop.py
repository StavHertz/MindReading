import sys
sys.path.append('../Latency_paper/')
from get_run_on_server import get_run_on_server
import os
import pandas as pd
if get_run_on_server():
	basic_path = '/data/dynamic-brain-workshop/'
else:
	basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')

from load_exp_file import load_exp_file
from plot_all_mean_sdfs import plot_all_mean_sdfs
from get_resource_path import get_resource_path
from create_train_test_data import create_train_test_data

resource_path = get_resource_path()
if not os.path.exists(resource_path):
    os.makedirs(resource_path)

manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
expt_info_df = pd.read_csv(manifest_file)
multi_probe_experiments = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

if get_run_on_server():
	run_short_version = False
else:
	run_short_version = True

# for multi_probe_id in range(len(multi_probe_experiments)):
multi_probe_id = 1
if True:
	print('Analyzing experiment number: ' + str(multi_probe_id))
	
	data_set, multi_probe_filename = load_exp_file(multi_probe_experiments, multi_probe_id, drive_path)

	print(multi_probe_filename)

	X1 = create_train_test_data(data_set, 'natural_scenes', 'VISp', 1.)
	X2 = create_train_test_data(data_set, 'flash_250ms', 'VISp', 1)
	# plot_all_mean_sdfs(data_set, multi_probe_filename)
	# # 'natural_scenes', 'flash_250ms'
	# current_stim_type = 'flash_250ms'
	# current_split_frames = True

	# latency_dataframe = get_experiment_latency_dataframe(data_set, multi_probe_filename, 
	# 	short_version=run_short_version, split_frames=current_split_frames, stim_type=current_stim_type)
	
	# save_exp_dataframe(latency_dataframe, current_stim_type + '_' + multi_probe_filename, resource_path)
	
	# print('Done')