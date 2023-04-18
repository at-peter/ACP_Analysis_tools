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
from pprint import pprint



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
    

def compare_two_means(path_to_test_one, path_to_test_two, scenario):
    print('path 1', path_to_test_one)
    print('path 2', path_to_test_two)

    data_1 = get_all_values_using_key_from_dir_path(path_to_test_one + scenario)
    data_2 = get_all_values_using_key_from_dir_path(path_to_test_two + scenario) 
    
    data_1_means = get_mean(data_1)
    data_2_means = get_mean(data_2)
    x = pg.ttest(data_1_means, data_2_means, correction = False)
    print(x)
    if x['p-val'].item() < 0.05:
        print("Null hypothesis rejected. Pval is ", x['p-val'].item())
    
    return x


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

def mean_across_all_runs(path, parameter = 'return_mean'):
    print('Path for mean', path)
    data = get_all_values_using_key_from_dir_path(path, key=parameter)
    means = get_mean(data)
    return means

def max_across_all_runs(path, parameter = 'return_mean'):
    data = get_all_values_using_key_from_dir_path(path, key=parameter)
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
        print('path for plot', path)
        # add the right -v to the scenario: 
        experiments.append(path.split('/')[-2])
        # if path.split('/')[2] ==  'molly':
        #     _scenario = scenario + '-v2/'
        # else:
        #     _scenario = scenario + '-v0/'
        
        # print('scenario data path', scenario ,path + scenario)
        if not maxes:
            datas.append(mean_across_all_runs(path + scenario, parameter))
        else:
            datas.append(max_across_all_runs(path + scenario, parameter))

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
    fig, ax = plt.subplots(num_columns , n_rows)

    plots_ = zip(boxes, path_array )
    for i, (box, path) in enumerate(plots_):
        # print(i, box, path)
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


def boxplots_by_scenario(experiment_paths, title, parameter_to_plot='return_mean' ,show=False, maxes=False, save_fig=False):
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
        'Foraging-8x8-2p-2f-coop/',
        'Foraging-2s-8x8-2p-2f-coop/',
        'Foraging-10x10-3p-3f/',
        'Foraging-2s-10x10-3p-3f/'
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
    fig, ax = plt.subplots(num_columns , n_rows, figsize = (18,12))

    plots_ = zip(boxes, scenarios)

    for i, (box, scenario) in enumerate(plots_):
        print(i, box, scenario, experiment_paths)
        box_plots_axes_scenario(experiment_paths,scenario, ax[box], maxes=maxes,parameter=parameter_to_plot)
        

    if show:
        if maxes:
            fig.suptitle(title + ' maxes '+ parameter_to_plot)
        else:
            fig.suptitle(title + ' ' + parameter_to_plot)
    
        plt.show()
    
    if save_fig:
        print(os.getcwd())
        path = experiment_paths[0].split('/')
        path = '/'.join(path[:5]) + '/'
        print(path)
        os.chdir(path)
        if maxes:
            fig.suptitle(title + ' maxes '+ parameter_to_plot)
        else:
            fig.suptitle(title + ' ' + parameter_to_plot)
        plt.savefig(path + 'boxplots_' + parameter_to_plot +'.png' )
        


