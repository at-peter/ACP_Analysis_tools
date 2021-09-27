import json
from math import sqrt
import numpy as np 
# import pandas as pd 
from pathlib import Path
import seaborn as sns
from matplotlib import pyplot as plt


def open_file(path):
    with open(path) as f:
        loaded_dictionary = json.load(f)
    return loaded_dictionary


def plot_means_of_many_runs(run_array, path_array, label_array):
    '''

    '''
    run_means = []
    run_mins = []
    run_maxs =[]

    #TODO: Check if the ranges align, if they dont exit cause 
    it = iter(run_array)
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        raise ValueError('not all lists have same length!')

    for run_index, run in enumerate(run_array):

        #set up the path string 

        #open the file at the path
        mean, se = get_mean_var_data(run, path_array[run_index])
        # each array in se is the se of a whole batch of runs, 
        # i need to square all values in the array, and average those, then sqrt them to get SE
        print('single standard error',se[0])
        np_se = np.array(se)
        # turn into variance 
        np_se = np.square(np_se)
        #mean over all variance batches
        np_se = np.mean(np_se, axis = 0)
        #make standard error 
        np_se = np.sqrt(np_se)
        np_se = np_se * (1/sqrt(the_len))
        print("before", np_se)
        np_se = np_se * 1.96
        print('average standard error', np_se)
        # get the mean, min and max values from the mean 
        np_mean = np.array(mean)
        
        np_means = np.mean(np_mean, axis=0)
        
        # np_max = np.max(np_mean, axis=0)
        # np_min = np.min(np_mean, axis=0)
        np_max = np.add(np_means,np_se)
        np_min = np.subtract(np_means, np_se)
        # print(np_max)
        # append those to respective arrays
        run_means.append(np_means)
        run_mins.append(np_min)
        run_maxs.append(np_max)
    
    
    # plotting now 
    colors = ['g', 'b', 'r', 'c', 'm', 'y', 'k','w']
    plt.figure(0)
    for index, run in enumerate(run_means):
        x_len = range(len(run))
        plt.plot(run, colors[index])
        plt.fill_between(x_len, run_mins[index], run_maxs[index], facecolor=colors[index], alpha=0.3)
    
    plt.title('Results of 16x16-4p-3f with varied max steps')
    plt.xlabel('training episodes')
    plt.ylabel('normalized reward')
    plt.legend(label_array)
    plt.show()
 

def get_mean_var_data(array_of_experiments, base_path):
    '''
    inputs: [range of sequential numebrs representing experiments that are of the same grouping]
    '''
    means = []
    std = []
    for i, experiment in enumerate(array_of_experiments):
        path_str = base_path + str(experiment) + '/metrics.json'
        path_str = Path(path_str)
        data = open_file(path_str)
        
        means.append(data['return_mean']['values'])
        std.append(data['return_std']['values'])
        
    
    return means, std 

def plot_many_means(array_of_experiments, legend_labels):
    
    mean_array = []
    std_array = []
    # open each of the experiment directories and extract all the metrics dictionaries
    # FIXME: this for loop can be replaced by get_mean_var_data
    for i , experiment in enumerate(array_of_experiments):
        # path_str = 'C:/source/atpeterepymarl/src/results/sacred/' + str(experiment) +  '/metrics.json'
        path_str = 'D:/atlas_DADA/' + str(experiment) +  '/metrics.json'
        path = Path(path_str) 
        data = open_file(path)
        # extract all the training mean data from each dictionary
        mean_array.append(data['return_mean']['values'])
        # extract all the training standard deviation data from the dictionary
        std_array.append(data['return_std']['values'])
    
    # TODO: sept 9, this is where we break things:
    np_mean = np.array(mean_array)
    np_means = np.mean(np_mean, axis=0)
    
    np_max = np.max(np_mean, axis=0)
    print(np_max)
    np_min = np.min(np_mean, axis=0)


    #get step value: 
    steps = data['return_mean']['steps']
    print(len(steps))
    #mean figure
    plt.figure(0)
    for i, y in enumerate(mean_array):
        # plt.plot(steps,y)
        sns.lineplot(x=steps, y=y)
        print(i)
        print(len(y))
    plt.legend(legend_labels)
    plt.title("Normalized Episode return mean comparison")
    plt.xlabel('Updates')
    plt.ylabel('Normalized Episode return mean values')
    
    #std figure 
    plt.figure(1)
    for i, y in enumerate(std_array):
        plt.plot(steps,y)
    plt.legend(legend_labels)
    plt.title("Normalized Episode return std mean comparison")
    plt.xlabel('Updates')
    plt.ylabel('Normalized Episode return std mean values')
    
    # TODO: this is test code
    plt.figure(2)
    x_len = range(len(np_means))
    plt.plot(x_len, np_means)
    plt.fill_between(x_len, np_min, np_max, facecolor='g', alpha=0.3)
    # plt.plot(x_len, np_max)
    # plt.plot(x_len, np_min)
    plt.title('means MADDPG 8x8 2p 3f')
    plt.show()
    return 1 


