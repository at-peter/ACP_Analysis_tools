import json 
from scipy import stats 
import math 
import matplotlib.pyplot as plt
import pingouin as pg 
import numpy as np 
import os
import statistics
import math 
import seaborn as sns
from Journal_data_vis_utils import open_file




def get_all_values_using_key_from_dir_path(path_to_collected_data, key='return_mean'):
    """
    This function goes into a directory full of runs and extracts each runs key values into a dictionary. 
    params: path str, key: str
    returns: dict {run_id:[values]}
    """
    data = {}
    os.chdir(path_to_collected_data)
    print(os.getcwd())
    dir_list = os.listdir()
    # get the data
    for path in dir_list:
        metrics_path = path_to_collected_data + path + '/metrics.json'
        print('metrics path', metrics_path)
        file_data = open_file(metrics_path)
        data[path] = [float(x) for x in file_data[key]['values']]

    return data


def plot_histogram(path_to_collected_data, value_to_plot='return_mean'):
    """
    This function creates a histogram of the means for a whole test. 
    This is done in order to be able to confirm the conditions necessary for the t interval. 
    Namely we need to be sure that the data is unimodal and not skewed too much. 
    """
    values = get_all_values_using_key_from_dir_path(path_to_collected_data, value_to_plot)
    print(values)
    # open all the folders in the path to collected data and get the value to print   
    # Create the max values, since they are easy to get. 
    maxes = []
    means = []
    for key in values: 
        maxes.append(max(values[key]))
        means.append(statistics.mean(values[key]))
   
    fig, axis = plt.subplots(figsize=(10,5), ncols=2)
    
    sns.distplot(a=means, hist=True, ax=axis[0])
    axis[0].set_title('Means')
    sns.distplot(a=maxes, hist=True, ax=axis[1])
    axis[1].set_title('Maxes')
    plt.show()
    

def compare_two_means(path_to_test_one, path_to_test_two):
    data_1 = get_all_values_using_key_from_dir_path(path_to_test_one)
    data_2 = get_all_values_using_key_from_dir_path(path_to_test_two) 
    
    data_1_means = get_mean(data_1)
    data_2_means = get_mean(data_2)
    x = pg.ttest(data_1_means, data_2_means, correction = False)
    print(x)
    if x['p-val'].item() < 0.05:
        print("Null hypothesis rejected. Pval is ", x['p-val'].item())
def get_mean(data_dictionary):
    means = []
    for key in data_dictionary: 
        means.append(statistics.mean(data_dictionary[key]))

    return means

def get_maxes(data_dictionary):
    maxes = []
    for key in data_dictionary: 
        maxes.append(max(data_dictionary[key]))
    
    return maxes

def _main():
    path = 'C:/source/atpeterepymarl/src/results/qmix_for_journal/Foraging-2s-8x8-2p-2f-coop-v0/'
    path2= 'C:/source/atpeterepymarl/src/results/qmix_for_journal/Foraging-8x8-2p-2f-coop-v0/'
    # plot_histogram(path)
    compare_two_means(path, path2)
    # grab the result values for means 

if __name__ == "__main__":
    _main()