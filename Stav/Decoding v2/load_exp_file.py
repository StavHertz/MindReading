import os
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

def load_exp_file(multi_probe_experiments, experiment, drive_path):
    multi_probe_filename = multi_probe_experiments.iloc[experiment]['nwb_filename']
    nwb_file = os.path.join(drive_path, multi_probe_filename)
    data_set = NWB_adapter(nwb_file)
    return data_set, multi_probe_filename[:-4]