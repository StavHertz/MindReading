from get_run_on_server import get_run_on_server

def get_resource_path():
	if get_run_on_server():
		return 'Output/'
	else:
		return '../../../Resources/Paper/' # ''