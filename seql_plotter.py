from matplotlib import pyplot as plt
import argparse 
import csv
import numpy as np 
# parser = argparse.ArgumentParser("Lets do some plottingggggg!")
# parser.add_argument('--file', type=str, help="File that you want to plot")
# parser.add_argument('--players', type=int, help="number of players in the game", default=2)
rows = []
fields = []
returns = []

path = 'C:/source/seac/seql/logs/8x8_2p_2f_coop/iql_Foraging-8x8-2p-2f-coop-v1_epinfo_final.csv'
players=2


for player in range(players):
    name = 'returns_' + str(player)
    exec("%s = list()" % name) 

# def open_file(path):
#     with open(path, 'r') as csvfile:
#         csvreader = csv.reader(csvfile)
#         fields = next(csvreader)
#         for rows in csvreader



if __name__ == "__main__":
    # args = parser.parse_args()
    # path = args.file
    # print(type(path))
    #open the file and get the data
    with open(path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        print(fields)
        for rows in csvreader:
            #TODO: need to split the returns here per player
            for player in range(players):
                returns = rows[1]
                re1 = returns.replace(']','').replace('[','')
                returns = re1.replace("'",'').split(" ")
                exec('returns_%s.append(float(returns[%d]))' %(player, player))
            # returns.append(rows[1])
    
    
   
  
    ## IQR calculation 
    q75, q25 = np.percentile(returns_0, [75,25])
    iqr0=q75-q25
    q75, q25 = np.percentile(returns_1, [75,25])
    iqr1=q75-q25

    print('IQR 0', iqr0)
    print('IQR 1', iqr1)

    #plot the returns 
    x =[]
    for i in range(len(returns_0)):
        x.append(i*50)
    
    plt.plot(x, returns_0, alpha=0.666)
    plt.plot(x, returns_1, alpha=0.666)
    plt.legend(["agent1","agent2"])
    plt.title("8x8_2p_2f_coop episode returns")
    plt.ylabel('Return value')
    plt.xlabel('50 episode intervals')
    plt.show()
        # the first field is the episode number 
        # the second field is the returns