import numpy as np

def get_all_frames(stim_type):
	if stim_type == 'natural_scenes':
		return np.array([2., 12., 23., 35., 48., 62., 77., 93.])
	if stim_type == 'flash_250ms':
		return [1.]
	if stim_type == 'drifting_gratings':
		return [0., 45., 90., 135.] 
	if stim_type == 'static_gratings':
		return [0., 30., 60., 90.]