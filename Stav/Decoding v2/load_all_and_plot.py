import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_all_and_plot(file_names):
    include_perm = False
    stim_names = ['Natural vs. Natural', 'Drifting vs. Drifting', 'Static vs. Static']
    if include_perm:
        stim_names.extend(['Permutation test'])
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

    if include_perm:
        row2 = np.zeros((len(all_region_labels)))
        for file_ind, file_name in enumerate(perm_file_names):
            with open(file_name) as f:
                [test_rates_over_regions, test_sems_over_regions, all_region_labels] = pickle.load(f)

            row2 += np.nan_to_num(np.array(test_rates_over_regions).flatten())

            for ind in range(len(test_rates_over_regions)):
                all_test_rates = test_rates_over_regions[ind]
                all_test_sems = test_sems_over_regions[ind]
                ax.scatter(x=range(len(all_test_sems)), y=all_test_rates, color=all_colors[ind+3], marker=all_markers[file_ind], alpha=0.5)
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
        print(row)

    if include_perm:
        row2 = row2/div_vals[0]
        ax.plot(row2, linewidth=4, marker='o', markersize=8)

    ax.set_xticks(range(len(all_region_labels)))
    ax.set_xticklabels([lbl[:lbl.index(' ')] for lbl in all_region_labels])
    ax.set_yticklabels([40, 50, 60, 70, 80, 90])
    ax.set_xlabel('Region', fontsize=22)
    ax.set_ylabel('Decoding accuracy (%)', fontsize=22)
    ax.legend(stim_names, loc='lower right', fontsize=14)
    ax.set_title('Decoding accuracy across regions', fontsize=24)
    ax.set_ylim([0.45, 0.95])
    for i in range(5,10):
        ax.axhline(y=i/float(10), color='gray', alpha=0.5)
    ax.tick_params(axis='both', which='major', labelsize=16)
    plt.show()




# file_name = 'LDA/ephys_multi_10_decoding_table.pkl'
# file_name = 'LDA/ephys_multi_58_decoding_table.pkl'
# file_name = 'KNN/ephys_multi_10_decoding_table.pkl'
file_names = ['LDA/ephys_multi_10_decoding_table.pkl', 'LDA/ephys_multi_58_decoding_table.pkl', 'LDA/ephys_multi_21_decoding_table.pkl']
perm_file_names = ['ephys_multi_10_perm_decoding_table.pkl', 'ephys_multi_58_perm_decoding_table.pkl', 'ephys_multi_21_perm_decoding_table.pkl']
load_all_and_plot(file_names)