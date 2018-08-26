basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'

from print_info import print_info
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

from load_exp_file import load_exp_file
from get_experiment_latency_dataframe import get_experiment_latency_dataframe
from save_exp_dataframe import save_exp_dataframe