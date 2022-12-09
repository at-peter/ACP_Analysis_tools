import json
from math import sqrt
import numpy as np 
# import pandas as pd 
from pathlib import Path
import seaborn as sns
from matplotlib import pyplot as plt


def open_file(path):
    '''
    This function opens the json in the path and returns it as a dictionary 
    '''
    with open(path) as f:
        loaded_dictionary = json.load(f)
    return loaded_dictionary


def plot_means_of_many_runs(run_array, path_array, label_array, plot_info = ('title', 'training episodes', 'normalized reward')):
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
        min_len = len(mean[0])
        # TODO: october 1 i have to cut down all the sizes to be the same. .
        # need to check if the sizes are all the same: 
        for data in range(len(mean)):
            # this loop finds the min 
            print(data, len(mean[data]))
            if min_len > len(mean[data]): 
                min_len = len(mean[data])
        
        print('min len',min_len)
        
        for data in range(len(mean)):
            # this loop cuts stuff down
            length = len(mean[data])
            diff = length - min_len
            for i in range(diff):
                mean[data].pop()
                se[data].pop()

             
        np_se = np.array(se)
        # turn into variance 
        np_se = np.square(np_se)
        #mean over all variance batches
        np_se = np.mean(np_se, axis = 0)
        #make standard error 
        np_se = np.sqrt(np_se)
        np_se = np_se * (1/sqrt(the_len))
        # print("before", np_se)
        np_se = np_se * 1.96
        # print('average standard error', np_se)
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
    
    plt.title(plot_info[0])
    plt.xlabel(plot_info[1])
    plt.ylabel(plot_info[2])
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
    atlas_data_path2 = 'E:/uncorrupted_atlas_data/sacred/'
    molly_data_path = 'C:/source/atpeterepymarl/src/results/sacred/'
    
    
    '''
    16x16-4f-6f 
    '''
    # steps50 =[[500],[502],[503],range(505,521)]
    # steps50 = collect_data_ranges(steps50)
    # print(len(steps50))
    # steps100 = collect_data_ranges([[541],range(543,549),range(550,562)])
    # print(len(steps100))
    # steps215 = collect_data_ranges([range(568,583),range(584,588)])
    # print(len(steps215))
    # experiment_list = [steps50, steps100, steps215]
    # path_list = [molly_data_path, molly_data_path, molly_data_path]
    # lable_list = ['iql - 50 steps', 'iql - 100 steps ', 'iql - 215 steps']
    # plot_info_tuple = ('Foraging-16x16-4p-6f-v1', 'training episodes', 'normalized reward')
   
    
    '''
    Plotting experiment 1 data:
    '''
    
    '''
    Foraging-8x8-3p-1f-coop-v1
    '''
    # experiment_list = [[433, 434, 435, 436, 437, 438, 451, 452, 453, 454, 455, 456, 487, 488, 489, 490, 491, 492, 571, 572, 573, 574, 575, 576],
    # [439, 440, 441, 442, 443, 444, 457, 458, 459, 460, 461, 462, 493, 494, 495, 496, 497, 498, 565, 566, 567, 568, 569, 570]
    # ]
    # path_list = [atlas_data_path2,atlas_data_path2]
    # lable_list =['Qmix','IQL']
    # plot_info_tuple = ('Foraging-8x8-3p-1f-coop-v1', 'training episodes', 'normalized reward')

    '''
    Foraging-8x8-2p-3f-v1
    '''
    # experiment_list = []
    # path_list = []
    # lable_list =[]

    '''Foraging-8x8-2p-2f-coop-v1'''
    experiment_list = [range(292,297),range(349,354),range(316, 321),range(355,360)]
    path_list = [molly_data_path, atlas_data_path2,atlas_data_path2,atlas_data_path2]
    lable_list =['Maddpg', 'VDN', 'Qmix', 'IQL']
    plot_info_tuple = ('Foraging-8x8-2p-2f-coop-v1', 'training episodes', 'normalized reward')
 
    '''Foraging-10x10-2p-8f-v1'''
    
    # experiment_list = [range(322,351),
    # [226, 227, 228, 229, 230, 231, 244, 245, 246, 247, 248, 249, 280, 281, 292, 293, 294, 295, 296, 297, 304, 305, 306, 307, 308, 309, 535, 536, 537],
    # [238, 239, 240, 241, 242, 243, 274, 275, 276, 277, 278, 279, 286, 287, 288, 289, 290, 291, 298, 299, 300, 301, 302, 303, 529, 530, 531, 532, 533]]
    # for i in experiment_list:
    #     print(len(i))
    # path_list = [molly_data_path,atlas_data_path2, atlas_data_path2]
    # lable_list =['Maddpg','VDN','IQL']
    # plot_info_tuple = ('Foraging-10x10-2p-8f-v1', 'training episodes', 'normalized reward')

    '''Foraging-2s-8x8-2p-3f-v1'''
    # vdn = collect_data_ranges([range(148,153),range(166,171),range(196,201),range(208,213),range(220,225)])
    # iql = collect_data_ranges([range(142,147), range(160, 165), range(190,195), range(202,207), range(214,219)])
    # experiment_list = [vdn, iql]
    # path_list = [atlas_data_path,atlas_data_path]
    # lable_list =['VDN','IQL']
    # plot_info_tuple = ('Foraging-2s-8x8-2p-2f-v1', 'training episodes', 'normalized reward')

    '''Foraging-15x15-4p-5f'''
    for i in range(1, 5):
        print(range(1,5))
        print(i)
    qmix = [608, 609, 610, 614, 617]
    print(len(qmix))
    maddpg = [618, 620, 621, 622, 627]
    print(len(maddpg))
    vdn = [619, 623, 624, 625, 626]
    print(len(vdn))
    iql = [611, 612, 613, 615, 616]
    print(len(iql))
    experiment_list = [qmix,maddpg, iql, vdn]
    path_list= [molly_data_path,molly_data_path,molly_data_path,molly_data_path]
    lable_list=['QMIX','MADDPG','IQL', 'VDN ']
    plot_info_tuple = ('Foraging-15x15-4p-5f ; averaged over 5 runs, confidence interval is z score', 'training episodes', 'normalized reward')


    '''
    experiment 2 plots
    '''
    
    '''
    Foraging-8x8-2p-3f-v1
    '''
    # experiment_list = [range(595,600),range(577,582), range(601,606),range(589,594)]
    # path_list = [atlas_data_path2,atlas_data_path2,atlas_data_path2,atlas_data_path2]
    # lable_list =['mappo','ippo','maa2c','coma']
    # plot_info_tuple = ('Foraging-8x8-2p-3f-v1', 'training episodes', 'normalized reward')


    plot_means_of_many_runs(experiment_list, path_list,lable_list,plot_info_tuple)
   
    '''
    Deprecated code for reference:
    '''

    # disjointed_array  = [[458, 460,462,469,474,477,483,484,485],[464,465,466,470,475,476,479,481,486], [459,461,467,468,471,473,478,482,487]]
    
    # lables = ['Agent 0 - MADDPG','Agent 0 - vdn', 'Agent 0 - iql', 'Agent 0 - QMIX', 'Agent 1 - MADDPG' ,'Agent1 vdn', 'Agent 1 iql', 'Agent 1 QMIX' ]
    # lables = []


    # plot_means_of_many_runs(experiment_list, path_list,lable_list)
    # plot_means_of_many_runs(experiment_list, path_list,lable_list)
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


    
