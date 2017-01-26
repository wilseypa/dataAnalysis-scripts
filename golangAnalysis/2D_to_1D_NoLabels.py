import sys
import numpy as np

# Create the output file
outFile = open(sys.argv[2], 'w+')
outFile.close()

# Determine input CSV file size information
rows = 0
inFile = open(sys.argv[1], 'r')
for _ in inFile:
    rows = rows + 1
cols = len(_.split(',')) - 1
inFile.close()

# Open both files
inFile = open(sys.argv[1], 'r')
outFile = open(sys.argv[2], 'a')

# Write the size information
outFile.write(str(rows) + '\n' + str(cols) + '\n')

# Tranform the data from 2D to 1D one line at a time
for line in inFile:
    tmpLine = line.split(',')
    oneD_col = '\n'.join(tmpLine[:-1])
    outFile.write(oneD_col + '\n')

# Close both files
inFile.close()
outFile.close()
