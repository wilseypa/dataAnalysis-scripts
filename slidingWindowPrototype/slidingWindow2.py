import numpy as np
from scipy.spatial import distance_matrix
import statistics
import random

# Determine whether the current vector belongs to any of the existing partitions.
def determineMembership(nnDistsFrmCurrVecToPartns, avgNNDistPartitions, f1, f2, f3):
    existingLabels = list(avgNNDistPartitions.keys())   # Create a list of existing partition labels in the window.
    maxLabel = max(existingLabels)   # Find the max. of the existing partition labels.

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
    maxAvgNNdPartns = max(avgNNDistPartitions.values())

    # If the minimum distance from the current vector to existing partitions is higher than f2 * maxAvgNNdPartns,
    # assign a new partition to the current vector.
    if minDistFrmCurrVecToPartn > (f2 * maxAvgNNdPartns):
        return maxLabel + 1

    # Create a list of 'regular' partitions. Here, 'regular' partition means a partition with >1 point whose
    # avg. nearest neighbor distance is not 0.
    regularPartns = [partns for partns, avgNNd in avgNNDistPartitions.items() if avgNNd > 0]

    # Filter the 'regular' partition(s) for which f1 <= r <= f2, where r is the ratio of the NN distance
    # from the current vector to a partition and the avg. NN distance in that partition.
    rpSimilarToCurrVec = [rp for rp in regularPartns
                        if nnDistsFrmCurrVecToPartns[rp] / avgNNDistPartitions[rp] >= f1
                        or nnDistsFrmCurrVecToPartns[rp] / avgNNDistPartitions[rp] <= f2]

    if -1 in avgNNDistPartitions.values():   # If the window has one or more partitions with exactly 1 point:
        # Make a list of partition label(s) with only 1 point in them.
        singlePointPartition = [sp for sp, avgNNd in avgNNDistPartitions.items() if avgNNd == -1]

        # Filter the partition label(s) from the previous list whose distance(s) to the current vector
        # is (are) not higher than the max of avg. nearest neighbor distances of the existing partitions.
        closeSPP = [cspp for cspp in singlePointPartition
                    if nnDistsFrmCurrVecToPartns[cspp] <= maxAvgNNdPartns]

        if len(closeSPP) != 0:   # If the list 'closeSPP' is not empty:
            # Find the single-point partition(s) that is (are) nearest to the current vector.
            closestSPP = list(set(nearestPartitions) & set(closeSPP))

            if len(closestSPP) != 0:
                return max(closestSPP)

        if 0 in avgNNDistPartitions.values():   # If any of partitions has(ve) avg. NN distance = 0:
            # Create a list of partition(s) with >1 point that has(ve) avg. nearest neighbor distance = 0.
            zeroNNdistPartns = [partns for partns, avgNNd in avgNNDistPartitions.items() if avgNNd == 0]

            # Filter the partition(s) from the previous list whose distance(s) to the current vector
            # is (are) less than f3.
            p0CloseToCurrVec = [p0 for p0 in zeroNNdistPartns if nnDistsFrmCurrVecToPartns[p0] < f3]

            candidatePartns = p0CloseToCurrVec + rpSimilarToCurrVec

            # Filter the partition(s) from the previous list that is (are) nearest to the current vector.
            nearestCandidatePartns = list(set(nearestPartitions) & set(candidatePartns))

            if len(nearestCandidatePartns) != 0:
                # (Randomly) Assign the current vector to a (the) partition filtered above.
                assignedPartition = random.choice(nearestCandidatePartns)
                return assignedPartition

        else:
            candidatePartns = rpSimilarToCurrVec
            nearestCandidatePartns = list(set(nearestPartitions) & set(candidatePartns))

            if len(nearestCandidatePartns) != 0:
                assignedPartition = random.choice(nearestCandidatePartns)
                return assignedPartition

    else:
        if 0 in avgNNDistPartitions.values():  # If any of partitions has(ve) avg. NN distance = 0:
            # Create a list of partition(s) with >1 point that has(ve) avg. nearest neighbor distance = 0.
            zeroNNdistPartns = [partns for partns, avgNNd in avgNNDistPartitions.items() if avgNNd == 0]

            # Filter the partition(s) from the previous list whose distance(s) to the current vector
            # is (are) less than f3.
            p0CloseToCurrVec = [p0 for p0 in zeroNNdistPartns if nnDistsFrmCurrVecToPartns[p0] < f3]

            candidatePartns = p0CloseToCurrVec + rpSimilarToCurrVec

            # Filter the partition(s) from the previous list that is (are) nearest to the current vector.
            nearestCandidatePartns = list(set(nearestPartitions) & set(candidatePartns))

            if len(nearestCandidatePartns) != 0:
                # (Randomly) Assign the current vector to a (the) partition filtered above.
                assignedPartition = random.choice(nearestCandidatePartns)
                return assignedPartition

        else:
            candidatePartns = rpSimilarToCurrVec
            nearestCandidatePartns = list(set(nearestPartitions) & set(candidatePartns))

            if len(nearestCandidatePartns) != 0:
                assignedPartition = random.choice(nearestCandidatePartns)
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

