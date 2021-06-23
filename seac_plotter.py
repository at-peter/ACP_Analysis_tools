import json
import numpy as np 
from matplotlib import pyplot as plt
from pprint import pprint
import pandas as pd
from pathlib import Path
import seaborn as sns

path = Path("C:/source/seac/seac/results/sacred/15/metrics.json")
# FIXME: coop envs dont save agent rewards, only the total sum of all in the episode_reward query
with open(path) as f:
    Loaded_dict = json.load(f)
print(Loaded_dict.keys())

def open_file(path):
    with open(path) as f:
        loaded_dictionary = json.load()
    return loaded_dictionary

def transform_dataframe(loaded_dictionary, num_agents):
   
    dataframe_list = []
    for agent in range(num_agents):
        query_str = 'agent'+str(agent)+'/episode_reward'
        extracted_data = loaded_dictionary[query_str]['values']
        dataframe_list.append(pd.DataFrame(extracted_data, columns=[query_str]))
        # if agent == range(num_agents)[-1]:
        #     print(dataframe_list)
        #     extracted_data = loaded_dictionary[query_str]["steps"]
        #     dataframe_list.append(pd.DataFrame(extracted_data, columns=['steps']))
    
    # print(dataframe_list)
    output_frame = pd.concat(dataframe_list,axis=1) 
    return output_frame

def plot(data , metric):
    x = range(len(data[metric]['values']))
    y = data[metric]['values']
    # pprint(data[metric]['values'])
    plt.plot(x, y)
    plt.title(metric)
    # plt.show()


def plot_many_agents(data, metric, num_agents):
    for agent in range(num_agents):
        query_str = 'agent'+str(agent)+'/'+metric
        extracted_data = data[query_str]['values']
        x = range(len(data[metric]['values']))
        plt.plot(x, extracted_data ,label="agent "+str(agent))
    plt.title(str(num_agents)+" agent " + metric)
    plt.xlabel('episodes')
    plt.ylabel('return')
    plt.legend()
    # plt.show()

if __name__ == '__main__':
    sns.set_theme(style='darkgrid')
    data = transform_dataframe(Loaded_dict,2)
    # interquartile range calculation 
    # todo: make this into a function
    q75, q25 = np.percentile(data['agent0/episode_reward'], [75,25])
    iqr0=q75-q25
    q75, q25 = np.percentile(data['agent1/episode_reward'], [75,25])
    iqr1=q75-q25

    print('IQR 0', iqr0)
    print('IQR 1', iqr1)
    # print(data.head(2))
    # sns.distplot(data)
    # data = data.rolling(7).mean()
    sns.lineplot(data=data, palette='tab10')
    plt.title('Episode rewards for 10x10 2p 8f env and SEAC alg')
    plt.ylabel('reward')
    plt.xlabel('2000 timestep intervals')
    plt.show()
    # plt.figure(0)
    # plot(Loaded_dict,'episode_reward')
    # plt.figure(1)
    # plot_many_agents(Loaded_dict,'episode_reward',2)
    # plt.show()