

import numpy as np


from functions import  readingFile,minimumSupport,get__allItems_with_first_count,getFrequentData, remove_infrequent_items_from_dataset,getGlobalTree,findChild, sub_sets,findFrequentItems
import sys, time






class FPgrowth:
    Start =  time.time()

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
   
    # Build the golbal tree for us where it starts from the empty node which is the root and then add nodes if they do not exist
    globalTree =  getGlobalTree(orderedTransactions)
    
    condtionalDictionary = dict()
    
   

    for item in reversed(frequentItemSet):
        index =0

        ourDictionary=dict()
      
        condtionalPath,conditionalCount=findChild(item,globalTree,[],[],[])

        for arrayValue in condtionalPath:

            for value in arrayValue:
                if value in ourDictionary:
                    ourDictionary[value] = ourDictionary[value] +conditionalCount[index]
                else:
                    ourDictionary.update({value:conditionalCount[index]})


            index = index+1
        
        if item in ourDictionary:
            del ourDictionary[item]
       
        if len(ourDictionary)!=0:
           
            for key, value in dict(ourDictionary).items():
                if value < threshold:
                    del ourDictionary[key]
            condtionalDictionary.update({item:ourDictionary})
   

    myJoinedCondtionalyArray = list()
    for value in reversed(frequentItemSet.keys()):
        myJoinedCondtionalyArray.append(value)
   
    array =[]


    
    arrayOfFrequentItem =[]
    for valueKey in condtionalDictionary:
      
        array =[]
     
        for value in condtionalDictionary[valueKey].keys():
            array.append(value)
     
        result =  sub_sets(array)
        result = list(filter(None, result))
     
        index = 0
        
        for unorderedArray in result:
            result[index] = unorderedArray + [valueKey]
            
            result[index]=sorted(result[index],key=myJoinedCondtionalyArray.index)
            
            FrequentItemsFound= findFrequentItems(result[index],orderedTransactions,threshold)
            if(FrequentItemsFound!= None):
                arrayOfFrequentItem.append(FrequentItemsFound)


            index =index+1
    # print(arrayOfFrequentItem)
    # print(myJoinedCondtionalyArray)
    print('|FPS|',len(arrayOfFrequentItem) +len(myJoinedCondtionalyArray) ) 
    end =  time.time()
    print(end-Start)
    from contextlib import redirect_stdout
    with open('MiningResult.txt', 'w') as f:
        with redirect_stdout(f):
            print('|FPS|:',len(arrayOfFrequentItem) +len(myJoinedCondtionalyArray))
            for itemset in myJoinedCondtionalyArray:
                print([itemset])
            for joinedItemsets in arrayOfFrequentItem:
                print(joinedItemsets)
            
    

            
                

