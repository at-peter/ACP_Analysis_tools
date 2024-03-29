import os

import pandas as pd
import json
import os
from matplotlib import pyplot as plt
import statistics
import scipy.stats as st
import numpy as np 

# from statistical_analysis import get_all_values_using_key_from_dir_path

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




def plot_lbf_stuff(alg, parameter, scenario, show=True, save=False):

    value_array = []
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-2s-10x10-3p-3f-v2/'
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-10x10-3p-3f-v2/'
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-8x8-2p-2f-coop-v2/'
    # alg = 'vdn'
    # parameter = 'td_error_abs'
    # main_paths = 'C:/Users/molly/Desktop/lbf_data/qmix lbf data/Foraging-10x10-3p-3f-v2/'
    main_lbf_paths = 'C:/source/results for journal/Results for paper/%s/LBF/%s_LBF_25step/'%(alg, alg)
    main_clbf_paths = 'C:/source/results for journal/Results for paper/%s/CLBF/%s_CLBF_25step/'%(alg, alg)
    # scenario = "Foraging-10x10-3p-3f/"
    # 'Foraging-10x10-3p-3f'
    # 'Foraging-2s-8x8-2p-2f-coop/'
    main_path = main_lbf_paths + scenario 
    # 'C:/Users/molly/Desktop/lbf_data/qmix lbf data/Foraging-10x10-3p-3f-v2/'
    # 'C:/source/atpeterepymarl/src/results/qmix_best_conf_100steps/Foraging-10x10-3p-3f-v0/'
    # C:\source\atpeterepymarl\src\results\qmix_best_conf_50steps\Foraging-2s-8x8-2p-2f-coop-v0
    # qplex_qatten_sc2
    # C:\Users\Wintermute\Desktop\best_configs\ippo_8x8_best_config_noseed/Foraging-2s-8x8-2p-2f-coop-v0

    # Get 
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
        value_array.append(dataframes[dataframe][parameter]['values'])
    plt.figure(1, figsize = (18,12))
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

    if show:
        plt.show()  
    elif save:
        plt.savefig(parameter+'_lineplot.png')
    plt.clf()
    

    print(max_value_array)
    print('max value = ', max(max_value_array))
    max_interval = calculate_ninefive_confidence(max_value_array)
    print('Max interval value', max_interval)
    output_laytex_max_values(max_value_array,max_interval)

    print('Mean value', statistics.mean(mean_value_array))
    interval = calculate_ninefive_confidence(mean_value_array)
    print("Mean interval value ", interval)
    output_laytex_mean_values(mean_value_array,interval)
    print(os.getcwd())

def plot_clbf_stuff(alg, parameter, scenario, show=True, save=False):

    value_array = []
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-2s-10x10-3p-3f-v2/'
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-10x10-3p-3f-v2/'
    # main_path = 'C:/Users/Wintermute/Desktop/best_configs/ippo_8x8_best_config_noseed/Foraging-8x8-2p-2f-coop-v2/'
    # alg = 'vdn'
    # parameter = 'td_error_abs'
    # main_paths = 'C:/Users/molly/Desktop/lbf_data/qmix lbf data/Foraging-10x10-3p-3f-v2/'
    main_lbf_paths = 'C:/source/results for journal/Results for paper/%s/LBF/%s_LBF_25step/'%(alg, alg)
    main_clbf_paths = 'C:/source/results for journal/Results for paper/%s/CLBF/%s_CLBF_50step/'%(alg, alg)
    # scenario = "Foraging-10x10-3p-3f/"
    # 'Foraging-10x10-3p-3f'
    # 'Foraging-2s-8x8-2p-2f-coop/'
    main_path = main_clbf_paths + scenario 
    # 'C:/Users/molly/Desktop/lbf_data/qmix lbf data/Foraging-10x10-3p-3f-v2/'
    # 'C:/source/atpeterepymarl/src/results/qmix_best_conf_100steps/Foraging-10x10-3p-3f-v0/'
    # C:\source\atpeterepymarl\src\results\qmix_best_conf_50steps\Foraging-2s-8x8-2p-2f-coop-v0
    # qplex_qatten_sc2
    # C:\Users\Wintermute\Desktop\best_configs\ippo_8x8_best_config_noseed/Foraging-2s-8x8-2p-2f-coop-v0

    # Get 
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
        value_array.append(dataframes[dataframe][parameter]['values'])
    plt.figure(1, figsize = (18,12))
    max_value_array = []
    mean_value_array = []
    # TODO: I could probably mean here using numpy and then 
    for e,i in enumerate(value_array):
        # print('Max value: ', max(i))
        max_value_array.append(max(i))
        # print('mean value:', statistics.mean(i))
        mean_value_array.append(statistics.mean(i))
        x = range(len(i))
        
        plt.plot(x,i,label= e)
        plt.legend()
    plt.title(name)
    if show: 
        plt.show()
    elif save:
        plt.savefig(parameter+'_lineplot.png')
    plt.clf()

    # plt.show()

    print(max_value_array)
    print('max value = ', max(max_value_array))
    max_interval = calculate_ninefive_confidence(max_value_array)
    print('Max interval value', max_interval)
    output_laytex_max_values(max_value_array,max_interval)

    print('Mean value', statistics.mean(mean_value_array))
    interval = calculate_ninefive_confidence(mean_value_array)
    print("Mean interval value ", interval)
    output_laytex_mean_values(mean_value_array,interval)
    print(os.getcwd())
   

