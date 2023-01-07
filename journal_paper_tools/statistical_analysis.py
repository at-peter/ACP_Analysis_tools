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
import math




def get_all_values_using_key_from_dir_path(path_to_collected_data, key='return_mean'):
    """
    This function goes into a directory full of runs and extracts each runs key values into a dictionary. 
    params: path str, key: str
    returns: dict {run_id:[values]}
    """
    data = {}
    os.chdir(path_to_collected_data)
    # print(os.getcwd())
    dir_list = os.listdir()
    # get the data
    for path in dir_list:
        metrics_path = path_to_collected_data + path + '/metrics.json'
        # print('metrics path', metrics_path)
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
    # print(values)
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

def mean_across_all_runs(path):
    data = get_all_values_using_key_from_dir_path(path)
    means = get_mean(data)
    return means

def max_across_all_runs(path):
    data = get_all_values_using_key_from_dir_path(path)
    maxes = get_maxes(data)
    return maxes


def box_plot_between_means(path_array, show=False):
    names = []
    datas = []
    title = path_array[0].split('/')[-2]
    for path in path_array:
        #get the data for each path
        datas.append(mean_across_all_runs(path))
        names.append(path.split('/')[-3])
    names.insert(0,' ')
    # data_1 = mean_for_each_timestep(path_to_test_one)
    # data_2 = mean_for_each_timestep(path_to_test_two) 
    # print(len(data_1))
    # print(len(data_2))
    # title = path_to_test_one.split('/')[-2]
    # data_1_name = path_to_test_one.split('/')[-3]
    # data_2_name = path_to_test_two.split('/')[-3]
    # # This is in a dictionary format. To make a boxplot, i need this to be meaned across all the runs in the dictionaty 
    # d = {
    #     data_1_name : data_1,
    #     data_2_name : data_2
    # }
    # datas = pd.DataFrame(data=d)
    
    
    plt.boxplot(datas)
    # sns.boxplot(datas)
    # this is the problem 
    ax = plt.gca()
    ax.set_xticks(range(len(datas)+1))
    ax.set_xticklabels(names)
    plt.title(title)
    plt.ylabel('return_mean')
    
    if show: 
        plt.show()

def mean_for_each_timestep(path, key=None, mean_axis=0):
    datas = []
    if key: 
        data = get_all_values_using_key_from_dir_path(path, key)
    else: 
        data = get_all_values_using_key_from_dir_path(path)
    
    for key in data: 
        datas.append(data[key])
    
    return np.mean(datas, axis=mean_axis)
    

def box_plots_axes(major_path, scenarios, ax):
   
    path_to_metrics = [major_path + scenario for scenario in scenarios]
    
    datas = []
    names = []
    for path in path_to_metrics:
        datas.append(mean_across_all_runs(path))
        names.append(path.split('/')[-3])
    # plt.sca(ax)
    ax.boxplot(datas)
    ax.set_title(major_path.split('/')[-2])
    ax.set_xticks((1,2,3,4))
    ax.set_xticklabels(scenarios)
    return 


def box_plots_axes_scenario(major_paths, scenario, ax, maxes = False, parameter='return_mean'):
    # in this case, the scenario is static and we simply add it to each of the major paths. 

    #
    datas = []
    experiments = []
    for path in major_paths: 
        # add the right -v to the scenario: 
        experiments.append(path.split('/')[-2])
        if path.split('/')[2] ==  'molly':
            _scenario = scenario + '-v2/'
        else:
            _scenario = scenario + '-v0/'
        
        # print('scenario data path', scenario ,path + _scenario)
        if not maxes:
            datas.append(mean_across_all_runs(path + _scenario))
        else:
            datas.append(max_across_all_runs(path + _scenario))

    # print(experiments)   
    colors = ['pink', 'lightblue', 'lightgreen','orchid' ]

    bplot = ax.boxplot(datas, patch_artist=True)
    for patch, color in zip(bplot['boxes'],colors):
        patch.set_facecolor(color)
    ax.set_title(scenario)
    ax.set_xticks((1,2,3,4))
    ax.set_xticklabels(experiments)



