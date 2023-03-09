
import numpy as np

from functions import readingFile,minimumSupport,get__allItems_with_first_count,getFrequentData, remove_infrequent_items_from_dataset,getGlobalTree
import sys, time


class LinkedList:
    def __init__(self):
        self.head =None


class Node:
    def __init__(self, value, next=None,previous=None):
        self.value = value
        self.next = next
        self.previous = previous

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
    print(frequentItemSet)
    # LL = LinkedList()
    # LL.head = Node(3)
    # print(LL.head.value)

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
            
                    

   
    globalTree =  getGlobalTree(orderedTransactions)
    print(globalTree)
