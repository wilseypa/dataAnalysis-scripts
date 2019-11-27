import numpy as np

data = np.genfromtxt('testData.csv', delimiter=',')   # Load the entire data as a numpy array.
dim = data.shape[1]   # Get the dimension of the data.

window = np.empty([0, dim])   # Create an empty sliding window.
windowMaxSize = 200   # Set the maximum number of data points the window may contain.
pointCounter = 0

for currVec in data:   # Loop through each vector in the data:
    pointCounter += 1
    currVec.shape = (1, dim)   # Correct the shape / dimension of the current vector.
    if window.shape[0] < windowMaxSize:
        window = np.append(window, currVec, axis=0)   # Fill the window until it reaches its max size.

        # Once the window size reaches its max, dump the contents of the window in a file.
        if window.shape[0] == windowMaxSize:
            np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')

    else:
        # Compute the distances from the current vector to the existing ones in the window.
        nnDistsFromCurrVec = []
        for existingVector in window:
            existingVector.shape = (1, dim)
            dist = np.linalg.norm(existingVector - currVec)
            nnDistsFromCurrVec.append(dist)

        nnIndex = nnDistsFromCurrVec.index(min(nnDistsFromCurrVec))   # Find the index of the nearest neighbor of the current vector.
        nearestNeighbor = window[nnIndex]   # Find the nearest neighbor of the current vector.
