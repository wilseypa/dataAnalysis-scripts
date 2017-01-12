import sys
import numpy as np
from random import *

'''
    Generates entire dataset by creating ids and generating raw columns

        Raw columns, centroids, and ids are formated in numpy arrays and returned
'''
def genRawData(argsDict):
    zf = []
    centsF = []

    ''' Parse arguments of dictionary '''
    minValue = float(argsDict['minValue'][0])
    maxValue = float(argsDict["maxValue"][0])
    clusters = int(argsDict["clusters"][0])
    dimensions = int(argsDict["dim"][0])
    vectors = int(argsDict["vectors"][0])
    dist = argsDict["dist"][0]
    cdist = float(argsDict["cdist"][0])
    csigma = float(argsDict["csigma"][0])

    ids = idClusters(clusters, vectors)
   
    for dim in range(0, dimensions):
        z, cents = genRawColumn(argsDict, clusters, ids, dist, vectors, minValue, maxValue, csigma)
        z = scaleRawData(argsDict, z, minValue, maxValue);
        if(zf == []):
            zf = z
            centsF = cents
        else:
            zf = np.append(zf, z, 1)
            centsF = np.append(centsF, cents,0 )
        
    return zf, ids, centsF


'''
    Generates cluster ids from 1 to # of clusters
'''
def idClusters(clusters, vectors):
    retIds = []
    for i in range(1, int(clusters) + 1):
        z = np.array([i for t in range(0, vectors/clusters)])
    
        if (retIds == []):
            retIds = z
        else:
            retIds = np.append(retIds, z, 0);
    return retIds 

def genDummyCols(argsDict, data):
    dummyCols = int(argsDict['dummyCols'][0])
    vectors = len(data)
    z = np.random.uniform(0,1,[vectors, dummyCols]);
    data = np.append(data, z, 1)

    return data


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
            z = np.append(z,z1,1)
            
            if(zf == []):
                zf = z
            else:
                zf = np.append(zf,z,1)
                
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
        for r in range(1, clusters + 1):
            z = np.random.randn(bc[r], 1)
            z = z * csigma
            z = z + cents[r - 1]
            if(zf == []):
                zf = z
            else:
                zf = np.append(z, zf, axis=0)

    if dist == "binomial" or dist == "binom":
        # n * p = mean; mean/n = p
        n = 1000
        if "n" in argsDict:
             n = float(argsDict["n"][0])
        for r in range(1, clusters + 1):
            z = z * csigma
            z = np.random.binomial(n,cents[r-1]/n,[bc[r], 1])
            if(zf == []):
                zf = z
            else:
                zf = np.append(z,zf,axis=0)

    if dist == "exponential" or dist == "exp":
        # mean = l^-1 = (1/l) = B
        for r in range(1, clusters + 1): 
            l = 1/cents[r - 1]
            z = np.random.exponential(l,[bc[r], 1])
            z = z*csigma
            if(zf == []):
                zf = z
            else:
                zf = np.append(z,zf,axis=0)

    if dist == "uniform" or dist == "uni":
        for r in range(1, clusters + 1):
            z = np.random.uniform(cents[r-1] -1, cents[r-1] + 1, [bc[r], 1])
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
    
    #Normalize
    z = (z-z.min())/float(z.max() - z.min())

    #Re-Scale
    z = minValue + z* (maxValue - minValue)
    return z


    
