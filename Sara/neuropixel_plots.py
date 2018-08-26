# -*- coding: utf-8 -*-
"""
Plotting functions for neuropixel probe data

Created on Sat Aug 25 09:08:57 2018

@author: sarap
"""

import numpy as np
import matplotlib.pyplot as plt 

def probe_heatmap(psth_matrix, depth, edges):
	"""
	Parameters
	----------
	psth_matrix : np.array
		Matrix of PSTHs ([number of neurons x time])

	depths : list/np.array
		electrode depths corresponding to the rows of psth_matrix

	edges : list/np.array
		time bin edges returned by np.histogram

    Returns
    -------
    fig, ax : matplotlib figure handles
	"""
	fig, ax = plt.subplots(1, 1, figsize=(15,20))
	bin_centers = edges[1:]-(edges[1]-edges[0])/2

	# Plot the firing rate heatmap
	plt.imshow(psth_matrix)
	# Add the stimulus onset, if necessary
	if np.min(edges) < 0:
		pre_time = np.min(edges)
	else:
		pre_time = 0
		ax.vlines(np.where(bin_centers == np.min(np.abs(centers))), ax.get_ylim()[1], ax.get_ylim()[0], 'white', alpha=0.4)

	x_pts, y_pts = np.shape(psth_matrix)
	# Correct the x-axis 
	xfac = ax.get_xticks()/x_pts*np.max(bin_centers)
	xfac = xfac - pre_time
	ax.set_xticklabels([str(np.round(x)) for x in xfac])

	# Correct the y-axis
	yfac = ax.get_yticks()/y_pts*np.max(np.abs(depth))
	ax.set_yticklabels([str(-np.round(y)) for y in yfac])

	# Plot labels
	ax.set_xlabel('Time (ms)', fontsize=20)
	ax.set_ylabel('Depth', fontsize=20)

	return fig, ax