def plot_means_of_means():
    '''
    This is the function to get the plots for experiment 1. 
    This function will take an array of ranges of files, extract the data, create a single mean array for the 
    '''

def plot_individual_agent_values(experiment_list, agent_legend_labels, number_of_agent):
    
    means = {
        'agent_0': [],
        'agent_1': []
        }

    std = {
        'agent_0' : [],
        'agent_1' : []
    }

    for i , experiment in enumerate(experiment_list):
        path_str = 'C:/source/atpeterepymarl/src/results/sacred/' + str(experiment) +  '/metrics.json'
        path = Path(path_str) 
        data = open_file(path)
        
        # extract all the training mean data from each dictionary
        # mean_array.append(data['return_mean']['values'])
        
        means['agent_0'].append(data['agent_0_mean_returns']['values'])
        means['agent_1'].append(data['agent_1_mean_returns']['values'])
        # extract all the training standard deviation data from the dictionary
        # std_array.append(data['return_std']['values'])
    
    steps = data['agent_0_mean_returns']['steps']
    
    print('steps', len(steps))
    
    colors = ['b','g', 'r', 'c', 'm', 'y', 'k', 'w']
    styles = ['--','-','-.','o','s', 'x',]

    plt.figure(0)
    for i, y in enumerate(means.values()):
        print('y', len(y))
        # sns.lineplot(x=steps, y=y[0])
        for m in range(len(y)):
            # sns.lineplot(x=steps, y = y[i])
            plt.plot(steps, y[m], colors[m] + styles[i])
    
    plt.legend(agent_legend_labels)
    plt.title("Normalized agent episode return mean comparison for 8x8-2p-3f")
    plt.xlabel('Updates')
    plt.ylabel('Normalized Episode return mean values')
    plt.show()


def plot_many_individual_agent_values(run_array, path_array, label_array):
    '''
    This function takes a list of lists containing similar scenarios, extracts individual agent data from those runs, 
    and plots them with a 95% confidence interval. 

    Input :
    run_array = [range(runs), range(runs), [manual_run_list],...]
    path_array = [location_of_range1, location_of_range2, ...]
    label_array = [algorithm_label1, algorithm_label2] 
    '''
    #TODO: September 25

def get_individual_agent_mean_var_data():
    '''
    This function wi
    '''
def collect_data_ranges(disjointed_data_array):
    '''
    This is for many disjointed obvious sections
    '''
    data_array=[]
    for _, data_segment in enumerate(disjointed_data_array):
	    data_array.extend(data_segment)

    return data_array
if __name__ == '__main__':
    '''
    This code plots the means of the epymarl code. 
    
    '''
    sns.set_theme(style='darkgrid')
    # sns.set_palette("bright")
    sns.set_palette("Set2")
    atlas_data_path = 'D:/atlas_DADA/'
    molly_data_path = 'C:/source/atpeterepymarl/src/results/sacred/'
    # experiment_list = [range(152,181),range(192,221), range(41,70)]
    experiment_list=range(152,181)
    path_list = [molly_data_path,molly_data_path,molly_data_path]
    lable_list = ['iql - 215 steps','iql - 100 steps', 'iql - 50 steps']
    disjointed_array  = [[458, 460,462,469,474,477,483,484,485],[464,465,466,470,475,476,479,481,486], [459,461,467,468,471,473,478,482,487]]
    
    lables = ['Agent 0 - MADDPG','Agent 0 - vdn', 'Agent 0 - iql', 'Agent 0 - QMIX', 'Agent 1 - MADDPG' ,'Agent1 vdn', 'Agent 1 iql', 'Agent 1 QMIX' ]
    # lables = []


    # plot_means_of_many_runs(experiment_list, path_list,lable_list)
    plot_means_of_many_runs(disjointed_array, path_list,lable_list)
    # means, var = get_mean_var_data(experiment_list,base_path)
    
    # plot_many_means(experiment_list, lables)
    # plot_individual_agent_values(experiment_list,lables, 2)
    
   
    # data_dict = open_file(path)
    # print(data_dict.keys())
    # # print(data_dict['return_std'])
    # plt.figure(1)
    # x = data_dict['return_mean']['steps']
    # y = data_dict['return_mean']['values']
    # sns.lineplot(x=x, y=y)
    # plt.title('QMIX 9x9-2p-3f mean return for all agents across evaluations for 60 steps')
    # plt.ylabel('return value (normalized)')
    # plt.xlabel('Update (in million steps)')
    
    # xx = data_dict['return_std']['steps']
    # yy = data_dict['return_std']['values']
    # plt.figure(2)
    # sns.lineplot(x=xx, y=yy)
    # plt.title('QMIX 9x9-2p-3f mean return std for all agents across evaluations for 60 steps')
    # plt.ylabel('std value (normalized)')
    # plt.xlabel('Update (in million steps)')
    
    # plt.show()
