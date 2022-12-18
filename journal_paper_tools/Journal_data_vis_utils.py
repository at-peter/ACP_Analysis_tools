import os

import pandas as pd
import json
import os
from matplotlib import pyplot as plt
import statistics
import scipy.stats as st

def open_file(path):
    """
    This function opens the json in the path and returns it as a dictionary.
    It is used to open the config and metrics files.
    Param: path -> text
    return: loaded_dictionary -> dictionary of json
    """

    with open(path) as f:
        loaded_dictionary = json.load(f)
    return loaded_dictionary


def _main():

    value_array = []
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-2s-10x10-3p-3f-v2/'
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-10x10-3p-3f-v2/'
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-8x8-2p-2f-coop-v2/'

    main_path = 'C:/source/atpeterepymarl/src/results/qmix_for_journal/Foraging-2s-8x8-2p-2f-coop-v0/'
    # qplex_qatten_sc2
    # C:\Users\Wintermute\Desktop\best_configs\ippo_8x8_best_config_noseed/Foraging-2s-8x8-2p-2f-coop-v0

    name = main_path.split('/')[-2] + ' ' + main_path.split('/')[-3]
    os.chdir(main_path)
    print(os.getcwd())
    dir_list = os.listdir()
    # list_of_paths = [main_path + '1']
    dataframes = {}
    name = main_path.split('/')[-2] + ' ' + main_path.split('/')[-3]
    for path in dir_list:
        print(path)
        
        metrics_path = main_path + path + '/metrics.json'
        print('metrics path', metrics_path)
        # dataframes[path] = pd.read_json(metrics_path)
        # meow = pd.read_json(metrics_path)
        # print(meow.info())
        # print(meow.head())

        dataframes[path] = open_file(metrics_path)
    # print(dataframes.keys())
    for i, dataframe in enumerate(dataframes):
       # grab the mean values
        # print(dataframe)
        # print(dataframes[dataframe])
        value_array.append(dataframes[dataframe]['return_mean']['values'])
    plt.figure(1)
    max_value_array = []
    mean_value_array = []
    for e,i in enumerate(value_array):
        # print('Max value: ', max(i))
        max_value_array.append(max(i))
        # print('mean value:', statistics.mean(i))
        mean_value_array.append(statistics.mean(i))
        x = range(len(i))
        
        plt.plot(x,i,label= e)
        plt.legend()
    plt.title(name)
    plt.show()
    print(max_value_array)
    print('max value = ', max(max_value_array))
    max_interval = calculate_ninefive_confidence(max_value_array)
    print('Max interval value', max_interval)

    print('Mean value', statistics.mean(mean_value_array))
    interval = calculate_ninefive_confidence(mean_value_array)
    print("Mean interval value ", interval)
 

def calculate_ninefive_confidence(value_array):
    '''
    This function calculates the 95% confidence interval of an array using the T distribution. 
    It outputs the +- value 
    '''
    
    nine_five = st.t.interval(confidence=0.95,
    df=len(value_array)-1,
    loc=statistics.mean(value_array),
    scale=st.sem(value_array))
    interval = statistics.mean(value_array)- nine_five[0] 

    return interval

if __name__ == "__main__":
    _main()