import numpy as np
from scipy.spatial import distance_matrix
import statistics
# from scipy.signal import find_peaks


# A function to determine if there is a relatively large gap in the values of the sorted distances.
def gapInSortedDists(sortedDists):
    diffedDists = np.diff(sortedDists)   # Compute the first order adjacent differences of the sorted distances.
    avg = statistics.mean(diffedDists)
    sd = statistics.stdev(diffedDists)
    peak = avg + 10*sd
    # trough = avg - 8*sd

    # peaks = find_peaks(diffedDists, prominence=10*sd)
    # if peaks[0].size > 0:
    #     return True
    # else:
    #     return False

    for val in diffedDists:
        if val > peak:
        # if (val > peak) or (val < trough):
            return True

    return False


data = np.genfromtxt('testData.csv', delimiter=',', skip_header=1)   # Load the entire data as a numpy array.
dim = data.shape[1]   # Get the dimension of the data.

window = np.empty([0, dim])   # Create an empty sliding window.
windowMaxSize = 200   # Set the maximum number of data points the window may contain.
pointCounter = 0
f1 = 3   # A factor that determines when new data points are added to the sliding window.
# f2 = 0.25

# Create two lists for the LRU architecture.
windowKeys = []
dynamicKeyContainer = []

key = 0

for currVec in data:   # Loop through each vector in the data:
    pointCounter += 1
    currVec.shape = (1, dim)   # Correct the shape / dimensions of the current vector.
    if window.shape[0] < windowMaxSize:
        window = np.append(window, currVec, axis=0)   # Fill the window until it reaches its max size.
        windowKeys.append(key)
        dynamicKeyContainer.append(key)
        key += 1

        # Once the window size reaches its max, construct the lower triangular distance matrix and dump
        # the contents of the window in a file.
        if window.shape[0] == windowMaxSize:
            distMat = np.tril(distance_matrix(window, window))
            np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')

    else:
        # Compute the distances from the current vector to the existing ones in the window.
        distsFromCurrVec = []
        for existingVector in window:
            existingVector.shape = (1, dim)
            dist = np.linalg.norm(existingVector - currVec)
            if dist == 0:
                break
            distsFromCurrVec.append(dist)

        if dist == 0:
            continue

        # Sort the distances from the current vector (to the existing ones in the window) in increasing order.
        ascendingDists = sorted(distsFromCurrVec)

        # Find the distance from the current vector to its nearest neighbor in the window.
        nnDistCurrVec = ascendingDists[0]

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

        print(pointCounter)
        print('nnDistCurrVec = ' + str(nnDistCurrVec) + ', ' + 'nnDistNN = ' + str(nnDistNN))
        print('nnDistCurrVec/nnDistNN = ' + str(nnDistCurrVec/nnDistNN))
        print(gapInSortedDists(ascendingDists))
        print('---------------------------------------------------------------------------------------')

        # Test the main criteria for adding the current vector to the sliding window.
        # If the current vector is to be added:
        if (nnDistCurrVec / nnDistNN > f1) or gapInSortedDists(ascendingDists):
        # if (nnDistCurrVec/nnDistNN > f1) or (nnDistCurrVec/nnDistNN < f2) or gapInSortedDists(ascendingDists):
            print("Point Added")
            print('=====================================================================================')
            keyToBeDeleted = dynamicKeyContainer.pop(0)   # Delete and return the first element from the list.
            indexToBeDeleted = windowKeys.index(keyToBeDeleted)   # Find the index of the vector to be deleted.
            del windowKeys[indexToBeDeleted]   # Delete the key of the vector.
            window = np.delete(window, indexToBeDeleted, axis=0)   # Delete the vector from the sliding window.

            # Delete the corresponding row and column from the distance matrix.
            distMat = np.delete(np.delete(distMat, indexToBeDeleted, axis=0), indexToBeDeleted, axis=1)

            # Delete the corresponding distance value from the list of distances from the current vector
            # to the existing ones in the window.
            del distsFromCurrVec[indexToBeDeleted]

            # Insert the current vector and its key into the rear ends of the sliding window and the key containers.
            window = np.append(window, currVec, axis=0)
            windowKeys.append(key)
            dynamicKeyContainer.append(key)
            key += 1

            # Update the distance matrix.
            distsFromCurrVecArray = np.array(distsFromCurrVec).reshape(1, windowMaxSize-1)
            distMat = np.append(distMat, distsFromCurrVecArray, axis=0)   # Add a row to the bottom of the matrix.
            zeroColumn = np.array([0] * windowMaxSize).reshape(windowMaxSize, 1)
            distMat = np.append(distMat, zeroColumn, axis=1)   # Add a column to the right of the matrix.

        else:
            # Discard the incoming vector, and move its representative (nearest neighbor) to the rear of
            # the dynamic key container.
            nnKey = windowKeys[nnIndex]
            dynamicKeyContainer.append(dynamicKeyContainer.pop(dynamicKeyContainer.index(nnKey)))

        # Dump the content of the window to a file every time n new data vectors are added to the window.
        if (pointCounter % windowMaxSize == 0) and (pointCounter > windowMaxSize):   # Here, n = windowMaxSize
            np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')


# np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')
# print(distMat)
# print(min(distMat[1:,0]))
# print(list(distMat[3,:]).index(min(distMat[3,:3])))