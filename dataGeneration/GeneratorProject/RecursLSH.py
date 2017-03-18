'''************** AUTHOR LEE *************'''


from Project import *
import operator
from random import choice
class RecLSH():

    def __init__(self,projector=None):
        #our counter, replace with mincount hash
        self.IDAndCount = {}
        self.IDAndCent = {}
        self.projector = projector

    def getProjector(self):
        return self.projector

    def hashvec(self,xt,x):
        '''
            super simple hash algorithm, reminiscient of pstable lsh
        '''
        s = 1
        for i in xrange(len(xt)):
            s<<=1
            if xt[i]>= 0:s+=1
            if self.IDAndCount.has_key(s):
                self.IDAndCount[s] = self.IDAndCount[s]+1
                self.IDAndCent[s].append(x)
            else:
                self.IDAndCount[s] = 1
                self.IDAndCent[s] = [x]

    def addtocounter(self,x,l):
        '''
            x          - input vector
            IDAndCount - ID->count map
            IDAndCent  - ID->centroid vector map
            hash the projected vector x and update
            the hash to centroid and counts maps
        '''
        xt = self.projector.proj(x)
        self.hashvec(xt,x)

    def medoid(self,X):
        '''
            X - set of vectors
            compute the medoid of a vector set
        '''
        ret = X[0]
        for i in xrange(1,len(X)):
            for j in xrange(len(X[i])): ret[j]+=X[i][j]
        for j in  xrange(len(ret)):ret[j]= ret[j]/float(len(X))

        return ret

    def findDensityModes(self,X,k,l):
        '''
            X - data set
            k - canonical k in k-means
            l - clustering sub-space
            Compute density mode via iterative deepening hash counting
        '''
        if self.projector == None:
            self.projector = Project(len(X[0]),l,projtype='dbf')

        #process data by adding to the counter
        for x in X:
            self.addtocounter(x,l)

        densityAndID = {}
        for cur_id in sort(self.IDAndCount.keys())[2:]:
            densityAndID = self.TwoTimesParentMetric(cur_id,densityAndID)

        # sort by counts
        densityAndIDList = sorted(densityAndID.items(), key=operator.itemgetter(1),reverse=True)
        # compute medoids
        estcentsmap = {}
        for d in densityAndIDList[:int(k*2)]:
            idcent = d[0]
            estcentsmap[idcent] = self.medoid(self.IDAndCent[idcent])
            #print bin(idcent),len(bin(idcent))-2,d[1]


        return self.offlineClusteringMerge(estcentsmap,k,densityAndIDList)


    ### Options ###

    #vvv Various metrics for deciding whether to split a node into two clusters or not vvv#
    def equalSiblingsMetric(self,cur_id, densityAndID):
        '''
            what do we know about these numbers
            parent = child_0 + child_1
            parent will always exist, but two children may not
            * if |parent| == |child|
              no sibling exists
            * if |parent| != |child|
            * good break case approx equal children -> |parent| - |child0| ~= |child0| -> parent ~= 2*|child0|
            * right child greater than deflated parent is not symmetric, need to only deflate on right child
        '''
        cur_count = self.IDAndCount[cur_id]
        parent_id = cur_id>>1
        parent_count = self.IDAndCount[parent_id]
        sibling_id = cur_id^1


        if parent_count==cur_count:
        # no sibling, consume parent, child0 has all density
                densityAndID[parent_id] = None
                densityAndID[cur_id] = cur_count

        if cur_count<0: #flag from left node to deflate parent node
            cur_count = -cur_count
            self.IDAndCount[parent_id] = parent_count-cur_count
            densityAndID[parent_id] = parent_count-cur_count
            self.IDAndCount[cur_id] = parent_count-cur_count #swap back to positive


        if cur_id&1==1:#right child
            densityAndID[parent_id] = densityAndID[parent_id]-cur_count

        else:#left child
            self.IDAndCount[sibling_id] = -cur_count


    def TwoTimesParentMetric(self,cur_id, densityAndID):
            cur_count = self.IDAndCount[cur_id]
            parent_id = cur_id>>1
            parent_count = self.IDAndCount[parent_id]
            sibling_id = cur_id^1

            if 2*cur_count>parent_count:
                #sibling_count = 0
                #if parent_count != cur_count:
                #    sibling_count = self.IDAndCount[sibling_id]
                densityAndID[parent_id] = 0#parent_count-(cur_count+sibling_count)
                densityAndID[cur_id] = cur_count
            return densityAndID
    #^^^ Various metrics for deciding whether to split a node into two clusters or not ^^^#

    #vvv Heuristics for merging oversampled clusters vvv#
    def overSampleBitwiseMerge(self,estcentsmap,k):
        '''
            an attempt to merge very close clusters by the hashes bit distance
            * if two cluster hashes are 1 bit away from one another merge to same cluster
            * favor bitwise similarities in later bits (further down the tree)
        '''

        def isPowerOfTwo (x):
            return ((x != 0) and not(x & (x - 1)))
        mergelist = []
        for i in xrange(len(estcentsmap.keys())):
            d =estcentsmap.keys()[i]
            for ii in xrange(i+1,len(estcentsmap.keys())):
                dd = estcentsmap.keys()[ii]
                if isPowerOfTwo(d^dd):
                    mergelist.append([d^dd,[d,dd]])

        mergelist.sort(reverse=True)

        for mergers in mergelist:
            if len(estcentsmap) == k:
                return estcentsmap
            if estcentsmap.has_key(mergers[1][1]) and estcentsmap.has_key(mergers[1][0]):
                estcentsmap[mergers[1][1]] = self.medoid(vstack((estcentsmap[mergers[1][0]],estcentsmap[ mergers[1][1] ])))
            estcentsmap.pop(mergers[1][0],None)
        return estcentsmap

    def overSampleLongesStrings(self,estcentsmap,k):
        '''
            simple heurisitic of favoring longer hash ids
        '''
        estcentsmaplist = sorted(estcentsmap.items(), key=operator.itemgetter(0),reverse=True)
        ret = {}
        for d in estcentsmaplist[:int(k)]:
            ret[d[0]] = d[1]
        return ret.values()

    def offlineClusteringMerge(self,estcentsmap,k,counts):
        import agglomerative
        counts = [ct[1] for ct in counts[:len(estcentsmap)]]
        return agglomerative.agglomerate(estcentsmap.values(),k,counts)[0]
#^^^ Heuristics for merging oversampled clusters ^^^#
    
    
    
    '''************** AUTHOR NICK *************'''
    
    def buildHashTable(self,X):
        if self.projector == None:
            self.projector = Project(len(X[0]),l,projtype='dbf')

        #process data by adding to the counter
        for x in X:
            self.addtocounter(x,l)
            
        return
    
    def findNN(self,X,xt,k,l):
        '''
            Test method for finding NNs of data
        '''
        if self.IDAndCount=={}:
            buildHashTable(self,X)
            
        s = 1
        for i in xrange(len(xt)):
            s<<=1
            if xt[i]>= 0:s+=1
            
            #Check count of current branch
            if self.IDAndCount.has_key(s):
                #print "\t" + bin(s) + "\t" + str(self.IDAndCount[s])
                if self.IDAndCount[s] == k:
                    #print "found count <= k"
                    #print self.IDAndCent[s]
                    return self.IDAndCent[s] 
                if self.IDAndCount[s] < k:
                    #print "Found branch with possibilities above"
                    #print s
                    s>>=0
                    #print s
                    
        
        return