def mean_lineplots_by_scenario(experiment_paths, title, parameter_to_plot='return_mean' ,show=False, maxes=False):
    scenarios = [
        'Foraging-8x8-2p-2f-coop/',
        'Foraging-2s-8x8-2p-2f-coop/',
        'Foraging-10x10-3p-3f/',
        'Foraging-2s-10x10-3p-3f/'
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
    fig, ax = plt.subplots(num_columns , n_rows)

    plots_ = zip(boxes, scenarios)

    for i, (box, scenario) in enumerate(plots_):
        print(i, box, scenario, experiment_paths)
        # TODO: this is where you populate each box with a plot of means of the value rather than boxplots. 
        # box_plots_axes_scenario(experiment_paths,scenario, ax[box], maxes=maxes,parameter=parameter_to_plot)
        

    if show:
        if maxes:
            fig.suptitle(title + ' maxes '+ parameter_to_plot)
        else:
            fig.suptitle(title + ' ' + parameter_to_plot)
        
        plt.show()



def bartletts_test(array):
    # in order to do bartletts test, i need to get the mean arrays 
    one, two = array
    result = stats.bartlett(one, two)
    print('-----------------------------------------------')
    print(result)
    print('p value', result[1])
    if result[1] <= 0.05: 
        print('null hypothesis rejected, variances are different')
        print('---------------------------------------------')
    else: 
        print('null hypothesis accepted, variances are statistically the same.')
        print('----------------------------------------------')
    return result[1]

def calculate_bartlett(paths_to_experiments, parameter='return_mean', maxes = False):
    means_25 = []
    means_50 = []

    scenarios = [
        'Foraging-8x8-2p-2f-coop/',
        'Foraging-2s-8x8-2p-2f-coop/',
        'Foraging-10x10-3p-3f/',
        'Foraging-2s-10x10-3p-3f/'
    ]
    
    # add the scenarios to the experiment:
    # open each scenario 
    # parse the data into the two sections that I need: 
    # 25 - 
    df = pd.DataFrame(columns=scenarios, index=[25,50])
    var_df = pd.DataFrame(columns=scenarios, index=[25,50])
    for scenario in scenarios: 
        # open the list 
        print("############################################################")
        print('scenario', scenario)
        for path in paths_to_experiments:  
            # print('path', path)  
            path_to_scenario = path + scenario
            # print('Path to scenario', path_to_scenario)
            data_dict = get_all_values_using_key_from_dir_path(path_to_scenario, key=parameter)
            the_mean = get_mean(data_dict)
            if maxes: 
                the_mean = get_maxes(data_dict)
            
            step_num = path_to_scenario.split('/')[-3]
            # print('step num', step_num)
            step_num_last = step_num.split('_')[-1]
            # print('step num last', step_num_last)
            num = step_num_last[:2]
            # print('num', num)
            if num == '25':
                means_25.append(the_mean)
            if num == '50': 
                means_50.append(the_mean)

        # print('means 25',means_25)
        # print('means 50',means_50)
        if means_25:
            print('25')
           
            df[scenario][25] = bartletts_test(means_25)
            # variance calculation: 
            # var_25 = np.var(means_25[0])
            var_25 = [np.var(means_25[i]) for i in range(len(means_25))]
            var_df[scenario][25] = var_25[1]-var_25[0]
            means_25.clear()
            
        
        if means_50: 
            print('50')
            
            df[scenario][50] = bartletts_test(means_50)
            # var_50 = np.var(means_50[0])
            var_50 = [np.var(means_50[i]) for i in range(len(means_50))]
            var_df[scenario][50] = var_50[1]- var_50[0]
            means_50.clear()
        print("############################################")

    # here we can create a dataframe that is outside of each scenario 
    print(os.getcwd())
    # need to get back to the major path; 
    path_list = paths_to_experiments[-1].split('/')
    print('path_list', path_list)
    
    print(df.head())
    print('path to experiments', paths_to_experiments[-1])
    path_to_csv = '/'.join(paths_to_experiments[-1].split('/')[:5] ) + '/' + parameter + '.csv'
    # path_to_csv = paths_to_experiments[-1].split('/')[-2].split('_')[0] + '_' + parameter + '.csv'
    print(path_to_csv)
    print('Difference of variance dataframe ')
    print(var_df.head())
    # from pathlib import Path 
    # path = Path(os.getcwd()).joinpath(path_to_csv)
    # print(path)
    df.to_csv(path_to_csv)







def _main():
   
    
    alg = 'mappo'
    path_to_results = ['C:/source/results for journal/Results for paper/%s/LBF/%s_LBF_25step/'%(alg, alg),
    'C:/source/results for journal/Results for paper/%s/LBF/%s_LBF_50step/'%(alg, alg),
    'C:/source/results for journal/Results for paper/%s/CLBF/%s_CLBF_25step/'%(alg, alg),
    'C:/source/results for journal/Results for paper/%s/CLBF/%s_CLBF_50step/'%(alg, alg)
    ]

    parameter_keys = [
        'return_mean', 
        'grad_norm',
        'loss', 
        'q_taken_mean',
        'target_mean'
    ]
    ippo_keys = [
        'agent_grad_norm',
        'critic_grad_norm',
        'critic_loss'
        'pg_loss',
        'pi_max',
        'advantage_mean'
    ]
    scenarios = [
        'Foraging-8x8-2p-2f-coop/',
        'Foraging-2s-8x8-2p-2f-coop/',
        'Foraging-10x10-3p-3f/',
        'Foraging-2s-10x10-3p-3f/'
    ]
    # plot_histogram(path)
    # df = pd.DataFrame(columns=[scenarios], index=['p-value'])
    # pvalues = {}
    # for scenario in scenarios:
    #     pvalues[scenario] = compare_two_means(path_to_results[0], path_to_results[2], scenario)['p-val'].item()
    
    # print(df.head())
    # pprint(pvalues)
    # grab the result values for means 
   
    # box_plot_between_means(paths, show = True)
    # plot_all_boxplots_for_comparison(big_paths, 'qmix', show= True)
    parameter_plot = 'advantage_mean'
    boxplots_by_scenario(path_to_results, '%s response surface between time and reward type'%alg ,parameter_to_plot=parameter_plot ,maxes=False ,show=False, save_fig=True)
   
    calculate_bartlett(path_to_results,parameter=parameter_plot, maxes = False)

if __name__ == "__main__":
    _main()