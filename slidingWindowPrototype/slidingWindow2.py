import numpy as np
from scipy.spatial import distance_matrix
import statistics

# Determine whether the current vector belongs to any of the existing partitions.
def determinePartition(partitionLabels, window):
    partitions = set(partitionLabels)
    for l in partitions:



data = np.genfromtxt('testData.csv', delimiter=',', skip_header=1)   # Load the entire data as a numpy array.
dim = data.shape[1]   # Get the dimension of the data.

window = np.empty([0, dim])   # Create an empty sliding window.
windowMaxSize = 200   # Set the maximum number of data points the window may contain.
pointCounter = 0

windowKeys = []
partitionLabels = []

key = 0

for currVec in data:   # Loop through each vector in the data:
    pointCounter += 1
    currVec.shape = (1, dim)

    # Initialize the sliding window. During the initialization, let's assume all points from the stream
    # belong to Partition 0.
    if window.shape[0] < windowMaxSize:
        label = 0
        window = np.append(window, currVec, axis=0)   # Fill the window until it reaches its max size.
        windowKeys.append(key)
        partitionLabels.append(label)
        key += 1

        # Once the window size reaches its max, construct the lower triangular distance matrix and dump
        # the contents of the window in a file.
        if window.shape[0] == windowMaxSize:
            distMat = np.tril(distance_matrix(window, window))
            np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')


    else:
        if len(set(partitionLabels)) == 1:
            if
