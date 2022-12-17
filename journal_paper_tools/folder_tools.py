from copy import copy
import os
import shutil
"""
Created November 20 2022 to fix if your HS is in muliple folders and you need add results directories together. 
"""

def copy_folder(source, destination):
    
    # Read source directory tree
    # read destination directory tree
    max_source_value, source_dir_list = extract_directory_tree(source)
    max_destination_value, dest_dir_list = extract_directory_tree(destination)
    
    print('destination', max_destination_value, dest_dir_list)
    print('source', max_source_value,source_dir_list)
    
    for i, e in enumerate(source_dir_list):
        source_item_path = source + '/' +str(e)
        destination_number = max_destination_value + i + 1 
        destination_path = destination + '/' +str(destination_number)
        # print(source_item_path, destination_number, destination_path)
        # os.mkdir(destination_path)
        move_files(source_item_path, destination_path)


    # for each value in the the list: 
    # copy all the directories into 

def move_files(source_path, destination_path):
    # try:
    print('copying:', source_path )
    shutil.copytree(
        source_path,
        destination_path,
        symlinks=False,
        ignore=None,
        copy_function=shutil.copy2,
        ignore_dangling_symlinks=False,
        dirs_exist_ok=True )
    # except:
    #     print("transfer failed for", source_path)
    return None


def extract_directory_tree(path):
    # need to move os to the location in path 
    cwd = os.getcwd()
   
    os.chdir(path)
    x = os.listdir()

    # get rid of _sources directory: 
    y = max(x)
    x.remove(y)

    # convert the str into ints
    z = list(map(int,x))
    # get the final value that is in the list:
    
    max_val = max(z)

    # sort the list 
    z.sort()

    # at the end, change back to the original working directory
    os.chdir(cwd)
    return max_val, z 

def sort_results_by_environment(path_to_results,list_of_environments):
    """
    This function sorts a results directory by environment. This is useful when you have a bunch of environments in a
    single results directory.
    """
    import json
    os.chdir(path_to_results)
    dir_list = os.listdir()
    print(os.getcwd())

    # get rid of sources 
    y = max(dir_list)
    dir_list.remove(y)
    print(dir_list)
    # create directories for each of the 
    for env in list_of_environments:
        # print(env)
        try:
            os.makedirs(env)
        except:
            print("Already created")
    
    #now i go through each directory, 
    for dir in dir_list:
    # open the config file
        path_to_config = path_to_results  + str(dir) + '/config.json'
        # print('path to config', path_to_config)
        try:
            with open(path_to_config) as f:
                loaded_dict = json.load(f)
            dir_env = loaded_dict['env_args']['key']
            for env in list_of_environments:
                if dir_env == env:
                    # move dir into the folder that is responsible for it
                    source = path_to_results + str(dir)
                    destination = path_to_results + str(env) +'/'+  str(dir)
                    print('source', source)
                    print('destination', destination)
                    move_files(source, destination)
        except FileNotFoundError:
            print('not the right directory ')

def sort_results_by_name(path_to_results,list_of_names):
    """
    This function sorts a results directory by environment. This is useful when you have a bunch of environments in a
    single results directory.
    """
    import json
    print(path_to_results)
    path_to_results = path_to_results + '/'
    print(os.getcwd)
    os.chdir(path_to_results)
    dir_list = os.listdir()
    print(os.getcwd())

    # get rid of sources 
    y = max(dir_list)
    dir_list.remove(y)
    print(dir_list)
    # create directories for each of the 
    for env in list_of_names:
        # print(env)
        try:
            os.makedirs(env)
        except:
            print("Already created")
    
    #now i go through each directory, 
    for dir in dir_list:
    # open the config file
        path_to_config = path_to_results  + '/' +str(dir) + '/config.json'
        print('path to config', path_to_config)
        try:
            with open(path_to_config) as f:
                loaded_dict = json.load(f)
            dir_name = loaded_dict['name']
            print('Loaded name', dir_name)
            for name in list_of_names:
                print('evaluating name', name)
                if dir_name == name:
                    # move dir into the folder that is responsible for it
                    source = path_to_results + '/' + str(dir)
                    destination = path_to_results + '/' + str(name) +'/'+  str(dir)
                    print('source', source)
                    print('destination', destination)
                    move_files(source, destination)
        except FileNotFoundError:
            print('not the right directory ')

def _main():
    
    
    #### merge folders into one #####
    # path1 = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/qmix/qmix_8x8_hs_2'
    # path2 = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/qmix/qmix_8x8_hs_realone'
    # base_path = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8'
    # source = 'C:/source/atpeterepymarl/src/results/the_other_qtran'
    # destination = 'C:/source/atpeterepymarl/src/results/qtran_regular_hs'
    
    # copy_folder(source, destination)


    #### Sort by environments #########
    path_to_results = "C:/source/atpeterepymarl/src/results/qplex_testings_different_configs/"
    
    list_of_envs = [
        'Foraging-10x10-3p-3f-v0',
        'Foraging-2s-10x10-3p-3f-v0',
        'Foraging-8x8-2p-2f-coop-v0',
        'Foraging-2s-8x8-2p-2f-coop-v0'
    ]
    list_of_names = [
        # 'qmix_best_conf_0',
        # 'qmix_best_conf_1'
        'qplex_sc2',
        'qplex_qatten_sc2'
    ]
    
    
    # sort_results_by_environment(path_to_results,list_of_envs)

    for env in list_of_envs:
        path_to_env = path_to_results + env
        print(env)
        sort_results_by_name(path_to_env, list_of_names)
    

if __name__ == '__main__':
    _main()