f1 = 0.5
f2 = 1.5
f3 = 0.25


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

        if window.shape[0] == windowMaxSize:   # Once the window size reaches its max:
            distMat = np.tril(distance_matrix(window, window))   # Construct the lower triangular distance matrix.

            # Dump the contents of the window in a file.
            np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')

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

            # Extract the average nearest neighbor distance in the single 'partition' in the window.
            avgNNDistSinglePartition = list(avgNNDistPartitions.values())[0]

            if nnDistCurrVec == 0:
                continue

            if avgNNDistSinglePartition == 0 and nnDistCurrVec < f3:
                continue

            if avgNNDistSinglePartition == 0 or \
                    (nnDistCurrVec/avgNNDistSinglePartition < f1) or \
                    (nnDistCurrVec/avgNNDistSinglePartition > f2):
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

                # print(pointCounter)

                # Insert the current vector, its key and a new label into the rear ends
                # of the corresponding containers.
                label = deletedLabel + 1
                window = np.append(window, currVec, axis=0)
                windowKeys.append(key)
                partitionLabels.append(label)
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
            targetPartition = determineMembership(nnDistsFrmCurrVecToPartns, avgNNDistPartitions, f1, f2, f3)

            if targetPartition not in avgNNDistPartitions:   # If the current vector was assigned a new partition:
                deletedKey = windowKeys.pop(0)  # Delete the key (the lowest key) from the front of the list.
                deletedLabel = partitionLabels.pop(0)  # Delete the label from the front of the list.
                window = np.delete(window, 0, axis=0)  # Delete the vector from the front of the sliding window.

                # Delete the 0-th row and 0-th column from the distance matrix.
                distMat = np.delete(np.delete(distMat, 0, axis=0), 0, axis=1)

                # Delete the corresponding distance value from the list of distances from the current vector
                # to the existing ones in the window.
                distsFromCurrVec.pop(0)

                # Find the positions of the points (in the window) that are members of the partition
                # from which the deletion took place.
                delPmemIndices = [i for i, pl in enumerate(partitionLabels) if pl == deletedLabel]

                # If there are no more points left in the partition from which the deletion took place:
                if not delPmemIndices:
                    del avgNNDistPartitions[deletedLabel]

                else:
                    # Recompute the average nearest neighbor distance in the partition from which the
                    # point was deleted.
                    nnDistsDelPartition = []
                    if delPmemIndices[0] == 0:
                        nnDist0thPoint = min(distMat[1:, 0])
                        nnDistsDelPartition.append(nnDist0thPoint)
                        delPmemIndices.pop(0)

                    for index in delPmemIndices:
                        row = distMat[index, :index]
                        column = distMat[index + 1:, index]
                        distsFromPoint = np.append(row, column)
                        nnDistPoint = min(distsFromPoint)
                        nnDistsDelPartition.append(nnDistPoint)

                    avgNNdDelPartition = statistics.mean(nnDistsDelPartition)
                    avgNNDistPartitions[deletedLabel] = avgNNdDelPartition


                # print(pointCounter)
                # Insert the current vector, its key and the new label into the rear ends
                # of the corresponding containers.
                window = np.append(window, currVec, axis=0)
                windowKeys.append(key)
                partitionLabels.append(targetPartition)
                key += 1

                # Update the distance matrix.
                distsFromCurrVecArray = np.array(distsFromCurrVec).reshape(1, windowMaxSize - 1)
                distMat = np.append(distMat, distsFromCurrVecArray, axis=0)  # Add a row to the bottom of the matrix.
                zeroColumn = np.array([0] * windowMaxSize).reshape(windowMaxSize, 1)
                distMat = np.append(distMat, zeroColumn, axis=1)  # Add a column to the right of the matrix.

                # Add a new key, value pair to the dictionary of partitions and their average nearest neighbor
                # distances. In this case, however, the newly created partition has only one point. So, at this
                # time, we insert a value of -1 for the average nearest neighbor distance of the new point.
                avgNNDistPartitions[targetPartition] = -1

            else:   # The current vector is assigned to one of the existing partitions:
                # Count the number of points in the target partition.
                numPointsTP = partitionLabels.count(targetPartition)

                # Retrieve the avg. nearest neighbor distance in the target partition.
                avgNNdTP = avgNNDistPartitions[targetPartition]

                # Find the first occurrence of a partition label != targetPartition label.
                for i in range(windowMaxSize):
                    if partitionLabels[i] != targetPartition:
                        deletedLabel = partitionLabels[i]
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
                # from which the deletion took place.
                delPmemIndices = [i for i, pl in enumerate(partitionLabels) if pl == deletedLabel]

                # If there are no more points left in the partition from which the deletion took place:
                if not delPmemIndices:
                    del avgNNDistPartitions[deletedLabel]

                else:
                    # Recompute the average nearest neighbor distance in the partition from which the
                    # point was deleted.
                    nnDistsDelPartition = []
                    if delPmemIndices[0] == 0:
                        nnDist0thPoint = min(distMat[1:, 0])
                        nnDistsDelPartition.append(nnDist0thPoint)
                        delPmemIndices.pop(0)

                    for index in delPmemIndices:
                        row = distMat[index, :index]
                        column = distMat[index + 1:, index]
                        distsFromPoint = np.append(row, column)
                        nnDistPoint = min(distsFromPoint)
                        nnDistsDelPartition.append(nnDistPoint)

                    avgNNdDelPartition = statistics.mean(nnDistsDelPartition)
                    avgNNDistPartitions[deletedLabel] = avgNNdDelPartition

                # print(pointCounter)
                # Insert the current vector, its key and partition label into the rear ends
                # of the corresponding containers.
                window = np.append(window, currVec, axis=0)
                windowKeys.append(key)
                partitionLabels.append(targetPartition)
                key += 1

                # Update the distance matrix.
                distsFromCurrVecArray = np.array(distsFromCurrVec).reshape(1, windowMaxSize - 1)
                distMat = np.append(distMat, distsFromCurrVecArray, axis=0)  # Add a row to the bottom of the matrix.
                zeroColumn = np.array([0] * windowMaxSize).reshape(windowMaxSize, 1)
                distMat = np.append(distMat, zeroColumn, axis=1)  # Add a column to the right of the matrix.

                # Update the avg. nearest neighbor distance of the partition the current vector was added to.
                if avgNNdTP == -1:
                    avgNNDistPartitions[targetPartition] = nnDistsFrmCurrVecToPartns[targetPartition]

                else:
                    nnD = nnDistsFrmCurrVecToPartns[targetPartition]
                    avgNNDistPartitions[targetPartition] = (numPointsTP * avgNNdTP + nnD) / (numPointsTP + 1)

        # Dump the content of the window to a file with the arrival of every n new data vectors from the stream.
        if (pointCounter % windowMaxSize == 0) and (pointCounter > windowMaxSize):  # Here, n = windowMaxSize
            np.savetxt('windowInstances/p' + str(pointCounter) + '.csv', window, delimiter=',')
            print(avgNNDistPartitions.keys())