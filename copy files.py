
import os
import shutil


path="E:/PaternRec/Project2/GT_LG_Paridhi/"
for fileName in os.listdir("E:\PaternRec\Project2\Paridhi_training"):
        try:
             fileName=fileName.replace(".inkml","")
             #w= open(path + fileName+)
             shutil.copy2(path + fileName+".lg", "E:\PaternRec\Project2\Paridhi_traning_ls")
        except:
                print("File not found",fileName)
'''
fileName="TestingFile.txt"

with open(fileName) as fD:
    for line in fD:
        line = line.strip()
        shutil.copy2(line, "testing_inkml")

fileName = "testingfiles.csv"

with open(fileName) as fD:
    for line in fD:
        line = line.strip("\n")
        line = line.split("/")
        line = line[-1]
        line = "E:/PaternRec/Project2/allInkmlFile/"+line
        shutil.copy2(line, "E:/PaternRec/Project2/Paridhi_testing")
'''

