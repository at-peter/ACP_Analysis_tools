import json
import numpy as np 
from matplotlib import pyplot as plt
from pprint import pprint
import pandas as pd
from pathlib import Path
import seaborn as sns





# with open(path) as f:
#     Loaded_dict = json.load(f)
# print(Loaded_dict.keys())

def open_file(directory_path, file_name):
    path = directory_path + file_name
    path = Path(path)
    with open(path) as f:
        loaded_dictionary = json.load(f)
    return loaded_dictionary

def extract_config_data(config_dict):

    name = config_dict['env_name']
    num_agents = name.split('-')[2]
    num_agents = int(num_agents[0])
    return name, num_agents


def transform_dataframe(loaded_dictionary, num_agents):
   
    dataframe_list = []
    #this is for agent plotting data
    for agent in range(num_agents):
        query_str = 'agent'+str(agent)+'/episode_reward'
        extracted_data = loaded_dictionary[query_str]['values']
        dataframe_list.append(pd.DataFrame(extracted_data, columns=[query_str]))
        if agent == range(num_agents)[-1]:
            # Get the steps
            extracted_data = loaded_dictionary[query_str]["steps"]
            dataframe_list.append(pd.DataFrame(extracted_data, columns=['steps']))
    

    # append the dataframe for the episode rewards:
    dataframe_list.append(pd.DataFrame(loaded_dictionary['episode_reward']['values'],
                                       columns=['episode_reward']))
    output_frame = pd.concat(dataframe_list, axis=1)
    # steps steps as the index for the Dataframe
    output_frame.set_index('steps', inplace=True)
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


def calculate_iqr(dataframe, num_agents):
    iqr = []
    # extract the IQR values
    for agent in range(num_agents):
        query = 'agent' + str(agent) + '/episode_reward'
        q75, q25 = np.percentile(dataframe[query], [75, 25])
        iqr.append(q75 - q25)
    # print to the screen

    # save the values to a txt file
    return iqr


def save_values(values, name, save_path):
    write_values =["%s\n" % value for value in values]
    filename = save_path.joinpath(name + '.txt')

    with open(filename, 'a') as file:
        file.write('------\n')
        file.writelines(write_values)

    return 1


def analyze_many(directory_values):

    for i in range(1,17):
        metrics_save_path = Path("D:/acp_data/metrics/")
        plots_save_path = Path("D:/acp_data/plots/")

        directory_path = 'C:/Users/Peter/Documents/source/repos/acp/seac/results/sacred/' + str(i) +'/'
        metrics_data = open_file(directory_path,'metrics.json')
        config_data = open_file(directory_path, 'config.json')

        name, num = extract_config_data(config_data)

        data = transform_dataframe(metrics_data, num)
        # interquartile range calculation
        # todo: make this into a function

        iqr =calculate_iqr(data, num)
        save_values(iqr,name,metrics_save_path)


        # for i, val in enumerate(iqr):
        #     print('IQR agent ' + str(i) + ' ' + str(val))


        plt.figure(0)
        title = 'total rewards for '+ name +' SEAC alg'
        # sns.lineplot(data=data, palette='tab10', alpha=0.35)
        sns.lineplot(data=data, x='steps', y='episode_reward')
        plt.title(title)
        plt.ylabel('reward')
        plt.xlabel('Episode intervals')
        file_name = title.replace(' ', '_')
        plt.savefig(plots_save_path.joinpath(file_name + '.jpg'), dpi=200)

def analyze_total(directory_number):
    directory_path = 'D:/acp_data/data_from_Atlas/seac/sacred/' + str(directory_number) + '/'
    metrics_data = open_file(directory_path,"metrics.json")
    config_data = open_file(directory_path, 'config.json')

    check_list = np.array(metrics_data['episode_reward']['values'])
    nonzero_index = list(np.nonzero(check_list)[0])

    name, num = extract_config_data(config_data)
    data = transform_dataframe(metrics_data, num)
    plt.figure(0)
    sns.lineplot(data=data, x='steps', y='episode_reward')
    title = 'total rewards for ' + name + ' SEAC alg'
    plt.title(title)
    plt.ylabel('reward')
    plt.xlabel('update intervals')
    plt.show()
if __name__ == '__main__':
    sns.set_theme(style='darkgrid')
    analyze_total(13)
    # directory_path = "C:/Users/Peter/Documents/source/repos/acp/seac/results/sacred/4/"




    # plt.figure(1)
    # title = 'Episode rewards for 16x16 4p 6f env and SEAC alg'
    # sns.lineplot(data=data, x='steps', y='episode_reward')
    # plt.show()

    # plt.figure(0)
    # plot(Loaded_dict,'episode_reward')
    # plt.figure(1)
    # plot_many_agents(Loaded_dict,'episode_reward',2)
    # plt.show()