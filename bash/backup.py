import os
from pathlib import Path
import subprocess

# Helper function I found online to sort a list by the second element of a tuple
# https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
def Sort_Tuple(tup):
    lst = len(tup)
    for i in range(0, lst): 
        for j in range(0, lst-i-1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

# Gets the working directory path
uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
dirPath = uppath(os.path.realpath(__file__), 1)

# Calls the backup script ./sql_backup.sh
subprocess.call(["sudo", os.path.join(dirPath, "sql_backup.sh"), dirPath])

# Limits the number of backups on disk to 21
files = []
for file in os.listdir(dirPath):
    if file.endswith(".sql"):
        fullPath = os.path.join(dirPath, file)
        files.append((fullPath, os.path.getmtime(fullPath)))

# Removes the oldest files
sortedDates = Sort_Tuple(files)
while (len(sortedDates) > 21):
    os.remove(sortedDates[0][0])
    sortedDates.pop(0)