import pickle
import matplotlib.pyplot as plt

def load_and_plot(file_name, title_str=''):
    stim_names = ['Natural vs. Natural', 'Drifting vs. Drifting', 'Static vs. Static']
    with open(file_name) as f:
        [test_rates_over_regions, test_sems_over_regions, all_region_labels] = pickle.load(f)
    
    fig, ax = plt.subplots(1,1,figsize=(12,6))
    for ind in range(len(test_rates_over_regions)):
        all_test_rates = test_rates_over_regions[ind]
        all_test_sems = test_sems_over_regions[ind]
        ax.errorbar(x=range(len(all_test_sems)), y=all_test_rates, yerr=all_test_sems, marker='o')
    ax.set_xticks(range(len(all_region_labels)))
    ax.set_xticklabels(all_region_labels)
    ax.set_xlabel('Region')
    ax.set_ylabel('Classification rate (%)')
    ax.legend(stim_names, loc='lower right')
    ax.set_title(title_str)
    ax.set_ylim([0.45, 0.95])
    plt.show()



# file_name = 'LDA/ephys_multi_10_decoding_table.pkl'
# file_name = 'LDA/ephys_multi_58_decoding_table.pkl'
# file_name = 'KNN/ephys_multi_10_decoding_table.pkl'
file_name = 'KNN/ephys_multi_58_decoding_table.pkl'

load_and_plot(file_name, title_str='KNN - Exp 58')