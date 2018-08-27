import matplotlib

def get_color_list():
	color_list = []
	for name, hex in matplotlib.colors.cnames.iteritems():
		color_list.append(name)
	return color_list