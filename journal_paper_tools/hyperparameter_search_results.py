
import os 
import json 
import yaml
from deepdiff import DeepDiff 
import pprint
import statistics
'''
This scanner will need to get the following values:
results - final step load then use [-1]
number  - the directory number 

'''
def extract_last_value_from_metrics_for_a_search(path_to_hyperparameter_search, info_key):
    """
    This function goes through a hyperparameter search directory and extracts the final value in info_key
    info_key : string, the key to use in metrics.json
    path_to_hyperparameter_search : string, path to the directory that contains the results from EPYMARL 
    returns:  
        last_value_dictionary : dict with keys that are run number 
    
    useful keys:  
    * return_std
    * return_mean 
    * test_return_mean
    * test_return_std

    """
    last_value_dictionary = {}
    last_30_value_dictionary = {}
    last_max_value_dictionary = {}
    list_of_dirs = os.listdir(path_to_hyperparameter_search)
    for dir in list_of_dirs:
        if dir == '_sources':
            #skip the sources directory
            continue
        path_to_metrics = path_to_hyperparameter_search + '\\' + str(dir) + '\\' + 'metrics.json'
        # load the metrics file 
        with open(path_to_metrics) as f: 
            try:
                loaded_dict = json.load(f)
            except:
                print("Dir ",dir, " has problems")


        # grab the last value from the means
        last_30_values = loaded_dict[info_key]['values'][-30:-1]
        total_max_value = max(loaded_dict[info_key]['values'])
        mean_of_last_30_values = statistics.mean(last_30_values)

        #### just the last value #####
        last_value_dictionary[int(dir)] = loaded_dict[info_key]['values'][-1]

        ###### last 30 values #####
        last_30_value_dictionary[int(dir)] = mean_of_last_30_values

        ## the biggest value of all ####
        last_max_value_dictionary[int(dir)] = total_max_value

    return last_value_dictionary, last_30_value_dictionary, last_max_value_dictionary

def extract_configs(path_to_directory, directory_number):

    path_to_config = path_to_directory + '\\' + str(directory_number) + '\\' + 'config.json'
    # path_to_config = path_to_second_hs_search + '\\' + str(fin_max) + '\\' + 'config.json'    
    with open(path_to_config) as f: 
        load_config = json.load(f)
        
    return load_config 

def __main():
    """
    This code is used to go through the hyperparameter search directory get the final mean return values, and create a
    list of configs that are in first place.
    """
    #### WHEN ON MOLLY #####
    # path_to_hyperparameter_search = "C:/source/atpeterepymarl/src/results/qtran_regular_hs"


    ###### When on Wintermute
    path_to_hyperparameter_search = "C:/Users/Wintermute/Desktop/hyperparameter search 10x10/ia2c_10x10_hs"
    # qmix path 2: C:\Users\Wintermute\Desktop\hyperparameter search 8x8\qmix\qmix_8x8_hs_2
    algo = 'ia2c'
    last_value_dictionary = {}
    list_of_dirs = os.listdir(path_to_hyperparameter_search)
    # list_of_dirs = os.listdir(path_to_second_hs_search)
    
    last_value_dictionary, last_30, last_max = extract_last_value_from_metrics_for_a_search(path_to_hyperparameter_search, 'return_mean')
    last_test_value_dictionary, _, _ = extract_last_value_from_metrics_for_a_search(path_to_hyperparameter_search, 'test_return_mean')
    # TODO December 09 2022, grab more than just means.
    
    last_std_value_dictionary, _, _  = extract_last_value_from_metrics_for_a_search(path_to_hyperparameter_search, 'return_std')
    # find max value from the dictionary
    fin_max = max(last_value_dictionary, key=last_value_dictionary.get)
    value_max = last_value_dictionary[fin_max]
    print("##### Last value #### ")
    print("Max value index", fin_max)
    print("max value", last_value_dictionary[fin_max])
    print('max value std', last_std_value_dictionary[fin_max])
    print("max test value", last_test_value_dictionary[fin_max])
    print('#########')
    print('##### last 30 values ')
    max_30 = max(last_30, key=last_30.get)
    print("Max value index", max_30)
    print("max value", last_30[max_30])
    print('max value std', last_std_value_dictionary[max_30])
    print("max test value", last_test_value_dictionary[max_30])
    print('#########')
    print('##### biggest values ')
    max_big = max(last_max, key=last_max.get)
    print("Max value index", max_big)
    print("max value", last_max[max_big])
    print('max value std', last_std_value_dictionary[max_big])
    print("max test value", last_test_value_dictionary[max_big])
    print('#########')


    print("Finding any duplicate entries")


    # ########### finding duplicate values ##################
    # ########### from dictionary using set
    rev_dict = {}
    for key, value in last_value_dictionary.items():
        rev_dict.setdefault(value, set()).add(key)

    
    
# to get the values that are associated with each duplicate, i simply enter the value, 
# since I have the max value, 
    config_array = []
    duplicate_entries = rev_dict[value_max]# these are a set 
    print('Duplicate entries', duplicate_entries)

    for i in duplicate_entries:
        config_array.append(extract_configs(path_to_hyperparameter_search, i))

    ###################### This copies the best run configs and outputs them as a config #######

    duplicate_entries = list(duplicate_entries)
   

    full_list = duplicate_entries 
    print(full_list)

    load_config = extract_configs(path_to_hyperparameter_search, fin_max)

    pp = pprint.PrettyPrinter(indent=4)
    # ddif = DeepDiff(config_array[0], config_array[2])
    # print('Root', duplicate_entries[0], 'new value', duplicate_entries[1])
    # pp.pprint(ddif)
    # pp.pprint(type(ddif))



    ################### go through the duplicates and compare them ##################
    # for j in range(len(duplicate_entries)):
    #     print('j', duplicate_entries[j])
    #     for i in range(len(duplicate_entries)): 
    #         # print('i',i)
    #         dif = DeepDiff(config_array[j], config_array[i]) 
    #         if not dif: 
    #             print(duplicate_entries[j],duplicate_entries[i], ' are the same' )
    #         print('Root', duplicate_entries[j], 'compare', duplicate_entries[i])
    #         pp.pprint(dif)

    for j in range(len(full_list)):
        print('j', full_list[j])
        for i in range(len(full_list)): 
            # print('i',i)
            dif = DeepDiff(config_array[j], config_array[i]) 
            if not dif: 
                print(full_list[j],full_list[i], ' are the same' )
            # print('Root', full_list[j], 'compare', full_list[i])
            # pp.pprint(dif.affected_root_keys)
    
    
    
    # # fin_max is the directory number, now you can get the hyperparameters for it:
    # path_to_config = path_to_hyperparameter_search + '\\' + str(fin_max) + '\\' + 'config.json'
    # # path_to_config = path_to_second_hs_search + '\\' + str(fin_max) + '\\' + 'config.json'    
    # with open(path_to_config) as f: 
    #     load_config = json.load(f)
        
    ##################################### This section modifies the new config ######################
    # modify the config name to make it different than the original 
    # load_config['name'] = algo + '_lbf_coop_best'
    # # to turn the hyperparameter config, i simply need to call this 

    # # Dump the config 
    # with open( algo + '_coop_best.config.yaml', 'w+') as file: 
    #     file.write(yaml.dump(load_config))


if __name__ == '__main__':

    __main()

