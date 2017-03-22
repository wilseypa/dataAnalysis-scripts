import sys
import numpy as np
from random import *
from math import ceil
from sklearn.preprocessing import MinMaxScaler

'''************** AUTHOR NICK *************'''

'''
    Generates entire dataset by creating ids and generating raw columns

        Raw columns, centroids, and ids are formated in numpy arrays and returned
'''
def genRawData(argsDict):
    zf = []
    centsF = []
    vNoiseArray=[]
    ids = []

    ''' Parse arguments of dictionary '''
    minValue = float(argsDict['minValue'][0])
    maxValue = float(argsDict["maxValue"][0])
    clusters = int(argsDict["clusters"][0])
    dimensions = int(argsDict["dim"][0])
    vectors = int(argsDict["vectors"][0])
    dist = argsDict["dist"][0]
    cdist = float(argsDict["cdist"][0])
    csigma = float(argsDict["csigma"][0])
    scaling = argsDict["scaling"][0]
    
    
    ids = idClusters(argsDict, clusters, vectors)
   
    for dim in range(0, dimensions):
        if(argsDict["evolve"][0] == 'true'): #IN PROGRESS
            zt = []
            centstF = []
            for i in range(0, int(ceil(vectors /int(argsDict["evint"][0])))):
                if(i == int(ceil(vectors/int(argsDict["evint"][0])))-1):
                    if(vectors%int(argsDict["evint"][0]) == 0):
                        ids = idClusters(argsDict, clusters, int(argsDict["evint"][0]))
                    else:
                        ids = idClusters(argsDict, clusters, vectors%int(argsDict["evint"][0]))
                else:
                    ids = idClusters(argsDict, clusters, vectors)
                z, cents = genRawColumn(argsDict, clusters, ids, dist, vectors, minValue, maxValue, csigma)
                z = genSparseVects(argsDict, z)
        
                if(zt == []):
                    zt = z
                    centstF = cents
                else:
                    zt = np.vstack((zt.flatten(), z.flatten()))
                    centstF = np.vstack((centstF.flatten(), cents.flatten))
                    
            print zt
            if(zf == []):
                zf = zt
                centsF = centstF
            else:
                zf = np.append(zf, zt, 1)
                centsF = np.column_stack((centsF, centstF))        
                    
        else:
            
            z, cents = genRawColumn(argsDict, clusters, ids, dist, vectors, minValue, maxValue, csigma)
            z = genSparseData(argsDict, z)
            z, ids, vNoiseArray = genSparseVectors(argsDict,z,ids,vNoiseArray)
            
            if(zf == []):
                zf = z
                centsF = cents
            else:
                zf = np.append(zf, z, 1)
                centsF = np.column_stack((centsF, cents))
            
    
    for i in xrange(len(vNoiseArray)):
        ids[vNoiseArray[i]] = clusters + 1
    if(scaling == 'true'):
        z = scaleRawData(argsDict, z, minValue, maxValue);
    return zf, ids, centsF


'''
    Generates cluster ids from 1 to # of clusters
'''
def idClusters(argsDict, clusters, vectors):
    retIds = []
    ccounts = argsDict["ccounts"][0]
    
    if ccounts == 'equal':
        for i in range(0, int(clusters)):
            z = np.array([i for t in range(0, vectors/clusters)])
            
            if (retIds == []):
                retIds = z
            else:
                retIds = np.append(retIds, z);   
            
    elif ccounts == 'separated':
        #TODO: 
        print "Not Implemented" 
    else: #random or nothing was entered
        zc = (np.random.randn(clusters) * (.1*(vectors/clusters))) + (vectors/clusters)
        tot = 0
        for i in range(0,int(clusters) - 1):
            z = np.array([i for t in range(0, int(zc[i])) ])
            
            tot = tot + int(zc[i])
            
            if (retIds == []):
                retIds = z
            else:
                retIds = np.hstack((retIds, z)); 
        
        z = np.array([int(clusters-1) for t in range(0, vectors - tot)])
        if (retIds == []):
            retIds = z
        else:
            retIds = np.hstack((retIds, z)); 
    
    return retIds

def genDummyCols(argsDict, data):
    dummyCols = int(argsDict['dummyCols'][0])
    vectors = len(data)
    z = np.random.uniform(0,0,[vectors, dummyCols]);
    data = np.append(data, z, 1)

    return data

def genSparseData(argsDict,data):
    targetPoints = int(float(argsDict["noise"][0]) * len(data))
    
    targetArray = np.random.choice(range(len(data)), targetPoints, replace=False)
    
    for i in xrange(len(targetArray)):
        data[targetArray[i]] = np.random.uniform(float(argsDict["minValue"][0]),float(argsDict["maxValue"][0]));
        
    return data

