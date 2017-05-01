import sys
from pattern_rec_read_files import *
import numpy as np
import math


def start(fileName):
    allFiles=get_all_file_paths(fileName)
    symbolsList=['\\int', '\\Delta', 'E', '\\tan', 'n', '\\gt', '9', '\\lambda', '/', '!',
             '\\div', '2', 'v', '\\leq', 'm', 's', '\\}', 'z', '\\times', 'A', 'B', 'Y',
             '\\lim', 'j', 'b', ']', 'q', 't', 'u', '\\geq', '\\alpha', 'y', '\\sqrt', '+',
             '7', 'o', 'g', 'R', '\\pi', '.', 'V', '\\lt', 'T', 'H', 'X', ',', '\\mu', 'l',
             '\\{', '\\in', 'e', '=', 'd', 'C', '\\log', '\\sigma', 'i', 'L', '4', '\\cos', '5', '0',
             ')', 'c', '\\rightarrow', '\\pm', 'I', '\\gamma', 'r', '3', '1', 'f', 'P', 'F', '|', '\\infty',
             'G', '8', '\\theta', '-', '\\sin', '6', 'M', '\\exists', 'w', 'k', '\\phi', '\\sum', '\\beta',
             'a', '[', '\\prime', 'S', 'h', 'p', 'N', '\\neq', 'x', '\\forall', '(', '\\ldots']
    print(symbolsList[45])
    print(len(symbolsList))
    data=np.zeros((len(allFiles),len(symbolsList)),dtype=np.int)
    fileIndex=0
    for file in allFiles:
        #print("working on",file)
        allSymbols=read_file_Traning(file)
        for symbol in allSymbols:
           if symbol in symbolsList:
                data[fileIndex][symbolsList.index(symbol)]+=1

        fileIndex+=1
    print(data)
    add=np.sum(data,axis=0)
    print(add)
    testing=add*.3
    testing=testing.astype(np.int)
    AimTesting=list(testing)
    traning = add*.7
    traning=traning.astype(np.int)
    AimTraning=list(traning)
    index=0
    print("\nAim Traning:",traning)
    print("\nAim Testing:", testing)
    testingFinal=[]
    traningFinal=[]
    for row in data:
        sseTest=calculateSSE(row,testing)
        sseTrain=calculateSSE(row,traning)
        if sseTest > sseTrain and len(testing)>0:
            testingFinal.append(index)
            testing-=data[index]
        else:
            traningFinal.append(index)
            traning-=data[index]
        index+=1

    gotTraning=evaluate(traningFinal,data)
    print("\nGot Traning:",gotTraning)

    gotTesting=evaluate(testingFinal,data)
    print("\nGot Testing:",gotTesting)
    print("Train:",AimTraning-gotTraning)
    print("Test:",AimTesting-gotTesting)
    with open("TraningFile.txt","w") as fileDiscriptor:
        for fileNam in traningFinal:
            fileDiscriptor.write(allFiles[fileNam]+"\n")


    with open("TestingFile.txt","w") as fileDiscriptor:
        for fileNam in testingFinal:
            fileDiscriptor.write(allFiles[fileNam]+"\n")

    #print("Traning",gotTraning)
    #print("Testing", gotTesting)
    errorCal(gotTraning,AimTesting)

    return 1
def errorCal(gotTraning,AimTesting):
    err=0
    for i in range(len(gotTraning)):
        err+=math.fabs((gotTraning[i]-AimTesting[i])/AimTesting[i])

    print("\n\n ERROR:",err/len(AimTesting))


def evaluate(traningFinal,data):
    val=data[traningFinal[0]]
    for i in traningFinal[1:]:
        val+=data[i]
    return val


def calculateSSE(val1,val2):
    sse=(val1-val2)**2
    sse=np.sqrt(np.sum(sse))
    return sse






if __name__ == '__main__':
    start("E:\PaternRec\Project2\TrainINKML")