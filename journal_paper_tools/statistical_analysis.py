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
import pandas as pd
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


def box_plot_between_means(path_to_test_one, path_to_test_two, show=False):
    
    
    data_1 = mean_for_each_timestep(path_to_test_one)
    data_2 = mean_for_each_timestep(path_to_test_two) 
    print(len(data_1))
    print(len(data_2))
    title = path_to_test_one.split('/')[-2]
    data_1_name = path_to_test_one.split('/')[-3]
    data_2_name = path_to_test_two.split('/')[-3]
    # This is in a dictionary format. To make a boxplot, i need this to be meaned across all the runs in the dictionaty 
    d = {
        data_1_name : data_1,
        data_2_name : data_2
    }
    datas = pd.DataFrame(data=d)
    
    
    # plt.boxplot(datas)
    sns.boxplot(datas)
    plt.title(title)
    
    if show: 
        plt.show()

def mean_for_each_timestep(path, key=None):
    datas = []
    if key: 
        data = get_all_values_using_key_from_dir_path(path, key)
    else: 
        data = get_all_values_using_key_from_dir_path(path)
    
    for key in data: 
        datas.append(data[key])
    
    return np.mean(datas, axis=0)
    




def _main():
    # path = 'C:/source/atpeterepymarl/src/results/qmix_for_journal/Foraging-2s-10x10-3p-3f-v0/'
    path= 'C:/source/atpeterepymarl/src/results/qmix_best_conf_50steps/Foraging-10x10-3p-3f-v0/'
    # path = 'C:/Users/molly/Desktop/lbf_data/qmix lbf data/Foraging-10x10-3p-3f-v2/'
    path2 = 'C:/source/atpeterepymarl/src/results/qmix_best_conf_100steps/Foraging-10x10-3p-3f-v0/'
    # plot_histogram(path)
    # compare_two_means(path, path2)
    # grab the result values for means 

    box_plot_between_two_means(path, path2, show = True)
if __name__ == "__main__":
    _main()