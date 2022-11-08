import pandas as pd 
import seaborn as sns 
import os 
import json 
import yaml
'''
This scanner will need to get the following values:
results - final step load then use [-1]
number  - the directory number 

'''

def __main():
    path_to_hyperparameter_search = 'datasets\hyperparameter seach qmix 10x10'   
    algo = 'qmix' 
    last_value_dictionary = {}
    list_of_dirs = os.listdir(path_to_hyperparameter_search)
    
    ########## TESTING SINGLE ENTRY CODE ###################
    # print(list_of_dirs)
    # dir = list_of_dirs[0]
    # path_to_metrics = path_to_hyperparameter_search + '\\' + str(dir) + '\\' + 'metrics.json'
    # print(path_to_metrics)
    # # Load the metrics file 
    # with open(path_to_metrics) as f:
    #     loaded_dict = json.load(f)
    
    # print(loaded_dict.keys())
    # last_value_dictionary[dir] = loaded_dict['return_mean']['values'][-1]
    # fin_max = max(last_value_dictionary, key = last_value_dictionary.get)

    ######### TESTING SINGLE ENTRY CODE END ################


    for dir in list_of_dirs:
        path_to_metrics = path_to_hyperparameter_search + '\\' + str(dir) + '\\' + 'metrics.json'
        # load the metrics file 
        with open(path_to_metrics) as f: 
            loaded_dict = json.load(f)
        # grab the last value from the means 
        last_value_dictionary[dir] = loaded_dict['return_mean']['values'][-1]
        
    print(last_value_dictionary)
    # find max value from the dictionary 
    fin_max = max(last_value_dictionary, key = last_value_dictionary.get)
    print("Max value", fin_max)
    # fin_max is the directory number, now you can get the hyperparameters for it:
    path_to_config = path_to_hyperparameter_search + '\\' + str(fin_max) + '\\' + 'config.json'
    
    with open(path_to_config) as f: 
        load_config = json.load(f)
    
    print(load_config)
    # modify the config name to make it different than the original 
    load_config['name'] = algo + '_lbf_coop_best'
    # to turn the hyperparameter config, i simply need to call this 

    # Dump the config 
    with open( algo + '_coop_best.config.yaml', 'w+') as file: 
        file.write(yaml.dump(load_config))


if __name__ == '__main__':

    __main()

