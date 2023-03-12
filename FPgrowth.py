
import numpy as np


from functions import readingFile,minimumSupport,get__allItems_with_first_count,getFrequentData, remove_infrequent_items_from_dataset,getGlobalTree,findChild
import sys, time






class FPgrowth:
    

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
    # begin = time.time()

    # received all the unique transactions
    candidates = get__allItems_with_first_count(Transactions)
    order = list(candidates.keys())
    
    orderedTransactions = list()
    # this sort out the transactions according to the order we specified for our frequent data
    frequentItemSet =getFrequentData(candidates, threshold)
    
    # removes the infrequent items from the dataset
    Transactions = remove_infrequent_items_from_dataset(Transactions,frequentItemSet)
    
    # order the transactions according to the frequent order of dataset
    for listVale in Transactions:
       orderedTransactions.append(sorted(listVale,key=order.index))
    # print(orderedTransactions)
    # print(frequentItemSet)
    # print(list(frequentItemSet.keys()))
    # Build the golbal tree for us where it starts from the empty node which is the root and then add nodes if they do not exist
    globalTree =  getGlobalTree(orderedTransactions)
    condtionalDictionary = dict()
    print(frequentItemSet)
    print(globalTree.word,globalTree.children,'global')
    print(globalTree.children['2'].children['5'].children['3'].children,'herer')

   

    # for item in reversed(frequentItemSet):
    #     index =0

    #     ourDictionary=dict()
    #     print(item)
    #     condtionalPath,conditionalCount=findChild(item,globalTree)

    #     print(condtionalPath,conditionalCount)
    #     for arrayValue in condtionalPath:

    #         for value in arrayValue:
    #             if value in ourDictionary:
    #                 ourDictionary[value] = ourDictionary[value] +conditionalCount[index][0]
    #             else:
    #                 ourDictionary.update({value:conditionalCount[index][0]})


    #         index = index+1
    #     if item in ourDictionary:
    #         del ourDictionary[item]
    #     # print(ourDictionary)
    #     if len(ourDictionary)!=0:
    #         # print(ourDictionary)
    #         # for key, value in dict(ourDictionary).items():
    #         #     if value < threshold:
    #         #         del ourDictionary[key]
    #         condtionalDictionary.update({item:ourDictionary})
    # print(condtionalDictionary)
            

            
                