def _main():
    alg = 'qmix'
    parameter = 'return_mean'
    # Foraging-8x8-2p-2f-coop/
    # Foraging-2s-8x8-2p-2f-coop/
    # Foraging-10x10-3p-3f/
    # Foraging-2s-10x10-3p-3f/


    scenario = "Foraging-2s-10x10-3p-3f/"
    shows = False
    saves = False 

    # plot_clbf_stuff(alg, parameter, scenario, show=shows, save=saves)
    plot_lbf_stuff(alg, parameter, scenario, show=shows, save=saves)

    ## getting means 
    # alg = 'ippo'
    # scenario = "Foraging-10x10-3p-3f/"
    # main_lbf_paths = 'C:/source/results for journal/Results for paper/%s/LBF/%s_LBF_25step/'%(alg, alg)
    # path_run = main_lbf_paths + scenario
    
    # plot_mean_for_run(path_run)

 

def plot_mean_for_run(path_to_a_run, key='return_mean'):
    means = mean_for_each_timestep(path_to_a_run, key=key, mean_axis=0)
    print(means)
    x = range(len(means))
    plt.plot(x, means)
    plt.show()



def get_all_values_using_key_from_dir_path(path_to_collected_data, key='return_mean'):
    """
    This function goes into a directory full of runs and extracts each runs key values into a dictionary. 
    params: path str, key: str
    returns: dict {run_id:[values]}
    """
    data = {}
    print('path in get all ', path_to_collected_data)
    os.chdir(path_to_collected_data)
    # print(os.getcwd())
    dir_list = os.listdir()
    print('inside get_all_values_using_key', dir_list)
    # get the data
    for path in dir_list:
        metrics_path = path_to_collected_data + path + '/metrics.json'
        print('metrics path', metrics_path)
        file_data = open_file(metrics_path)
        data[path] = [float(x) for x in file_data[key]['values']]

    return data

def mean_for_each_timestep(path, key=None, mean_axis=0):
    datas = []
    if key: 
        data = get_all_values_using_key_from_dir_path(path, key)
    else: 
        data = get_all_values_using_key_from_dir_path(path)
    
    print('data', len(data))
    for key in data: 
        datas.append(data[key])
    
    return np.mean(datas, axis=mean_axis)

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


def output_laytex_max_values(max_array, max_conf):
    round_val = round(max(max_array),2)
    round_conf = round(max_conf,2)
    output = '$ %s \pm %s $'%(round_val, round_conf)
    print(output)

def output_laytex_mean_values(mean_array, mean_conf):

    round_val = round(statistics.mean(mean_array),2)
    round_conf = round(mean_conf,2)
    output = '$ %s \pm %s $'%(round_val, round_conf)
    print(output)

if __name__ == "__main__":
    _main()