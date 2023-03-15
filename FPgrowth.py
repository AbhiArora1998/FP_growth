
from audioop import reverse
from unittest import result
import numpy as np


from functions import combineItems, readingFile,minimumSupport,get__allItems_with_first_count,getFrequentData, remove_infrequent_items_from_dataset,getGlobalTree,findChild, sub_sets
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
   #  print(order,'ore')
    
    # order the transactions according to the frequent order of dataset
    for listVale in Transactions:
    #    print(listVale)
       orderedTransactions.append(sorted(listVale,key=order.index))
    # print(orderedTransactions)
    # print(frequentItemSet)
    # print(list(frequentItemSet.keys()))
    # Build the golbal tree for us where it starts from the empty node which is the root and then add nodes if they do not exist
    globalTree =  getGlobalTree(orderedTransactions)
    condtionalDictionary = dict()
    print(frequentItemSet)
    print(globalTree.word,globalTree.children,'global')
   #  print(globalTree.children['2'].children['5'].children['3'].children,'herer')
    
   
   #  FoundItem, FoundCount=findChild('1',globalTree,[],[],[])
   #  print(FoundItem, FoundCount,'here')
   # #  print(FoundItem,FoundCount)

    for item in reversed(frequentItemSet):
        index =0

        ourDictionary=dict()
        # print(item)
        condtionalPath,conditionalCount=findChild(item,globalTree,[],[],[])

        # print(condtionalPath,conditionalCount,'here')
        for arrayValue in condtionalPath:

            for value in arrayValue:
                if value in ourDictionary:
                    ourDictionary[value] = ourDictionary[value] +conditionalCount[index]
                else:
                    ourDictionary.update({value:conditionalCount[index]})


            index = index+1
        # print(ourDictionary)
        if item in ourDictionary:
            del ourDictionary[item]
        # print(ourDictionary)
        if len(ourDictionary)!=0:
            # print(ourDictionary)
            for key, value in dict(ourDictionary).items():
                if value < threshold:
                    del ourDictionary[key]
            condtionalDictionary.update({item:ourDictionary})
    # print(condtionalDictionary)
    # print(frequentItemSet)

    myJoinedCondtionalyArray = list()
    for value in reversed(frequentItemSet.keys()):
        myJoinedCondtionalyArray.append(value)
    print(myJoinedCondtionalyArray)
    array =[]


    

    for valueKey in condtionalDictionary:
        print(valueKey,'hr')
        array =[]
        # print(condtionalDictionary[value].keys())
        for value in condtionalDictionary[valueKey].keys():
            array.append(value)
        # print(array,order)
        result =  sub_sets(array)
        result = list(filter(None, result))
        # result=combineItems(myJoinedCondtionalyArray,order)
        index = 0

        for unorderedArray in result:
            result[index] = unorderedArray + [valueKey]
            
            result[index]=sorted(result[index],key=myJoinedCondtionalyArray.index)
            
            index =index+1
        print(result)
    
    
            
    

            
                

