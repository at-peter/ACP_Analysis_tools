import sys
import json
import yaml

'''
Created Nov 20 2022 
Made to fix a problem i created for myself by dumpting to json rather than to yaml
'''
my_path = "C:/Users/Wintermute/Desktop/hyperparameter search 8x8/maa2c/maa2c_8x8_hs_2/434/maa2c_best_config_2.json"


print(yaml.dump(json.load(open(my_path))))