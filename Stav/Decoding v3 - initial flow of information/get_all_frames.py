import numpy as np

def get_all_frames(stim_type):
	if stim_type == 'natural_scenes':
		return np.array([2., 12., 23., 35., 48.])
		# return np.array([2., 12., 23., 35., 48., 62., 77., 93.])
		# return np.array(range(1, 118)).astype(float)
		# return np.array(range(1, 5)).astype(float)
		# return np.array(range(1, 3)).astype(float)
	if stim_type == 'drifting_gratings':
		return [0., 45., 90., 135., 180., 225., 270., 315.]
		# return [0., 45., 90., 135.] #  180.  225.  270.  315.
		# return [0., 45.] 
	if stim_type == 'static_gratings':
		return [0., 30., 60., 90., 120., 150.]
		# return [0., 30., 60., 90.] #  120.  150.
		# return [0., 30.]
	if stim_type == 'flash_250ms':
		return [1.]