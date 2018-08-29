# -*- coding: utf-8 -*-
"""
Depth analysis

Created on Tue Aug 28 21:45:02 2018

@author: sarap
"""
import pickle
from pandas import pd

latency_path = os.path.normpath('D:/Latencies/10/')

depth_df = pickle.load(open(os.path.join(latency_path, 'VISpm_natural_scenes_latency.pkl')))

