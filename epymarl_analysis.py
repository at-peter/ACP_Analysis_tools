import numpy
import seaborn as sns
import pandas 
from matplotlib import pyplot
from epymarl_plotter import open_file


def convergence_analysis(path):
    '''
    This method grabs the last value from each of the 30 runs and performs analysis on it. 
    values that need to be grabed are the training values and the testing values 

    '''

    return final_training_values, final_test_values

if __name__ == "__main__":
    '''
    This code is the code that checks if the final value of the training and testing return means are above 0.9
    '''
    sns.set_theme(style='darkgrid')
    base_path = 'C:/source/atpeterepymarl/src/results/sacred/' 
    # path = 'C:/source/atpeterepymarl/src/results/sacred/171/metrics.json'

    # data = open_file(path)
    # print(data.keys())
    
#    start_index = 

    final_test_values = []
    final_training_values = []
    test_above_cutoff = 0 
    training_above_cutoff = 0

    experiment_list = range(242,252)
    for _ , experiment in enumerate(experiment_list):
        path = base_path + str(experiment) + '/metrics.json'
        data = open_file(path)
        final_test_values.append(data['test_return_mean']['values'][-1])
        if data['test_return_mean']['values'][-1] >= 0.9:
            test_above_cutoff += 1 
        final_training_values.append(data['return_mean']['values'][-1])
        if data['return_mean']['values'][-1] >= 0.9:
            training_above_cutoff += 1 

    print("test above 0.9", test_above_cutoff)
    print("training above 0.9", training_above_cutoff)
    
    x_test = range(len(final_test_values))
    x_training = range(len(final_training_values))
    test_cutoff = [0.9]*len(x_test)
    training_cutoff = [0.9]*len(x_training)

    pyplot.figure(0)
    pyplot.plot(x_test, final_test_values)
    pyplot.plot(x_test, test_cutoff)
    pyplot.title('test')
    
    
    pyplot.figure(1)
    pyplot.plot(x_training, final_training_values,'-x')
    pyplot.plot(x_training, training_cutoff)
    pyplot.title('Final training episode means Qmix 9x9-2p-3f, max timesteps 50')
    pyplot.xlabel('runs')
    pyplot.ylabel('final episode mean return')
    pyplot.show()

    



