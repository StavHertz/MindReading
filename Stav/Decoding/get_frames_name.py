
def get_frames_name(stim_type):
	if stim_type == 'natural_scenes':
		return 'frame'
	if stim_type == 'flash_250ms':
		return 'color'
	if stim_type == 'drifting_gratings' or stim_type == 'static_gratings':
		return 'orientation' # 0.   45.   90.  135.  180.  225.  270.  315.