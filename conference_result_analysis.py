import pandas as pd
import statistics

list_of_ia2c_paths = [
    'C:\source\workshop\ia2c_2s-8x8-2p-2f-coop\ia2c_2s-8x8-2p-2f-coop.csv',
    'C:\source\workshop\ia2c_8x8-2p-2f-coop\ia2c_8x8-2p-2f-coop.csv',
    'C:\source\workshop\ia2c_2s-10x10-3p-3f-v0\ia2c_2s-10x10-3p-3f-v0.csv',
    'C:\source\workshop\ia2c_10x10-3p-3f-v0\ia2c_10x10-3p-3f-v0.csv'
]

account = 'mappo'

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
    print("++++++++++++++++++++++")
    print(name)
    print('Mean of means', statistics.mean(means))
    print("Max results", max(maxs))