def plot_all_boxplots_for_comparison(path_array, title, show=False):

    total = len(path_array)
    num_columns = math.ceil(total / 2)
    n_rows = 2 

    boxes = []
    x = range(num_columns)
    y = range(n_rows)
    
    for i in x: 
        for j in y:
            boxes.append((i,j))
    
   
    # need to select the right scenarios based on where the data comes from: 
    scenarios_v0 = [
        'Foraging-8x8-2p-2f-coop-v0/',
        'Foraging-2s-8x8-2p-2f-coop-v0/',
        'Foraging-10x10-3p-3f-v0/',
        'Foraging-2s-10x10-3p-3f-v0/'
    ]

    scenario_v2 = [
        'Foraging-8x8-2p-2f-coop-v2/',
        'Foraging-2s-8x8-2p-2f-coop-v2/',
        'Foraging-10x10-3p-3f-v2/',
        'Foraging-2s-10x10-3p-3f-v2/'
    ]

    # set up the major figure and axes: 
    fig, ax = plt.subplots(num_columns , n_rows, sharey=True)

    plots_ = zip(boxes, path_array )
    for i, (box, path) in enumerate(plots_):
        print(i, box, path)
        comp = path.split('/')[2]
        if comp == 'molly':
                #molly uses v2
            box_plots_axes(path, scenario_v2,ax[box])
        else:
            box_plots_axes(path,scenarios_v0, ax[box])
    
    
    
    # for box in boxes: 
    #     print('box',box)           
    #     for path in path_array:
    #         print(path)

    #         comp = path.split('/')[2]
    #         if comp == 'molly':
    #             #molly uses v2
    #             box_plots_axes(path, scenario_v2,ax[box])
    #         else:
    #             box_plots_axes(path,scenarios_v0, ax[box])
    #         # box_plots_axes()


    # time to populate the axes with the boxplots 
    # for this I need a function that will take in 

    if show:
        fig.suptitle(title + ' means')
        plt.show()


def boxplots_by_scenario(experiment_paths, title, parameter_to_plot='return_mean' ,show=False, maxes=False):
    '''
    This function creates a subplot for each scenario. Each subplot contains a box and whisker comparison of all the different experiments fed to the function

    parameters:
    experiment_paths :: array of paths, paths are str
    title :: str 
    parameter_to_plot :: valid parameter to plot from metrics file, str
    show :: boolean to show plot or not 
    maxes :: boolean to output analysis of max values rather than mean values. 

    '''
    scenarios = [
        'Foraging-8x8-2p-2f-coop',
        'Foraging-2s-8x8-2p-2f-coop',
        'Foraging-10x10-3p-3f',
        'Foraging-2s-10x10-3p-3f'
    ]
    # get the number of subplots to make
    total = len(experiment_paths)
    num_columns = math.ceil(total / 2)
    n_rows = 2 

    boxes = []
    x = range(num_columns)
    y = range(n_rows)
    
    for i in x: 
        for j in y:
            boxes.append((i,j))
    # create the fig and subplot axes 
    fig, ax = plt.subplots(num_columns , n_rows, sharey=True)

    plots_ = zip(boxes, scenarios)

    for i, (box, scenario) in enumerate(plots_):
        # print(i, box, scenario, experiment_paths)
        box_plots_axes_scenario(experiment_paths,scenario, ax[box], maxes=maxes)
        

    if show:
        if maxes:
            fig.suptitle(title + ' maxes '+ parameter_to_plot)
        else:
            fig.suptitle(title + ' ' + parameter_to_plot)
        
        plt.show()



def _main():
    # path = 'C:/source/atpeterepymarl/src/results/qmix_for_journal/Foraging-2s-10x10-3p-3f-v0/'
    big_paths = [
        
        'C:/Users/molly/Desktop/lbf_data/qmix lbf data/',
        'C:/source/atpeterepymarl/src/results/qmix_for_journal/',
        "C:/source/atpeterepymarl/src/results/qmix_lbf_50_steps/",
        'C:/source/atpeterepymarl/src/results/qmix_best_conf_50steps/'
            ]

    path= 'C:/source/atpeterepymarl/src/results/qmix_best_conf_50steps/Foraging-8x8-2p-2f-coop-v0/'
    path3 = 'C:/Users/molly/Desktop/lbf_data/qmix lbf data/Foraging-8x8-2p-2f-coop-v2/'
    path2 = 'C:/source/atpeterepymarl/src/results/qmix_best_conf_100steps/Foraging-8x8-2p-2f-coop-v0/'
    path4 = 'C:/source/atpeterepymarl/src/results/qmix_for_journal/Foraging-8x8-2p-2f-coop-v0/'
    # plot_histogram(path)
    # compare_two_means(path, path2)
    # grab the result values for means 
    paths = [path3 ,path4 ,path, path2]


    # box_plot_between_means(paths, show = True)
    # plot_all_boxplots_for_comparison(big_paths, 'qmix', show= True)
    boxplots_by_scenario(big_paths, 'QMIX response surface between time and reward type',maxes=False ,show=True)
if __name__ == "__main__":
    _main()