import pandas as pd
import statistics
import scipy.stats as st


def calculate_ninefive_confidence(value_array):
    '''
    This function calculates the 95% confidence interval of an array using the T distribution. 
    It outputs the +- value 
    '''
    
    nine_five = st.t.interval(confidence=0.95,
    df=len(value_array)-1,
    loc=statistics.mean(value_array),
    scale=st.sem(value_array))
    interval = statistics.mean(value_array)- nine_five[0] 

    return interval


list_of_ia2c_paths = [
    'C:\source\workshop\ia2c_2s-8x8-2p-2f-coop\ia2c_2s-8x8-2p-2f-coop.csv',
    'C:\source\workshop\ia2c_8x8-2p-2f-coop\ia2c_8x8-2p-2f-coop.csv',
    'C:\source\workshop\ia2c_2s-10x10-3p-3f-v0\ia2c_2s-10x10-3p-3f-v0.csv',
    'C:\source\workshop\ia2c_10x10-3p-3f-v0\ia2c_10x10-3p-3f-v0.csv'
]

account = 'qmix'

list_of_paths = [
    'C:/source/workshop/' + account + '_2s-8x8-2p-2f-coop/' + account + '_2s-8x8-2p-2f-coop.csv',
    'C:/source/workshop/' + account + '_8x8-2p-2f-coop/' + account + '_8x8-2p-2f-coop.csv',
    'C:/source/workshop/' + account + '_2s-10x10-3p-3f-v0/' + account + '_2s-10x10-3p-3f-v0.csv',
    'C:/source/workshop/' + account + '_10x10-3p-3f-v0/' + account +'_10x10-3p-3f-v0.csv'
]

# path = 'C:/source/workshop/ia2c_8x8-2p-2f-coop/ia2c_8x8-2p-2f-coop.csv'
for path in list_of_paths:

    name = path.split('/')[-1]

    df = pd.read_csv(path)

    columns = list(df)

    means = []
    maxs = []


    for i, col in enumerate(columns):
        # print(df[col].mean())
        if i != 0:
            means.append(df[col].mean())

    for i, col in enumerate(columns):
        if i != 0:
            maxs.append(df[col].max())
        # print(df[col].max())
    
    mean_confidence = calculate_ninefive_confidence(means)
    max_confidence = calculate_ninefive_confidence(maxs)
    print("++++++++++++++++++++++")
    print(name)
    print('Mean of means', statistics.mean(means))
    print('Mean confidence interval',mean_confidence )
    print("Max results", max(maxs))
    print('Max confidence values', max_confidence)

