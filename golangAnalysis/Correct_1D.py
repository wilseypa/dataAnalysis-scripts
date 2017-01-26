import sys

# Open both files
dataFile = open(sys.argv[1], 'r')
corrFile = open(sys.argv[2], 'w+')

# Remove the first two lines
# Increment all others by one
counter = 0
for line in dataFile:
    if counter >= 2:
        corrFile.write(str(float(line) + 1) + '\n')
    else:
        counter = counter + 1

# Close the files
dataFile.close()
corrFile.close()