def genSparseVectors(argsDict,data,ids,targetArray):
    if(targetArray == []):
        targetPoints = int(float(argsDict["vectornoise"][0]) * len(data))
        targetArray = np.random.choice(range(len(data)), targetPoints, replace=False)
    
    for i in xrange(len(targetArray)):
        data[targetArray[i]] = np.random.uniform(float(argsDict["minValue"][0]),float(argsDict["maxValue"][0]));
    
    
    return data,ids,targetArray

'''
    Generates centroids for clusters generation mean
        TODO: Generate nearby clusters (bi, tri, quad, none)
'''
def genCentroids(argsDict, clusters, minValue, maxValue):
    #TODO - 'nearby' clustering for close neighbor
    zf = []
    cOrg = argsDict["corg"][0]
    scalePerc = argsDict['cdist'][0]

    if cOrg == 'random':
        zf = np.random.uniform(minValue, maxValue, clusters)
    if cOrg == 'bi':
        for i in range(0,clusters/2):
            z = np.random.uniform(minValue,maxValue,1)
            z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z = np.vstack((z,z1))
            
            if(zf == []):
                zf = z
            else:
                zf = np.vstack((zf,z))
                
        if(clusters%2 > 0):
            z = np.random.uniform(minValue,maxValue,1)
            if(zf == []):
                zf = z
            else:
                zf = np.append(zf,z,1)
            
    if cOrg == 'tri':
        for i in range(0,clusters/3):
            z = np.random.uniform(minValue,maxValue,1)
            z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z2 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z1 = np.append(z1,z2,1)
            z = np.append(z,z1,1)
            if(zf == []):
                zf = z
            else:
                zf = np.append(zf,z,1)
            
        if(clusters%3 == 1):
            np.random.uniform(minValue,maxValue,1)
        if(clusters%3 == 2):
            z = np.random.uniform(minValue,maxValue,1)
            z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z = np.append(z,z1,1)
            
            if(zf == []):
                zf = z
            else:
                zf = np.append(zf,z,1)
        
    if cOrg == 'quad':
        for i in range(0,clusters/4):
            z = np.random.uniform(minValue,maxValue,1)
            z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z2 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z3 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z2 = np.append(z2,z3,1)
            z1 = np.append(z1,z2,1)
            z = np.append(z,z1,1)
            if(zf == []):
                zf = z
            else:
                zf = np.append(zf,z,1)
                
        if(clusters%4 == 1):
            np.random.uniform(minValue,maxValue,1)
        if(clusters%4 == 2):
            z = np.random.uniform(minValue,maxValue,1)
            z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z = np.append(z,z1,1)
            if(zf == []):
                zf = z
            else:
                zf = np.append(zf,z,1)
        if(clusters%4 == 3):
            z = np.random.uniform(minValue,maxValue,1)
            z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z2 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
            z1 = np.append(z1,z2,1)
            z = np.append(z,z1,1)
            if(zf == []):
                zf = z
            else:
                zf = np.append(zf,z,1)
    
    
    return zf


'''
    Generates a single raw column by creating centroids for the point ids,
        then generate points in columns using centroid as mean
'''
def genRawColumn(argsDict, clusters, ids, dist, vectors, minValue, maxValue, csigma):
    
    cents = genCentroids(argsDict, clusters, minValue, maxValue)
    zf = []
    bc = np.bincount(ids)    
    
    if dist == "gauss" or dist == "normal" or dist == "norm" or dist == "gaussian":
        for r in range(0, clusters):
            z = np.random.randn(bc[r], 1)
            z = z * csigma
            z = z + cents[r]
            if(zf == []):
                zf=np.copy(z)
            else:
                zf = np.vstack((zf, z))
            
    elif dist == "binomial" or dist == "binom":
        # n * p = mean; mean/n = p
        n = 1000
        if "n" in argsDict:
             n = float(argsDict["n"][0])
        for r in range(0, clusters):
            z = z * csigma
            z = np.random.binomial(n,cents[r]/n,[bc[r], 1])
            if(zf == []):
                zf = z
            else:
                zf = np.append(z,zf,axis=0)

    elif dist == "exponential" or dist == "exp":
        # mean = l^-1 = (1/l) = B
        for r in range(0, clusters): 
            l = 1/cents[r - 1]
            z = np.random.exponential(l,[bc[r], 1])
            z = z*csigma
            if(zf == []):
                zf = z
            else:
                zf = np.append(z,zf,axis=0)

    elif dist == "uniform" or dist == "uni":
        for r in range(0, clusters):
            z = np.random.uniform(cents[r] -1, cents[r] + 1, [bc[r], 1])
            z = z*csigma
            if(zf == []):
                zf = z
            else:
                zf = np.append(z,zf,axis=0)

    return zf, cents


'''
    Scales data in a naive way to the expected range
        TODO: Make this scale edges better
'''
def scaleRawData(argsDict, z, minValue, maxValue):
    mins = np.min(z)
    maxs = np.max(z)
    
    rng = maxs - mins
    #Normalize
    z = maxValue - (((maxValue - minValue) * (maxs - z)) / rng)

    return z

'''****************************************'''

    
