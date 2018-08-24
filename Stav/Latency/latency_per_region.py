# AWS
basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'

# We need to import these modules to get started
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Import NWB_adapter
import os
import sys
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

from filter_spikes_by_region_stimulus import filter_spikes_by_region_stimulus


current_stimulus = ['natural_images']

# Provide path to manifest file
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')

# Create a dataframe 
expt_info_df = pd.read_csv(manifest_file)

#make new dataframe by selecting only multi-probe experiments
multi_probe_expt_info = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

#all_regions = []
#
#for multi_probe_example in range(len(multi_probe_expt_info)):
#
#    multi_probe_filename  = multi_probe_expt_info.iloc[multi_probe_example]['nwb_filename']
#
#    # Specify full path to the .nwb file
#    nwb_file = os.path.join(drive_path,multi_probe_filename)
#
#    data_set = NWB_adapter(nwb_file)
#    unique_regions = np.unique(data_set.unit_df['structure'])
#    unique_list = list(unique_regions)
#    all_regions.extend(unique_list)
#
#all_regions = list(set(all_regions))
all_regions = ['VISp', 'VISrl', 'DG', 'CA', 'VISal', 'VISam', 'SCs', 'TH', 'VISpm', 'VISl']
print(all_regions)

for region in all_regions:
    region_spikes = filter_spikes_by_region_stimulus(multi_probe_expt_info, region, current_stimulus)
    plt.plot(region_spikes)
    break