import os
import pandas as pd
basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'
import sys
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')

from load_exp_file import load_exp_file
from get_experiment_latency_dataframe import get_experiment_latency_dataframe
from save_exp_dataframe import save_exp_dataframe
from get_resource_path import get_resource_path

resource_path = get_resource_path()
if not os.path.exists(resource_path):
    os.makedirs(resource_path)

manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
expt_info_df = pd.read_csv(manifest_file)
multi_probe_experiments = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

for multi_probe_id in range(len(multi_probe_experiments)):
	data_set, multi_probe_filename = load_exp_file(multi_probe_experiments, multi_probe_id, drive_path)
	latency_dataframe = get_experiment_latency_dataframe(data_set, multi_probe_filename, short_version=True)
	save_exp_dataframe(latency_dataframe, multi_probe_filename, resource_path)