import sys
import numpy as np

# Create the output file
outFile = open(sys.argv[3], 'w+')
outFile.close()

# Open all files
inFiles = []
for i in range(1, 7):
    print('Opened: ' + sys.argv[1] + str(i) + sys.argv[2])
    inFiles.append(open(sys.argv[1] + str(i) + sys.argv[2], 'r'))
outFile = open(sys.argv[3], 'a')

# Combine all input files into a single output file
for f1, f2, f3, f4, f5, f6 in zip(inFiles[0], inFiles[1], inFiles[2], inFiles[3], inFiles[4], inFiles[5]):
    outFile.write(','.join([f1, f2, f3, f4, f5, f6]).replace('\n', '') + '\n')

# Close both files
for item in inFiles:
    item.close()
outFile.close()
