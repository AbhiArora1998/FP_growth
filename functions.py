"""
       This class gets initialsed every time we create a new node or object
       This contains a count to keep the count of item 
       Word to track of the word 
       and children which is a dictionary to keep count of all the childrens associated with this node
"""
class Node:
    def __init__(self, count,word):
        self.count = count
        self.word = word
        self.children = dict()

"""
       This is a recursive function allowing to traverse through the tree 
       This function helps provide all the projections of all the frequent items 
       This function append all the parent came accross and send it along with the count of the item we are searching for 
       It recursively traverse all the way down till it find the item we are looking for
"""
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


"""
       Creating a pointer name parent which allows to keep track of where we are in the global tree  
"""
class LinkedList:
    def __init__(self):
        self.parent =None

"""
       This funtion takes all the transactions taken from the dataset 
       then this function goes to the loop and remove all the items that are infrequent with the help of frequentItemset 
"""
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

"""
    This function takes the dictionary of hashtbale and remove all the items that are below threshold 
"""
def getFrequentData(L,threshold):
    aboveThreshold = L.copy()
    for value in aboveThreshold:      
        if aboveThreshold[value] < threshold:
            L.pop(value)    
    return L

"""
        1) This function takes the ordered Transactions 
        2) Then it creates a root node to begin with 
        3) Then it creates a newnode if the parent value does not match and allocate it to the children  
"""
def getGlobalTree(orderedTransactions):
    # import copy
    parent = LinkedList()
    root = Node(1,'Empty')
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
    takes the array or items that are required to find the subsets 
    Reference https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-4.php
"""

def getMySubsets(boxArray):
        return mergeJoinRecusive(list(), sorted(boxArray))

"""
    Recurisively call itself to merge all the possible items together if nothing then it merges an empty set and return that as well 
    Reference https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-4.php 
"""

def mergeJoinRecusive( totalItems, boxArray):
        if boxArray:
            return mergeJoinRecusive(totalItems, boxArray[1:]) + mergeJoinRecusive(totalItems + [boxArray[0]], boxArray[1:])
        return [totalItems]

"""
    This function checks if all the conditional itemsets are frequent or not 
    If they are frequent then we save them 
    If they are not we remove them from the conditonal itemsets
"""
def findFrequentItems(array,parent,threshold):
    count = 0;
    for Box in parent:
        if(set(array).issubset(set(Box))):
            count = count+1
    if count>= threshold:
        return array

