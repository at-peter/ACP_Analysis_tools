import json
from numpy import array 
import pandas as pd 
from pathlib import Path
import seaborn as sns
from matplotlib import pyplot as plt
path = Path('C:/source/atpeterepymarl/src/results/sacred/44/metrics.json')

def open_file(path):
    with open(path) as f:
        loaded_dictionary = json.load(f)
    return loaded_dictionary


def plot_many_means(array_of_experiments, legend_labels):
    
    mean_array = []
    std_array = []
    # open each of the experiment directories and extract all the metrics dictionaries
    for i , experiment in enumerate(array_of_experiments):
        path_str = 'C:/source/atpeterepymarl/src/results/sacred/' + str(experiment) +  '/metrics.json'
        path = Path(path_str) 
        data = open_file(path)
        # extract all the training mean data from each dictionary
        mean_array.append(data['return_mean']['values'])
        # extract all the training standard deviation data from the dictionary
        std_array.append(data['return_std']['values'])
    


    
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
    plt.show()
    return 1 

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







if __name__ == '__main__':
    '''
    This code plots the means of the epymarl code. 
    
    '''
    sns.set_theme(style='darkgrid')
    # sns.set_palette("bright")
    sns.set_palette("Set2")
    experiment_list = range(242,252)
    # lables = ['Agent 0 - MADDPG','Agent 0 - vdn', 'Agent 0 - iql', 'Agent 0 - QMIX', 'Agent 1 - MADDPG' ,'Agent1 vdn', 'Agent 1 iql', 'Agent 1 QMIX' ]
    lables = []

    plot_many_means(experiment_list, lables)
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
