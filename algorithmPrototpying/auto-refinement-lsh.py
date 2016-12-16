from pylab import *

def proj(x,P):
    '''
        x - high dimensional vector
        P - len(x) * n matrix of GNV elements
        this is a naive and slow random projection,
        but it's compact and to the point.
    '''
    return x.dot(P)*(1/float(len(P)))**.5

def hashvec(x):
    '''
        super simple hash algorithm, reminiscient of pstable lsh
    '''
    s = ''
    for i in xrange(len(x)):
        if x[i] > 0.0: s = s+ '1'
        else : s = s+'0'
    return s


def addtocounter(x,P,IDAndCount,IDAndCent):
    '''
        x          - input vector
        IDAndCount - ID->count map
        IDAndCent  - ID->centroid vector map

        hash the projected vector x and update
        the hash to centroid and counts maps
    '''
    xt = proj(x,P)
    s = hashvec(xt)

    for i in xrange(1,len(s)):
        if IDAndCount.has_key(s[:i]):
            IDAndCount[str(s[:i])] = IDAndCount[s[:i]]+1
            IDAndCent[str(s[:i])].append(x)
        else:
            IDAndCount[s[:i]] = 1
            IDAndCent[str(s[:i])] = [x]

def medoid(X):
    '''
        X - set of vectors
        compute the medoid of a vector set
    '''
    ret = X[0]
    for i in xrange(1,len(X)):
        for j in xrange(len(X[i])): ret[j]+=X[i][j]
    for j in  xrange(len(ret)):ret[j]= ret[j]/float(len(X))
    return ret

def findDensityModes(X,k,l):
    '''
        X - data set
        k - canonical k in k-means
        l - clustering sub-space
        Compute density mode via iterative deepening hash counting
    '''
    d = len(X[0])

    #our counter, replace with mincount hash
    IDAndCount = {}
    IDAndCent = {}

    #create projector matrixs
    P = randn(d,l)

    #process data by adding to the counter
    for x in X:
        addtocounter(x,P,IDAndCount, IDAndCent)

    #we are adding everything and sorting here, real implementation would
    #use a priority queue, heap, skiplist, redblack, and may be bounded
    densityAndID = []
    for h in sort(IDAndCount.keys()):
        if len(h)>1  and 2*IDAndCount[h] > IDAndCount[h[:len(h)-1]]:
            densityAndID.append( (IDAndCount[h],h))

            #remove old
            if len(h)>2 and densityAndID.__contains__((IDAndCount[h[:len(h)-1]],h[:len(h)-1] )):
                densityAndID.remove((IDAndCount[h[:len(h)-1]],h[:len(h)-1] ))

    # sort
    densityAndID.sort(reverse=True)

    # compute medoids
    estcents = []
    for d in densityAndID[0:k]:
        idcent = d[1]
        estcents.append(medoid(IDAndCent[idcent]))

    return estcents

l = 24
def run(d,n,k,noise = 4):
    '''
        d - dimensionality
        n - number of vectors to generate
        k - number of clusters to partition vectors in
        this method generates data from a heteroscedastic gaussian distribution
        and partitions it into k clusters. It then adds noise 1/4 from a uniform
        distribution -1.5 - +1.5. Then plots the results of iterative deepening
        hash count clustering and plots the data in a 3x3 subplot.
    '''
    #generate some density modes
    cents = rand(k,d)*2-1
    X = []
    for i in xrange(n):
        if i%noise==0:X.append(rand(d)*3-1.5)#add some noise
        X.append( array(cents[randint(len(cents))]+(randn(d)*(.15*rand()))))

    estcents = findDensityModes(X,k,l)

    #randomly pick the axis to plot
    xcol , ycol = randint(d),randint(d)
    while xcol == ycol: ycol = randint(d)

    subplot(3,3,k-1)
    plot([x[xcol] for x in X[::2]],[x[ycol] for x in X[::2]],',',label=str(k))
    plot([x[xcol] for x in estcents],[x[ycol] for x in estcents],'o',color='gold',markersize=7)
    plot([x[xcol] for x in cents],[x[ycol] for x in cents],'*',markersize=7,color='red')
    legend()


'''
    Run some tests with different numbers of clusters
'''
d = 500
n = 5000
for i in range(2,11):
    run(d,n,i)

show()
