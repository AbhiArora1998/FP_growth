

def remove_infrequent_items_from_dataset(Transactions,frequentItemSet):
    tempCopy = []
    for value in Transactions:
        test=list(set (value) - set (list(frequentItemSet.keys())))
        if len(test) != 0: 
            test =  list( set(value)-set(test))
            tempCopy.append(test)
        else:
            tempCopy.append(value)
    return tempCopy

def getFrequentData(L,threshold):
    aboveThreshold = L.copy()
    for value in aboveThreshold:      
        if aboveThreshold[value] < threshold:
            L.pop(value)    
    return L


def getGlobalTree(orderedTransactions):
    from collections import Counter
    tempTree=[]
    for itemArray in orderedTransactions:
        
        if len(tempTree)==0:
            initialValue =dict(Counter(itemArray))
            tempTree.append(initialValue)
           
        else:
            index = 0
            alreadyExist =False
            for treeValue in tempTree:
                
                if itemArray[0] in treeValue.keys():
                    
                    tempValue=Counter(itemArray)
                    tempTree[index]=dict(Counter(tempTree[index]) + tempValue)
                    
                    alreadyExist = True
                    break
                index = index+1
            if alreadyExist == False:
                temp = dict(Counter(itemArray))
                tempTree.append(temp)
    return tempTree

"""
       Reading the file from the dataPath mentioned in the terminal 
       PreProcessing the file to start reading the file from items 
"""



def readingFile(dataPath):

    resultedFile= list()
    totalRows = 0
    with open(dataPath) as f: 
        lines = f.readlines()
    for line in lines: 
        if totalRows==0:
            totalRows=line
        else:  
            line = line.split("\t")
            updatedFile = line
            updatedFile = updatedFile[2]
            updatedFile = updatedFile.replace('\n','')
            updatedFile = updatedFile.split()
            resultedFile.append(updatedFile)
    return resultedFile, totalRows

"""
    Counting the minimum Threshold or support when user informs us with the percentage he/she would like
"""
def minimumSupport(totalRows,percentage):
    minimum_confidence_percent = percentage
    return (int(totalRows)*minimum_confidence_percent)/100

def isSubsetFunc(item1,item2):
    return set(item1).issubset(set(item2))



"""
    This is being used to count all the items uniquely for the first loop 
    This is being done to reduce the time complexity 
    All the values are being mapped and then are being counted using the library counter
"""
def get__allItems_with_first_count(Transactions):
    from collections import Counter
    totalRowsCounter=0
    totalItems = Counter()
   
    for line in Transactions:
        if totalRowsCounter==0:
            totalItems=(Counter(line))
        else:
            totalItems=(Counter(line)) + totalItems
        totalRowsCounter = totalRowsCounter+1
    
    totaldict=dict(totalItems)
    totalItems = list(totaldict.keys())
    respectiveCount = list(totaldict.values())
    # print(totaldict)
    totaldict=dict(sorted(totaldict.items(),key=lambda x:x[1],reverse=True))
    
    return totaldict
"""
        This counts the rest of the values by checking if the given item exist in the transactions
"""

def item_counter(singleItemSet, Transactions):
    incremente_count = 0
    for i in range(len(Transactions)):
        if isSubsetFunc(singleItemSet,Transactions[i]):
            incremente_count = incremente_count+1
    return incremente_count

"""
    This function checks finds all the items and checks if it subset of discarded items 
    If it is then ignore the items. Else count the amount of times it was repeated and send items back which are above threshold
    
"""

def get_L_and_itemCount_and_discarded_items(itemSet, initialTransactions, threshold,rejectValues):
    tempL,newDiscardedValue,itemCount = list(),list(),list()   
    for index in range(len(itemSet)):
        isDiscarded = -1
        value = itemSet[index]
        if len(rejectValues.keys()) > 0:
            for reject in rejectValues[len(rejectValues.keys())]:
                if isSubsetFunc(reject,value):
                    isDiscarded = 1
                    break
        if isDiscarded == -1:
            # [1]
            itemCounter = item_counter(value,initialTransactions)
            if itemCounter >= threshold:
                tempL.append(value)
                itemCount.append(itemCounter)
            else:
                newDiscardedValue.append(value)
    return tempL,itemCount,newDiscardedValue

"""
    This checks if the two items have anything in common neglect it 
    They are not and we have all the items sorted 
    therefore check if the last index is greater than the previous one 
    then join that item 
"""
def inner_combine_sets(firstItem,secondItem,sortedOrder):
    lastIndex = -1
    for index in range(len(firstItem)):
        # [1]
        if firstItem[index] == secondItem[index]:
            return list()
    if sortedOrder.index(firstItem[lastIndex]) < sortedOrder.index(secondItem[lastIndex]):    
            return firstItem + [secondItem[lastIndex]]

    return list()

"""
    if the length of combined result from the inner_combine_sets function is greater than one and is not already in our list 
    add it and otherwise ignore it 
"""
def combineItems(items,initialItem):
    temp = list()
    for index in range(len(items)-1):
        for innerIndex in range(index+1,len(items)):
            combinedResult = inner_combine_sets(items[index],items[innerIndex],initialItem)
            if len(combinedResult)>0 and combinedResult not in temp:
                temp.append(combinedResult)

    return temp
            
        