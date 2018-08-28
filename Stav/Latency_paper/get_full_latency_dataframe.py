import numpy as np
import pandas as pd
from get_all_exp_file_names import get_all_exp_file_names
from get_resource_path import get_resource_path
from load_exp_dataframe import load_exp_dataframe

def get_full_latency_dataframe():
	resource_folder = get_resource_path()
	all_exp_files = get_all_exp_file_names()

	full_latency_dataframe = []
	for exp_file in all_exp_files:
	    latency_dataframe = load_exp_dataframe(exp_file, resource_folder)
	    full_latency_dataframe.append(latency_dataframe)
	full_latency_dataframe = pd.concat(full_latency_dataframe, ignore_index=True)
	return full_latency_dataframe