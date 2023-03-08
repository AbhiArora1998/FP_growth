import time
import numpy as np
import sys

from functions import readingFile, minimumSupport,get__allItems_with_first_count,get_L_and_itemCount_and_discarded_items,combineItems

class Apriori: 
    
    initialiZations=sys.argv
    fileName = initialiZations[1]
    initalPercentage = int(initialiZations[2])
    Transactions = list()
    candidate,large,discarded_transactions,supportCount=dict(),dict(),dict(),dict()
    totalSize=1
    print('hello I am alive')
    print('Please wait...')
    # reading the trasactions
    Transactions,totalRows=readingFile(fileName)
    
    #  counting the minimum threshold 
    threshold = minimumSupport(totalRows,initalPercentage)
    print('Minimum_Support',threshold)
    begin = time.time()

    # received all the unique transactions
    asc = sorted(get__allItems_with_first_count(Transactions),key=int)
    # print(sortedOrder)
    candidate.update({1 : [[item] for item in asc] })
    discarded_transactions.update({1:list()})


    # Check and count the values for itesm the first time
    # [1]
    receivedL,receiveditemCount,receivedDiscarededValue  =  get_L_and_itemCount_and_discarded_items(candidate[1],Transactions,threshold,discarded_transactions)
    # updaing the dictionary for the first time
    large.update({1:receivedL})
    supportCount.update({1:receiveditemCount})
    discarded_transactions.update({1:receivedDiscarededValue})
   
    totalSize = 1 + totalSize
    noMoreItems = False
    """
        The main loop of the file where we find all the item sets starting from L2, C2 to end of the dictionary
        This loop checks if the dictionary is empty 
        This loop also ends the time when the while loop ends
    """
    
    while noMoreItems ==False :
        print('Almost there :)')
        joinedSet = combineItems(large[totalSize-1],asc)
        candidate.update({totalSize:joinedSet})
        receivedL,receiveditemCount,receivedDiscarededValue = get_L_and_itemCount_and_discarded_items(candidate[totalSize],Transactions,threshold,discarded_transactions)
        if len(receivedL) <1:
            noMoreItems = True
            print('Thanks for your patience\n')
            break
        else: 
            large.update({totalSize:receivedL})
            supportCount.update({totalSize:receiveditemCount})
            discarded_transactions.update({totalSize:receivedDiscarededValue})
            totalSize = totalSize+1 
            
    totalSize = 0   
    
    end = time.time()
    print('Total RunTime', end-begin,"seconds")
    for index in range(1, len(large.keys())+1):
                totalSize = totalSize + len(large[index])
    print('|FPS|:',totalSize)
    
    """
        Opening the file to print the final output of the mining process of apriori 
        The result gets printed in the txt file name MiningResult.txt
    """
    from contextlib import redirect_stdout
    with open('MiningResult.txt', 'w') as f:
        with redirect_stdout(f):
            print('|FPS|:',totalSize)
            for index in range(1, len(large.keys())+1):
                for values in range(0,len(large[index])):
                    print(large[index][values],":",supportCount[index][values])
                

             



    
