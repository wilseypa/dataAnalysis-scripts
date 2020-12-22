import numpy as np
from scipy.spatial import distance_matrix
import statistics
import random


# Determine whether the current vector belongs to any of the existing partitions.
def determineMembership(nnDistsFrmCurrVecToPartns, avgNNDistPartitions, f2, f3):
    # Find the minimum of the distances from the current vector to the existing partitions.
    minDistFrmCurrVecToPartn = min(nnDistsFrmCurrVecToPartns.values())

    # Find the partition(s) that is (are) nearest to the current vector.
    nearestPartitions = [k for k in nnDistsFrmCurrVecToPartns
                         if nnDistsFrmCurrVecToPartns[k] == minDistFrmCurrVecToPartn]

    # If the (nearest neighbor) distance from the current vector to any partition is 0, assign the current
    # vector to that partition. If there are more than one such partitions, assign the current vector randomly
    # to one of them.
    if minDistFrmCurrVecToPartn == 0:
        assignedPartition = random.choice(nearestPartitions)
        return assignedPartition

    # Find the max of the avg. nearest neighbor distances of the existing partitions in the window.
    # maxAvgNNdPartns = max(avgNNDistPartitions.values())

    existingLabels = list(avgNNDistPartitions.keys())  # Create a list of existing partition labels in the window.
    maxLabel = max(existingLabels)  # Find the max. of the existing partition labels.

    # If the minimum distance from the current vector to existing partitions is higher than f2,
    # assign a new partition to the current vector.
    if minDistFrmCurrVecToPartn > f2:
        return maxLabel + 1

    candidatePartns = []
    for partn in avgNNDistPartitions:
        if avgNNDistPartitions[partn] == -1 and nnDistsFrmCurrVecToPartns[partn] <= f2:
            candidatePartns.append(partn)

        elif avgNNDistPartitions[partn] <= f3 and nnDistsFrmCurrVecToPartns[partn] <= 1:
            candidatePartns.append(partn)

        elif avgNNDistPartitions[partn] > 0 and nnDistsFrmCurrVecToPartns[partn] / avgNNDistPartitions[partn] <= f2:
            candidatePartns.append(partn)

    nearestCandidatePartns = list(set(nearestPartitions) & set(candidatePartns))

    if len(nearestCandidatePartns) != 0:
        assignedPartition = max(nearestCandidatePartns)
        return assignedPartition

    return maxLabel + 1


data = np.genfromtxt('testData.csv', delimiter=',', skip_header=1)   # Load the entire data as a numpy array.
dim = data.shape[1]   # Get the dimension of the data.

window = np.empty([0, dim])   # Create an empty sliding window.
windowMaxSize = 200   # Set the maximum number of data points the window may contain.
pointCounter = 0

windowKeys = []
partitionLabels = []
avgNNDistPartitions = {}

key = 0

# f1 = 0.5
f2 = 4
f3 = 0.25
# minWeight = 5   # Partitions with number of points <= minWeight can be potential outliers.

# A partition is considered outdated if it did not receive any new point for more than
# the last 25 insertions.
timeToBeOutdated = 25

numPointsPartn = {}   # Create a dictionary to store the number of points in each partition.
maxKeys = {}   # Create a dictionary to store the maxKey of each partition.

