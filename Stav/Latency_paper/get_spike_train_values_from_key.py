def get_spike_train_values_from_key(spike_train_name):
	split_arr = spike_train_name.split('__')
	st_vals = {}
	st_vals['experiment'] = split_arr[0]
	st_vals['probe'] = split_arr[1]
	st_vals['region'] = split_arr[2]
	st_vals['unit_id'] = split_arr[3]
	st_vals['depth'] = split_arr[4]
	st_vals['full_unit_id'] = spike_train_name
	if len(split_arr) == 6:
		st_vals['frame'] = split_arr[5]
	else:
		st_vals['frame'] = 0

	return st_vals