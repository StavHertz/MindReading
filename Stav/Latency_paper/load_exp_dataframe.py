import pickle

def load_exp_dataframe(multi_probe_filename, resource_path):
	with open(resource_path + multi_probe_filename + '_latency_table.pkl') as f:
		latency_dataframe = pickle.load(f)
	return latency_dataframe