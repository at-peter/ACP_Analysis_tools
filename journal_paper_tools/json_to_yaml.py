import sys
import json
import yaml

'''
Created Nov 20 2022 
Made to fix a problem i created for myself by dumpting to json rather than to yaml
'''

list_of_configs = [
    '100',
    '263',
    '554',
    '149'
]

# for i, e in enumerate(list_of_configs):
#     the_path = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/vdn/vdn_8x8_hs_2/' + e + '/vdn_best_config_' + \
#                str(i) + '.json'
# my_path = "C:/source/atpeterepymarl/src/results/qtran_regular_hs/206/qtran_best_config_4.json"
my_path = "C:/Users/Wintermute/Desktop/hyperparameter search 8x8/ippo/ippo_8x8_hs_2/80/ippo_best_8.json"

json_name = my_path.split('/')[-1]
name = json_name.split('.')[0]
yaml_name = name + '.yaml'

#### change the name to match the name of the config for easy sorting later ####
json_data = json.load(open(my_path))
json_data['name'] = name

#### get rid of the seed value
del json_data['seed']

##### print the hyperparameters:

hyperparameters = [
    'hidden dimension',
    'learning rate ',
    'reward standardisation ',
    'network type ',
    'entropy coefficient',
    'evaluation epsilon ',
    'epsilon anneal ',
    'target update ',
    'n-step',
    'q_nstep'
]

config_hyperparameters = [
    'hidden_dim',
    'lr',
    'standardise_rewards',
    'use_rnn',
    'entropy_coef',
    'evaluation_epsilon',
    'epsilon_anneal_time',
    'target_update_interval_or_tau',
    'q_nstep'
]

for i , hyperparameter in enumerate(hyperparameters):
    # print(i, hyperparameter)
    try:
        if json_data[config_hyperparameters[i]]:
            print(hyperparameter, json_data[config_hyperparameters[i]])
    except:
        print('hyperparameter', hyperparameter, ' is not included in the config')
        pass

    # if json_data[config_hyperparameters[i]]:
    #     print(hyperparameter, json_data[config_hyperparameters[i]])



with open(yaml_name, 'w') as file:
    yaml.dump(json_data, file)
    print('dump complete :)')
