import json
import os 
from pathlib import Path
import shutil
'''
Cartographer; 
metrics needs to be checked 
config.json is where all the information is held

'''

def open_file(path):
    # print(path)
    #check if the file has anything in it 
    if not os.path.getsize(path):
        return {}
    with open(path) as f:
        data = json.load(f)
    
    return data 

def extract_configs(path):
    '''
    This function takes the config file and get the name and env_args[key] values, 
    modifies them and then spits them out  
    tested and works
    '''
    #open config file 
    data = open_file(path)

    algo = data['name']
    env = data['env_args']['key']
    steps = data['env_args']['time_limit']

    return algo, env, steps

def check_metrics(path): 
    '''
    This function checks the metrics file and makes sure it is not empty
    tested and works 
    '''
    empty = False
    # print(path)
    data = open_file(path)
    
    #check empty dictionary
    if not data:
        empty = True
    
    if empty: 
        return 0
    else:
        return 1

def make_mapfile(directory_path):


    return 1

def scan_directory(base_directory_path, algorithm, environment,step=50, show_directory=False):
    counter = 0 
    value_list = []
    folder_list = os.listdir(base_directory_path)
    # TODO: get rid of the -source item
    folder_list.remove('_sources')
    for item, value in enumerate(folder_list):
        directory = base_directory_path+value+'/'
        metrics = directory+'metrics.json'
        # print(metrics)
        # metrics_data = open_file(metrics)
        config = directory+'config.json'
        algo, env, steps = extract_configs(config) 
        # print(value, algo, env, steps)
        if algo == algorithm and env == environment and steps == step:
            if show_directory:
                print(value, steps)
            value_list.append(int(value))
            counter += 1 
        flag = check_metrics(metrics)
        # print(flag)
        if not flag: 
            print(value, " Has empty metrics")
            # delete_directory_contents(directory)
    value_list.sort()
    print("Total number of runs for",algorithm, environment, counter)
    print(value_list)

def delete_directory_contents(path):
    try: 
        shutil.rmtree(path)
    except:
        print('error cleaning directory', path)



if __name__ == "__main__":

    path = 'C:/source/atpeterepymarl/src/results/sacred/'
    atlas_path = 'D:/atlas_DADA/'
    atlas_data_path2 = 'E:/uncorrupted_atlas_data/sacred/'

    algorithms = [ 'qmix', 'maddpg', 'iql_lbf', 'coma', 'ia2c', 'ippo','maa2c','qtran','vdn']
    envs = ['Foraging-8x8-3p-1f-coop-v1','Foraging-8x8-2p-3f-v1', 'Foraging-8x8-2p-2f-coop-v1', 'Foraging-10x10-2p-8f-v1', 'Foraging-2s-8x8-2p-3f-v1' ]
    new_algorithms = ['ippo', 'maa2c', 'mappo', 'coma']
    # algorithms = ['qmix','iql']
    envs = ['Foraging-15x15-4p-3f-v1']

    # envs = ['Foraging-16x16-4p-6f-v1']ex

    # open_file(path)
    # scan_directory(path)
    for _ , alg in enumerate(algorithms):
        for _, env in enumerate(envs):
            scan_directory(path, alg, envs, step = 50, show_directory=False)
    
