import pickle

def save_exp_dataframe(latency_dataframe, multi_probe_filename, resource_path):
	with open(resource_path + multi_probe_filename + '_latency_table.pkl', 'w') as f:
		pickle.dump(latency_dataframe, f)