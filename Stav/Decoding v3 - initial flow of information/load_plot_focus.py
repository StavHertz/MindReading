from get_resource_path import get_resource_path
import pickle
multi_probe_filename = 'ephys_multi_58'
with open(multi_probe_filename + '_decoding_table.pkl') as f:
	[information_table, sems_table, all_x_axis, all_regions] = pickle.load(f)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1,1,figsize=(12,6))
for row in information_table:
    ax.plot(all_x_axis, row, marker='o')
for i in range(5,10):
    ax.axhline(y=i/float(10), color='gray', alpha=0.5)
ax.legend(all_regions, loc='upper left')
ax.set_ylabel('Decoding accuracy (%)')
ax.set_ylim([0.43, 0.93])
ax.set_yticklabels([40, 50, 60, 70, 80, 90])
ax.set_xlabel('Window size (ms)')
ax.set_title('Decoding accuracy based on window size (exp10, natural)')
plt.show()