for currVec in data:   # Loop through each vector in the data:
    # Dump the content of the window to a file with the arrival of every n new data vectors from the stream.
    if (pointCounter % windowMaxSize == 0) and (pointCounter > windowMaxSize):  # Here, n = windowMaxSize
        np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')
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

        if window.shape[0] == windowMaxSize:   # Once the window size reaches its max:
            distMat = np.tril(distance_matrix(window, window))   # Construct the lower triangular distance matrix.

            # Dump the contents of the window in a file.
            # np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')

            # Find the average nearest neighbor distance in the existing partition (i.e. Partition 0).
            nnDistsPartition0 = []
            nnDist0thPoint = min(distMat[1:, 0])
            nnDistsPartition0.append(nnDist0thPoint)
            for index in range(1, windowMaxSize):
                row = distMat[index, :index]
                column = distMat[index+1:, index]
                distsFromPoint = np.append(row, column)
                nnDistPoint = min(distsFromPoint)
                nnDistsPartition0.append(nnDistPoint)

            avgNNDistPartition0 = statistics.mean(nnDistsPartition0)
            avgNNDistPartitions[label] = avgNNDistPartition0

            numPointsPartn[label] = windowMaxSize
            maxKeys[label] = key - 1


    else:
        if len(avgNNDistPartitions) == 1:   # If the window is 'pure':
            # Compute the distances from the current vector to the existing ones in the window.
            distsFromCurrVec = []
            for existingVector in window:
                existingVector.shape = (1, dim)
                dist = np.linalg.norm(existingVector - currVec)
                distsFromCurrVec.append(dist)

            # Sort the distances from the current vector (to the existing ones in the window) in increasing order.
            ascendingDists = sorted(distsFromCurrVec)

            # Find the distance from the current vector to its nearest neighbor in the window.
            nnDistCurrVec = ascendingDists[0]

            print("nnDistCurrVec")
            print(nnDistCurrVec)

            # Extract the average nearest neighbor distance in the single 'partition' in the window.
            avgNNDistSinglePartition = list(avgNNDistPartitions.values())[0]

            if nnDistCurrVec == 0:
                print(pointCounter)
                print(avgNNDistPartitions)
                print("==============================================================================================")
                continue

            if avgNNDistSinglePartition <= f3 and nnDistCurrVec <= 1:
                print(pointCounter)
                print(avgNNDistPartitions)
                print("==============================================================================================")
                continue

            print("avgNNDistSinglePartition")
            print(avgNNDistSinglePartition)

            if avgNNDistSinglePartition == 0 or nnDistCurrVec / avgNNDistSinglePartition > f2:
                deletedKey = windowKeys.pop(0)   # Delete the key (the lowest key) from the front of the list.
                deletedLabel = partitionLabels.pop(0)   # Delete the label from the front of the list.
                window = np.delete(window, 0, axis=0)  # Delete the vector from the front of the sliding window.

                # Delete the 0-th row and 0-th column from the distance matrix.
                distMat = np.delete(np.delete(distMat, 0, axis=0), 0, axis=1)

                # Delete the corresponding distance value from the list of distances from the current vector
                # to the existing ones in the window.
                distsFromCurrVec.pop(0)

                # Recompute the average nearest neighbor distance in the existing partition.
                nnDistsPartition = []
                nnDist0thPoint = min(distMat[1:, 0])
                nnDistsPartition.append(nnDist0thPoint)
                for index in range(1, windowMaxSize-1):
                    row = distMat[index, :index]
                    column = distMat[index + 1:, index]
                    distsFromPoint = np.append(row, column)
                    nnDistPoint = min(distsFromPoint)
                    nnDistsPartition.append(nnDistPoint)

                avgNNDistPartition = statistics.mean(nnDistsPartition)
                avgNNDistPartitions[deletedLabel] = avgNNDistPartition

                # Decrement the number of points in the existing partition by 1.
                numPointsPartn[deletedLabel] = windowMaxSize - 1

                print("Point Added")

                # Insert the current vector, its key and a new label into the rear ends
                # of the corresponding containers.
                label = deletedLabel + 1
                window = np.append(window, currVec, axis=0)
                windowKeys.append(key)
                partitionLabels.append(label)

                maxKeys[label] = key
                key += 1

                # Update the distance matrix.
                distsFromCurrVecArray = np.array(distsFromCurrVec).reshape(1, windowMaxSize - 1)
                distMat = np.append(distMat, distsFromCurrVecArray, axis=0)  # Add a row to the bottom of the matrix.
                zeroColumn = np.array([0] * windowMaxSize).reshape(windowMaxSize, 1)
                distMat = np.append(distMat, zeroColumn, axis=1)  # Add a column to the right of the matrix.

                # Add a new key, value pair to the dictionary of partitions and their average nearest neighbor
                # distances. In this case, however, the newly created partition has only one point. So, at this
                # time, we insert a value of -1 for the average nearest neighbor distance of the new point.
                avgNNDistPartitions[label] = -1

                numPointsPartn[label] = 1

            print(pointCounter)
            print(avgNNDistPartitions)
            print("==============================================================================================")

        else:
            # Create a dictionary to store the nearest neighbor distance from the current vector to each
            # partition in the window.
            nnDistsFrmCurrVecToPartns = {}

            # Create a list to store the distances from the current vector to all existing points in the window.
            distsFromCurrVec = [0] * windowMaxSize

            for partition in avgNNDistPartitions:
                # Find the positions of the points (in the window) that are members of the present 'partition'.
                indicesOfMembers = [i for i, pl in enumerate(partitionLabels) if pl == partition]

                # Compute the distances from the current vector to the members of the current partition.
                distsFrmCurrVecToMembrs = []
                for idx in indicesOfMembers:
                    member = window[idx]
                    member.shape = (1, dim)
                    dist = np.linalg.norm(member - currVec)
                    distsFrmCurrVecToMembrs.append(dist)
                    distsFromCurrVec[idx] = dist

                # Sort the distances from the current vector to the members in the present partition
                # in increasing order.
                ascendingDistsToMembrs = sorted(distsFrmCurrVecToMembrs)

                # Find the distance from the current vector to its nearest neighbor in the present partition.
                nndToPartn = ascendingDistsToMembrs[0]

                # Insert the distance from the current vector to its nearest neighbor in the present partition
                # into the corresponding dictionary.
                nnDistsFrmCurrVecToPartns[partition] = nndToPartn

            # Determine the membership of the current vector to one of the existing partitions in the window.
            # If the current vector cannot be assigned to any of the existing partitions, create a new partition
            # with only the current vector.
            targetPartition = determineMembership(nnDistsFrmCurrVecToPartns, avgNNDistPartitions, f2, f3)

            # Find the outdated partition(s).
            outdatedPartn = [op for op in maxKeys if (key - maxKeys[op]) > timeToBeOutdated]

            if len(outdatedPartn) != 0:   # If there is (are) outdated partition(s):
                # Find the number(s) of points in the outdated partition(s).
                numPtsOutdated = [numPointsPartn[npo] for npo in outdatedPartn]

                # Find the smallest size (i.e. the min. of the number(s) of points) of the outdated partition(s).
                numPtsSmallestOutdated = min(numPtsOutdated)

                # Find the smallest outdated partition(s).
                smallestOutdated = [so for so, numPts in numPointsPartn.items() if numPts == numPtsSmallestOutdated]

                partnToBeDeleted = min(smallestOutdated)

                # Find the first occurrence of a partition label from which deletion will take place.
                for i in range(windowMaxSize):
                    if partitionLabels[i] == partnToBeDeleted:
                        deletedLabel = partnToBeDeleted
                        indexToBeDeleted = i
                        del partitionLabels[i]   # Delete the partition label.
                        break

                del windowKeys[indexToBeDeleted]  # Delete the key of the vector.
                window = np.delete(window, indexToBeDeleted, axis=0)  # Delete the vector from the sliding window.

                # Delete the corresponding row and column from the distance matrix.
                distMat = np.delete(np.delete(distMat, indexToBeDeleted, axis=0), indexToBeDeleted, axis=1)

                # Delete the corresponding distance value from the list of distances from the current vector
                # to the existing ones in the window.
                del distsFromCurrVec[indexToBeDeleted]

                # Find the positions of the points (in the window) that are members of the partition
                # from which the point was deleted.
                delPmemIndices = [i for i, pl in enumerate(partitionLabels) if pl == deletedLabel]

                # If there are no more points left in the partition from which the deletion took place:
                if not delPmemIndices:
                    del avgNNDistPartitions[deletedLabel]
                    del numPointsPartn[deletedLabel]
                    del maxKeys[deletedLabel]

                else:
                    # Decrement the number of points in the partition from which the point was deleted by 1.
                    numPointsPartn[deletedLabel] = numPtsSmallestOutdated - 1

                    # Recompute the average nearest neighbor distance in the partition from which the
                    # point was deleted.
                    # If there is only 1 point left in the partition that the point was deleted from:
                    if numPointsPartn[deletedLabel] == 1:
                        avgNNDistPartitions[deletedLabel] = -1

                    else:
                        nnDistsDelPartition = []
                        for i in delPmemIndices:
                            row = [distMat[i, :i][j] for j in delPmemIndices if j < i]
                            column = [distMat[i+1:, i][j - (i+1)] for j in delPmemIndices if j > i]
                            distsFromPoint = np.append(row, column)
                            nnDistPoint = min(distsFromPoint)
                            nnDistsDelPartition.append(nnDistPoint)

                        avgNNdDelPartition = statistics.mean(nnDistsDelPartition)
                        avgNNDistPartitions[deletedLabel] = avgNNdDelPartition

                print("Point Added")

                # Insert the current vector, its key and partition label into the rear ends
                # of the corresponding containers.
                window = np.append(window, currVec, axis=0)
                windowKeys.append(key)
                partitionLabels.append(targetPartition)
                maxKeys[targetPartition] = key   # Insert or update the maxKey of the target partition.

                # Update the distance matrix.
                distsFromCurrVecArray = np.array(distsFromCurrVec).reshape(1, windowMaxSize - 1)
                distMat = np.append(distMat, distsFromCurrVecArray, axis=0)  # Add a row to the bottom of the matrix.
                zeroColumn = np.array([0] * windowMaxSize).reshape(windowMaxSize, 1)
                distMat = np.append(distMat, zeroColumn, axis=1)  # Add a column to the right of the matrix.

                if targetPartition not in avgNNDistPartitions:  # If the current vector was assigned a new partition:
                    avgNNDistPartitions[targetPartition] = -1
                    numPointsPartn[targetPartition] = 1

                else:  # The current vector is assigned to one of the existing partitions:
                    # Retrieve the avg. nearest neighbor distance in the target partition.
                    avgNNdTP = avgNNDistPartitions[targetPartition]

                    if avgNNdTP == -1:   # If the target partition previously had only 1 point:
                        # Update the avg. nearest neighbor distance of the partition the current vector was added to.
                        avgNNDistPartitions[targetPartition] = nnDistsFrmCurrVecToPartns[targetPartition]
                        numPointsPartn[targetPartition] = 2

                    else:
                        # Find the positions of the points (in the window) that are members of the target partition.
                        tpMemIndices = [i for i, tp in enumerate(partitionLabels) if tp == targetPartition]

                        # Recompute the average nearest neighbor distance in the target partition.
                        nnDistsTP = []
                        for i in tpMemIndices:
                            row = [distMat[i, :i][j] for j in tpMemIndices if j < i]
                            column = [distMat[i+1:, i][j - (i+1)] for j in tpMemIndices if j > i]
                            distsFromPoint = np.append(row, column)
                            nnDistPoint = min(distsFromPoint)
                            nnDistsTP.append(nnDistPoint)

                        avgNNdTargetPartn = statistics.mean(nnDistsTP)
                        avgNNDistPartitions[targetPartition] = avgNNdTargetPartn
                        numPointsPartn[targetPartition] = numPointsPartn[targetPartition] + 1

                key += 1

            else:   # There is no outdated partition in the window:
                if targetPartition not in avgNNDistPartitions:  # If the current vector was assigned a new partition:
                    deletedKey = windowKeys.pop(0)  # Delete the key (the lowest key) from the front of the list.
                    deletedLabel = partitionLabels.pop(0)  # Delete the label from the front of the list.
                    window = np.delete(window, 0, axis=0)  # Delete the vector from the front of the sliding window.

                    # Delete the 0-th row and 0-th column from the distance matrix.
                    distMat = np.delete(np.delete(distMat, 0, axis=0), 0, axis=1)

                    # Delete the corresponding distance value from the list of distances from the current vector
                    # to the existing ones in the window.
                    distsFromCurrVec.pop(0)

                    # Find the positions of the points (in the window) that are members of the partition
                    # from which the point was deleted.
                    delPmemIndices = [i for i, pl in enumerate(partitionLabels) if pl == deletedLabel]

                    # If there are no more points left in the partition from which the deletion took place:
                    if not delPmemIndices:
                        del avgNNDistPartitions[deletedLabel]
                        del numPointsPartn[deletedLabel]
                        del maxKeys[deletedLabel]

                    else:
                        # Decrement the number of points in the partition from which the point was deleted by 1.
                        numPointsPartn[deletedLabel] = numPointsPartn[deletedLabel] - 1

                        # Recompute the average nearest neighbor distance in the partition from which the
                        # point was deleted.
                        # If there is only 1 point left in the partition that the point was deleted from:
                        if numPointsPartn[deletedLabel] == 1:
                            avgNNDistPartitions[deletedLabel] = -1

                        else:
                            nnDistsDelPartition = []
                            for i in delPmemIndices:
                                row = [distMat[i, :i][j] for j in delPmemIndices if j < i]
                                column = [distMat[i+1:, i][j - (i+1)] for j in delPmemIndices if j > i]
                                distsFromPoint = np.append(row, column)
                                nnDistPoint = min(distsFromPoint)
                                nnDistsDelPartition.append(nnDistPoint)

                            avgNNdDelPartition = statistics.mean(nnDistsDelPartition)
                            avgNNDistPartitions[deletedLabel] = avgNNdDelPartition

                    print("Point Added")

                    # Insert the current vector, its key and the new label into the rear ends
                    # of the corresponding containers.
                    window = np.append(window, currVec, axis=0)
                    windowKeys.append(key)
                    partitionLabels.append(targetPartition)
                    maxKeys[targetPartition] = key

                    key += 1

                    # Update the distance matrix.
                    distsFromCurrVecArray = np.array(distsFromCurrVec).reshape(1, windowMaxSize - 1)
                    distMat = np.append(distMat, distsFromCurrVecArray, axis=0)
                    zeroColumn = np.array([0] * windowMaxSize).reshape(windowMaxSize, 1)
                    distMat = np.append(distMat, zeroColumn, axis=1)  # Add a column to the right of the matrix.

                    # Add a new key, value pair to the dictionary of partitions and their average nearest neighbor
                    # distances. In this case, however, the newly created partition has only one point. So, at this
                    # time, we insert a value of -1 for the average nearest neighbor distance of the new point.
                    avgNNDistPartitions[targetPartition] = -1
                    numPointsPartn[targetPartition] = 1

                else:   # The current vector is assigned to one of the existing partitions:
                    # Find the first occurrence of a partition label != targetPartition label.
                    for i in range(windowMaxSize):
                        if partitionLabels[i] != targetPartition:
                            deletedLabel = partitionLabels[i]
                            indexToBeDeleted = i
                            del partitionLabels[i]  # Delete the partition label.
                            break

                    del windowKeys[indexToBeDeleted]  # Delete the key of the vector.
                    window = np.delete(window, indexToBeDeleted, axis=0)  # Delete the vector from the sliding window.

                    # Delete the corresponding row and column from the distance matrix.
                    distMat = np.delete(np.delete(distMat, indexToBeDeleted, axis=0), indexToBeDeleted, axis=1)

                    # Delete the corresponding distance value from the list of distances from the current vector
                    # to the existing ones in the window.
                    del distsFromCurrVec[indexToBeDeleted]

                    # Find the positions of the points (in the window) that are members of the partition
                    # from which the point was deleted.
                    delPmemIndices = [i for i, pl in enumerate(partitionLabels) if pl == deletedLabel]

                    # If there are no more points left in the partition from which the deletion took place:
                    if not delPmemIndices:
                        del avgNNDistPartitions[deletedLabel]
                        del numPointsPartn[deletedLabel]
                        del maxKeys[deletedLabel]

                    else:
                        # Decrement the number of points in the partition from which the point was deleted by 1.
                        numPointsPartn[deletedLabel] = numPointsPartn[deletedLabel] - 1

                        # Recompute the average nearest neighbor distance in the partition from which the
                        # point was deleted.
                        # If there is only 1 point left in the partition that the point was deleted from:
                        if numPointsPartn[deletedLabel] == 1:
                            avgNNDistPartitions[deletedLabel] = -1

                        else:
                            nnDistsDelPartition = []
                            for i in delPmemIndices:
                                row = [distMat[i, :i][j] for j in delPmemIndices if j < i]
                                column = [distMat[i+1:, i][j - (i+1)] for j in delPmemIndices if j > i]
                                distsFromPoint = np.append(row, column)
                                nnDistPoint = min(distsFromPoint)
                                nnDistsDelPartition.append(nnDistPoint)

                            avgNNdDelPartition = statistics.mean(nnDistsDelPartition)
                            avgNNDistPartitions[deletedLabel] = avgNNdDelPartition

                    print("Point Added")

                    # Insert the current vector, its key and partition label into the rear ends
                    # of the corresponding containers.
                    window = np.append(window, currVec, axis=0)
                    windowKeys.append(key)
                    partitionLabels.append(targetPartition)
                    maxKeys[targetPartition] = key   # Update the maxKey of the target partition.

                    key += 1

                    # Update the distance matrix.
                    distsFromCurrVecArray = np.array(distsFromCurrVec).reshape(1, windowMaxSize - 1)
                    distMat = np.append(distMat, distsFromCurrVecArray, axis=0)  # Add a row to the bottom of the matrix
                    zeroColumn = np.array([0] * windowMaxSize).reshape(windowMaxSize, 1)
                    distMat = np.append(distMat, zeroColumn, axis=1)  # Add a column to the right of the matrix.

                    # Retrieve the avg. nearest neighbor distance in the target partition.
                    avgNNdTP = avgNNDistPartitions[targetPartition]

                    if avgNNdTP == -1:  # If the target partition previously had only 1 point:
                        # Update the avg. nearest neighbor distance of the partition the current vector was added to.
                        avgNNDistPartitions[targetPartition] = nnDistsFrmCurrVecToPartns[targetPartition]
                        numPointsPartn[targetPartition] = 2

                    else:
                        # Find the positions of the points (in the window) that are members of the target partition.
                        tpMemIndices = [i for i, tp in enumerate(partitionLabels) if tp == targetPartition]

                        # Recompute the average nearest neighbor distance in the target partition.
                        nnDistsTP = []
                        for i in tpMemIndices:
                            row = [distMat[i, :i][j] for j in tpMemIndices if j < i]
                            column = [distMat[i+1:, i][j - (i+1)] for j in tpMemIndices if j > i]
                            distsFromPoint = np.append(row, column)
                            nnDistPoint = min(distsFromPoint)
                            nnDistsTP.append(nnDistPoint)

                        avgNNdTargetPartn = statistics.mean(nnDistsTP)
                        avgNNDistPartitions[targetPartition] = avgNNdTargetPartn
                        numPointsPartn[targetPartition] = numPointsPartn[targetPartition] + 1

            print(pointCounter)
            print(nnDistsFrmCurrVecToPartns)
            print("targetPartition " + str(targetPartition))
            print(avgNNDistPartitions)
            print("==================================================================================================")