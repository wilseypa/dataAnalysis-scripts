import numpy as np
from scipy.spatial import distance_matrix

def gapInSortedDists(sortedDists):
    diffedDists = np.diff(sortedDists)

data = np.genfromtxt('testData.csv', delimiter=',')   # Load the entire data as a numpy array.
dim = data.shape[1]   # Get the dimension of the data.

window = np.empty([0, dim])   # Create an empty sliding window.
windowMaxSize = 4   # Set the maximum number of data points the window may contain.
pointCounter = 0

for currVec in data:   # Loop through each vector in the data:
    pointCounter += 1
    currVec.shape = (1, dim)   # Correct the shape / dimensions of the current vector.
    if window.shape[0] < windowMaxSize:
        window = np.append(window, currVec, axis=0)   # Fill the window until it reaches its max size.

        # Once the window size reaches its max, construct the lower triangular distance matrix and dump
        # the contents of the window in a file.
        if window.shape[0] == windowMaxSize:
            distMat = np.tril(distance_matrix(window, window))
            np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')
            # print(distMat)

    else:
        # Compute the distances from the current vector to the existing ones in the window.
        distsFromCurrVec = []
        for existingVector in window:
            existingVector.shape = (1, dim)
            dist = np.linalg.norm(existingVector - currVec)
            distsFromCurrVec.append(dist)

        # Find the distance from the current vector to its nearest neighbor in the window.
        nnDistCurrVec = min(distsFromCurrVec)

        # Find the index of the nearest neighbor of the current vector.
        nnIndex = distsFromCurrVec.index(nnDistCurrVec)

        # nearestNeighbor = window[nnIndex]   # Find the nearest neighbor of the current vector.

        # Find the NN distance of the nearest neighbor of the current vector.
        if nnIndex == 0:
            # Pick the min of the first column (except the first element of the first column, which is 0)
            # of the distance matrix.
            nnDistNN = min(distMat[1:, 0])
        else:
            # Pick the min of the nnIndex-th row (up to the diagonal element of the row starting which all
            # elements are 0's) of the distance matrix.
            nnDistNN = min(distMat[nnIndex, :nnIndex])


# print(distMat)
# print(min(distMat[1:,0]))
# print(list(distMat[3,:]).index(min(distMat[3,:3])))