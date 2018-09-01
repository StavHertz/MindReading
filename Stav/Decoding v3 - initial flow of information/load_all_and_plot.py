import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_all_and_plot(file_name):
    stim_names = ['Natural vs. Natural', 'Drifting vs. Drifting', 'Static vs. Static']
    all_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    all_markers = ['*', 'x', 'v']

    fig, ax = plt.subplots(1,1,figsize=(12,6))

    stim_region_list = []
    for file_ind, file_name in enumerate(file_names):
        with open(file_name) as f:
            [test_rates_over_regions, test_sems_over_regions, all_region_labels] = pickle.load(f)

        stim_region_list.append(np.array(test_rates_over_regions))

        for ind in range(len(test_rates_over_regions)):
            all_test_rates = test_rates_over_regions[ind]
            all_test_sems = test_sems_over_regions[ind]
            ax.scatter(x=range(len(all_test_sems)), y=all_test_rates, color=all_colors[ind], marker=all_markers[file_ind], alpha=0.5)
            # ax.errorbar(x=range(len(all_test_sems)), y=all_test_rates, yerr=all_test_sems, marker='o')


    sum_vals = np.zeros(stim_region_list[0].shape)
    div_vals = np.zeros(stim_region_list[0].shape)
    for exp_id in range(len(stim_region_list)):
        c_stim_region = np.nan_to_num(stim_region_list[exp_id])
        sum_vals = sum_vals + c_stim_region
        c_div_vals = c_stim_region.copy()
        c_div_vals[c_div_vals>0] = 1
        div_vals = div_vals + c_div_vals
    sum_vals = sum_vals/div_vals

    for row in sum_vals:
        ax.plot(row, linewidth=4, marker='o', markersize=8)


    ax.set_xticks(range(len(all_region_labels)))
    ax.set_xticklabels([lbl[:lbl.index(' ')] for lbl in all_region_labels])
    ax.set_xlabel('Region', fontsize=22)
    ax.set_ylabel('Decoding accuracy', fontsize=22)
    ax.legend(stim_names, loc='lower right', fontsize=14)
    ax.set_title('Decoding accuracy across regions', fontsize=24)
    ax.set_ylim([0.45, 0.95])
    ax.tick_params(axis='both', which='major', labelsize=16)
    plt.show()




# file_name = 'LDA/ephys_multi_10_decoding_table.pkl'
# file_name = 'LDA/ephys_multi_58_decoding_table.pkl'
# file_name = 'KNN/ephys_multi_10_decoding_table.pkl'
file_names = ['LDA/ephys_multi_10_decoding_table.pkl', 'LDA/ephys_multi_58_decoding_table.pkl', 'LDA/ephys_multi_21_decoding_table.pkl']

load_all_and_plot(file_names)