from functions import  readingFile,minimumSupport,get__allItems_with_first_count,getFrequentData, remove_infrequent_items_from_dataset,getGlobalTree,findChild, getMySubsets,findFrequentItems
import sys, time
class FPgrowth:
    #  Starting the time
    Start =  time.time()
    #  takes the value from the command prompt
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
    # received all the unique transactions
    candidates = get__allItems_with_first_count(Transactions)
    order = list(candidates.keys())
    orderedTransactions = list()
    # this sort out the transactions according to the order we specified for our frequent data 
    # And also gives us frequent data which is the first table 
    frequentItemSet =getFrequentData(candidates, threshold)
    # removes the infrequent items from the dataset
    Transactions = remove_infrequent_items_from_dataset(Transactions,frequentItemSet)
    # order the transactions according to the frequent order of dataset
    for listVale in Transactions:
       orderedTransactions.append(sorted(listVale,key=order.index))
    # Build the golbal tree for us where it starts from the empty node which is the root and then add nodes if they do not exist
    globalTree =  getGlobalTree(orderedTransactions)
    condtionalDictionary = dict()
    # Goes through every item projection
    # and provide us all the items that was found associacted with the given projection 
    for item in reversed(frequentItemSet):
        print('Almost there please wait...')
        index =0
        ourDictionary=dict()
        # recursive calls for the projections
        condtionalPath,conditionalCount=findChild(item,globalTree,[],[],[])
        # Increase the counts for all the projections if same found in the other array
        for arrayValue in condtionalPath:
            for value in arrayValue:
                if value in ourDictionary:
                    ourDictionary[value] = ourDictionary[value] +conditionalCount[index]
                else:
                    ourDictionary.update({value:conditionalCount[index]})
            index = index+1
        # Delete the projection name from the result
        if item in ourDictionary:
            del ourDictionary[item]
        #  Remove the values that are below threshold 
        if len(ourDictionary)!=0:
            for key, value in dict(ourDictionary).items():
                if value < threshold:
                    del ourDictionary[key]
            condtionalDictionary.update({item:ourDictionary})
   
    myJoinedCondtionalyArray = list()
    #  Saves the final conditional jonied array
    for value in reversed(frequentItemSet.keys()):
        myJoinedCondtionalyArray.append(value)
   
    arrayOfFrequentItem =[]
    arrayOfFrequentItemCount = []
    # Loops through to remove all the empty array and values that are below threshold which was conunted in the previous for loop
    for valueKey in condtionalDictionary:  
        array =[]
        for value in condtionalDictionary[valueKey].keys():
            array.append(value)
        # Find the combinations for the projections
        result =  getMySubsets(array)
        result = list(filter(None, result))
        index = 0
        for unorderedArray in result:
            result[index] = unorderedArray + [valueKey]
            result[index]=sorted(result[index],key=myJoinedCondtionalyArray.index)
            FrequentItemsFound,FrequentItemsCountFound= findFrequentItems(result[index],orderedTransactions,threshold)
            if(FrequentItemsFound!= None):
                arrayOfFrequentItem.append(FrequentItemsFound)
                arrayOfFrequentItemCount.append(FrequentItemsCountFound)
            index =index+1
    
    # Prints the final length 
    print('|FPS|',len(arrayOfFrequentItem) +len(myJoinedCondtionalyArray) ) 
    end =  time.time()
    # Prints the time it takes to finish the code
    print("Total Run Time",end-Start)
    # Prints the result in the MiningResult.txt file
    from contextlib import redirect_stdout
    with open('MiningResult.txt', 'w') as f:
        with redirect_stdout(f):
            print('|FPS|:',len(arrayOfFrequentItem) +len(myJoinedCondtionalyArray))
            lastIndex = 0
            for itemset in myJoinedCondtionalyArray:
                print([itemset],"=",frequentItemSet[itemset])
            for joinedItemsets in arrayOfFrequentItem:
                print(joinedItemsets,"=",arrayOfFrequentItemCount[lastIndex])
                lastIndex = lastIndex+1
            
    

            
                

