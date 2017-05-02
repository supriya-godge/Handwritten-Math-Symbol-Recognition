
import os
import shutil

'''
path="E:/PaternRec/Project2/GT_LG_Paridhi/"
for fileName in os.listdir("E:/PaternRec/Project2/test_out"):
        try:
             w= open(path + fileName)
             shutil.copy2(path + fileName, "E:/PaternRec/Project2/GT_testing")
        except:
                print("File not found",fileName)
'''
fileName="TraningFile.txt"

with open(fileName) as fD:
    for line in fD:
        line = line.strip()
        shutil.copy2(line, "testing_inkml")


