
def sub_sets(sset):
        return subsetsRecur([], sorted(sset))
    
def subsetsRecur( current, sset):
        if sset:
            return subsetsRecur(current, sset[1:]) + subsetsRecur(current + [sset[0]], sset[1:])
        return [current]

class Node:
    def __init__(self, count,word):
        self.count = count
        self.word = word
        self.children = dict()

def findFrequentItems(array,parent,threshold):
    count = 0;
    for Box in parent:
       
        if(set(array).issubset(set(Box))):
            count = count+1
        
    if count>= threshold:
       
        return array
    


def findChild(item,parent,returningList,conditionalPath,conditionalCount):
        
        
        if parent.word !="Empty":
            returningList = (returningList + [parent.word])
        if parent.word == item:
            conditionalPath.append(returningList)
            conditionalCount.append(parent.count)
            return conditionalPath , conditionalCount
        else:
            # This means that parent has children
            if len(parent.children) !=0:
                for child in parent.children:
                    FoundItem, FoundCount = findChild(item, parent.children[child],returningList,conditionalPath,conditionalCount)
                return conditionalPath,conditionalCount                   
            return conditionalPath, conditionalCount



class LinkedList:
    def __init__(self):
        self.parent =None


def remove_infrequent_items_from_dataset(Transactions,frequentItemSet):
    tempCopy = []
    for value in Transactions:
        test=list(set (value) - set (list(frequentItemSet.keys())))
        if len(test) != 0: 
            test =  list( set(value)-set(test))
            test = [*set(test)]
            tempCopy.append(test)
        else:
            test = [*set(test)]

            tempCopy.append(value)
        
    return tempCopy

def getFrequentData(L,threshold):
    aboveThreshold = L.copy()
    for value in aboveThreshold:      
        if aboveThreshold[value] < threshold:
            L.pop(value)    
    
    return L


def getGlobalTree(orderedTransactions):
    # import copy
    parent = LinkedList()
    root = Node(1,'Empty')
    
    index = 0
    for box in  orderedTransactions:
        
        
        parent = root
        for item in box: 
           
                
             
                if len(parent.children) == 0:
                
                    newNode = Node(1,item)

                    dictValue = {item:newNode}
                    parent.children.update(dictValue)
                                

                    

                    parent = newNode
                  
                    
                else:
                   

                    for child in parent.children:
                        childExist = False
                       
                        if item == child:
                          
                            parent.children[child].count=parent.children[child].count+1
                           

                            parent =parent.children[child]
                            childExist = True
                            break
                    
                    if not childExist:
                        
                        anotherNode = Node(1,item)

                      
                        anotherdictValue = {item:anotherNode}
                        parent.children.update(anotherdictValue)
                        parent = anotherNode
                        
    return root

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
            
        


# globalTree = []
    # tempTree=[]
    # for itemArray in orderedTransactions:
        
    #     if len(tempTree)==0:
    #         initialValue =dict(Counter(itemArray))
    #         tempTree.append(initialValue)
    #         globalTree.append(initialValue)
    #     else:
    #         index = 0
    #         alreadyExist =False
    #         for treeValue in tempTree:
                
    #             if itemArray[0] in treeValue.keys():
    #                 print(index,'found')
    #                 tempValue=Counter(itemArray)
    #                 globalTree[index]=dict(Counter(globalTree[index]) + tempValue)
    #                 print(globalTree[index])
    #                 alreadyExist = True
    #                 break
    #             index = index+1
    #         if alreadyExist == False:
    #             temp = dict(Counter(itemArray))
    #             tempTree.append(temp)
    #             globalTree.append(temp)
    # print(globalTree)


    # def findChild(item,parent):
    #     conditionalPath = []
    #     conditionalCount = []
    #     # print(parent.word,'I am the parent now')
    #     if parent.word  != item:
    #        # If the parent is not equal to the item then we wanna go down to look if children exist 
    #        if len(parent.children)!=0:
    #         #    print(parent.word,'has children',parent.children)
    #            middlePath= []
    #            middlecount= []

    #            for child in parent.children:
                    
    #                 foundItem,count=findChild(item,parent.children[child])
    #                 middlePath.append(parent.word)
    #                 # print(foundItem,count,'goingTO')
    #                 if parent.word != 'Empty':
    #                     if len(foundItem)!=0:
    #                         # print([parent.word],count,'here')
                            
    #                         # print(foundItem + [parent.word],count,'where')
    #                         savedValue=(foundItem + [parent.word]),count

    #                         middlePath.append(savedValue)
    #                         middlecount.append(count)

    #                     # print(middlePath,"did we find something")
    #                 else:
    #                     print('we are back at the emptyParent',foundItem,count)
    #                     # print(foundItem,count)
    #                     if len(foundItem)!=0:
    #                         # print(foundItem)
    #                         conditionalPath.append(foundItem)
    #                     if len(count)!=0:
    #                         # print('we are going in')
    #                         conditionalCount.append(count)
    #                     # print('we are back at the emptyParent',conditionalPath,conditionalCount)
    #         #    print(conditionalPath, conditionalCount,'should be returing now') 
    #            return conditionalPath, conditionalCount
    #        else:
    #         #    print(parent.word,'no child exist for this one this also means we did not find any child')
    #            return [],[]
    #     else:
    #         print([parent.word],[parent.count],'here')
    #         return [parent.word],[parent.count]