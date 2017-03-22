from numpy import *
def affinity(X,Y):
    return sum((X-Y)**2)**.5

def affinityMatrix(A):
    arr_len = len(A)
    ret = zeros([arr_len,arr_len])
    for i in xrange(arr_len):
        for j in xrange(i+1,arr_len):
            d = affinity(A[i],A[j])
            ret[i][j] = d
    return ret

def nn(grid,labels,clustersizes):
    '''
        find the nearest two clusters of the remaining clusters in labels
    '''
    minlabel = [labels[0],labels[1]]
    minaff = grid[labels[0]][labels[1]]
    for i in xrange(len(labels)):
        idx1 = labels[i]
        for j in xrange(i+1,len(labels)):
            idx2 = labels[j]
            if grid[idx1][idx2] < minaff and (clustersizes[idx1]>0 or clustersizes[idx2]>0):
                minaff = grid[idx1][idx2]
                if clustersizes[idx1]>clustersizes[idx2]:minlabel = [idx1,idx2]
                else : minlabel = [idx2,idx1]
    return minlabel

def weightedCentroid(A,clustersizes,keeplabel,removelabel):
    '''
        compute a new centroid based on the weighted average of two prior centroids
    '''
    newsize = float(clustersizes[removelabel]+clustersizes[keeplabel])
    weigthedRatioKeep = clustersizes[keeplabel]/newsize
    weightedRatioRemove = clustersizes[removelabel]/newsize
    newcentroid = weigthedRatioKeep*A[keeplabel]+weightedRatioRemove*A[removelabel]
    return newcentroid,newsize



def agglomerateNearest(keeplabel,removelabel,labels,clustersizes, grid,A):
    '''
        merge the two nearest clusters
    '''
    #weighted centroid
    A[keeplabel],clustersizes[keeplabel] =weightedCentroid(A,clustersizes,keeplabel,removelabel)
    for idx1 in labels:
        grid[idx1][keeplabel] = affinity(A[idx1],A[keeplabel])
    for idx1 in labels:
        grid[idx1][removelabel] = -1
    labels.remove(removelabel)
    return labels,A,grid,clustersizes



def agglomerate(A,k,clustersizes=None):
    '''
        perform agglomerative clustering until label size = k
    '''
    A = array(A)
    grid = affinityMatrix(A)
    labels = range(len(grid))
    if clustersizes==None: clustersizes = [1.0]*len(grid)
    while len(labels) > k:
        keeplabel,removelabel = nn(grid,labels,clustersizes)
        labels,A,grid,clustersizes = agglomerateNearest(keeplabel,removelabel,labels,clustersizes, grid,A)

    try:
        badhombre = clustersizes.index(1.0)
        print "crap"
    except:
        noopvar = None

    return [A[l] for l in labels],[clustersizes[l] for l in labels]

if __name__ == "__main__":
    A = (random.randn(100,2)*.33+[1,1]).tolist()
    A.extend((random.randn(100,2)*.33+[-1,-1]).tolist())
    A.extend((random.randn(100,2)*.33+[1,-1]).tolist())
    A.extend((random.randn(100,2)*.33+[-1,1]).tolist())
    A.extend((random.randn(100,2)*.33 + [2,-1]).tolist())
    A.extend((random.randn(100,2)*.33 + [-2,2]).tolist())
    A.extend(random.randn(100,2).tolist())
    A = array(A)

    clusters,clustersizes =  agglomerate(A,6)
    clusters = array(clusters)
    '''
    import pylab
    pylab.plot(A[:,0],A[:,1],'o')
    pylab.plot(clusters[:,0],clusters[:,1],'*',markersize=10)
    pylab.show()
    '''
print clusters,clustersizes