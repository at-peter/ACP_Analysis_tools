import sys
import json
import yaml

'''
Created Nov 20 2022 
Made to fix a problem i created for myself by dumpting to json rather than to yaml
'''

# THIS opens the config

def create_json_configs(list_of_configs, folder_path, alg):
    for i, e in enumerate(list_of_configs):
        path = folder_path + '/' + str(e) + '/config.json'
        json_data = json.load(open(path))
        #### set the name
        name = alg + '_best_conf_' + str(i)
        json_data['name'] = name
        #### get rid of the seed value
        del json_data['seed']
        yaml_name = name + '.yaml'
        with open(yaml_name, 'w') as file:
            yaml.dump(json_data, file)
            print('dump complete :)')

def compare_hyperparameters():
    print('not done yet')


def __main():
    list_of_configs = [
        # IQL confs
        # '142',
        # '225' - this one 

        # Ippo confs:
        # 193,
        # 98, -this one 
        # 112

        #QMIX confs:
        # 211,
        # 338 - this one 

        #IA2C confs:
        # 87,
        # 55 - this one 

        #VDN confs:
        # 71,
        # 118 - this one 

        # # MAPPO conf:
        # 203 #this one 
        
        #M
    ] 

    folder_path = "C:/Users/Wintermute/Desktop/hyperparameter search 10x10/mappo_10x10_hs"
    alg = 'mappo'
    create_json_configs(list_of_configs,folder_path,alg)


if __name__ == '__main__':
    __main()
#
#
# # for i, e in enumerate(list_of_configs):
# #     the_path = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/vdn/vdn_8x8_hs_2/' + e + '/vdn_best_config_' + \
# #                str(i) + '.json'
# # my_path = "C:/source/atpeterepymarl/src/results/qtran_regular_hs/206/qtran_best_config_4.json"
# my_path = "C:/Users/Wintermute/Desktop/hyperparameter search 10x10/iql_10x10_hs/142/"
#
# json_name = my_path.split('/')[-1]
# name = json_name.split('.')[0]
# yaml_name = name + '.yaml'
#
# #### change the name to match the name of the config for easy sorting later ####
# json_data = json.load(open(my_path))
# json_data['name'] = name
#
# #### get rid of the seed value
# del json_data['seed']
#
# ##### print the hyperparameters:
# # FIXME: December 9 2022 These are not w
# hyperparameters = [
#     'hidden dimension',
#     'learning rate ',
#     'reward standardisation ',
#     'network type ',
#     'entropy coefficient',
#     'evaluation epsilon ',
#     'epsilon anneal ',
#     'target update ',
#     'n-step',
#     'q_nstep'
# ]
#
# config_hyperparameters = [
#     'hidden_dim',
#     'lr',
#     'standardise_rewards',
#     'use_rnn',
#     'entropy_coef',
#     'evaluation_epsilon',
#     'epsilon_anneal_time',
#     'target_update_interval_or_tau',
#     'q_nstep'
# ]
#
# for i , hyperparameter in enumerate(hyperparameters):
#     # print(i, hyperparameter)
#     try:
#         if json_data[config_hyperparameters[i]]:
#             print(hyperparameter, json_data[config_hyperparameters[i]])
#     except:
#         print('hyperparameter', hyperparameter, ' is not included in the config')
#         pass
#
#     # if json_data[config_hyperparameters[i]]:
#     #     print(hyperparameter, json_data[config_hyperparameters[i]])
#
#
#
# with open(yaml_name, 'w') as file:
#     yaml.dump(json_data, file)
#     print('dump complete :)')
