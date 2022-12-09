import os

import pandas as pd
import json
import os
from matplotlib import pyplot as plt


def open_file(path):
    """
    This function opens the json in the path and returns it as a dictionary.
    It is used to open the config and metrics files.
    Param: path -> text
    return: loaded_dictionary -> dictionary of json
    """

    with open(path) as f:
        loaded_dictionary = json.load(f)
    return loaded_dictionary


def _main():

    value_array = []
    # main_path = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/ihateeverything/Foraging-10x10-3p-3f-v2/'
    main_path ="C:/source/atpeterepymarl/src/results/qtran_best_configs/Foraging-8x8-2p-2f-coop-v0/"
    os.chdir(main_path)
    dir_list = os.listdir()
    # list_of_paths = [main_path + '1']
    dataframes = {}
    name = main_path.split('/')[-2] + ' ' + main_path.split('/')[-3]
    for path in dir_list:
        metrics_path = path + '/metrics.json'
        # dataframes[path] = pd.read_json(metrics_path)
        # meow = pd.read_json(metrics_path)
        # print(meow.info())
        # print(meow.head())

        dataframes[path] = open_file(metrics_path)

    for i, dataframe in enumerate(dataframes):
       # grab the mean values
        value_array.append(dataframes[dataframe]['return_mean']['values'])
    plt.figure(1)
    for e,i in enumerate(value_array):
        print('Max value: ', max(i))
        x = range(len(i))
        plt.plot(x,i,label= e)
        plt.legend()
        plt.title(name)
    plt.show()


if __name__ == "__main__":
    _main()