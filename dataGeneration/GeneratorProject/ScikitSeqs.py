from ReadResults import *
import os
import subprocess
import stats
import time
import sys
import resource
from utils import *
from Project import *
from RecursLSH import *
from sklearn.neighbors import KDTree, BallTree, LSHForest
from sklearn.cluster import KMeans, MiniBatchKMeans, MeanShift, estimate_bandwidth


'''************** AUTHOR NICK *************'''
def runKDTreeSizeAnalysis(argsdict, data, inlbl, fPath, fName, fileN, i):
    start = time.time()
    tree = KDTree(data, leaf_size = 1)
    end = time.time()
    
    print tree.get_tree_stats()
    return tree.__sizeof__(),(end-start)



def runBallTreeSizeAnalysis(argsdict, data, inlbl, fPath, fName, fileN, i):
    start = time.time()
    tree = BallTree(data, leaf_size = 1)
    end = time.time()
    print tree.get_tree_stats()
    
    return sys.getsizeof(tree),(end-start)

def runForestLSHSizeAnalysis(argsdict, data, inlbl, fPath, fName, fileN, i):
    start = time.time()
    tree = LSHForest(random_state=42)
    tree.fit(data)
    end=time.time()
    
    return sys.getsizeof(tree),(end-start)

def runSizeAnalysis(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime):
    data = readInputFromFile(fileN + "_RAW",'float')
    inlbl = readInputFromFile(fileN + "_LBLONLY.csv",'int')
    
    size, time = runKDTreeSizeAnalysis(argsdict, data, inlbl, fPath, fName, fileN, i)
    
    outfile = file(outFN, 'a')
    outfile.write('KDTree' + str(i) +  ',' + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(0) + ',' + str(time) + ',' + str(0)
                  +  ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)  
                  + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(time) + ',' + str(size) + '\n')
    outfile.close()
    
    size, time = runBallTreeSizeAnalysis(argsdict, data, inlbl, fPath, fName, fileN, i)
    
    outfile = file(outFN, 'a')
    outfile.write('BallTree' + str(i) +  ',' + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(0) + ',' + str(time) + ',' + str(0)
                  +  ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)  
                  + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(time) + ',' + str(size) + '\n')
    outfile.close()
    
    size, time = runForestLSHSizeAnalysis(argsdict, data, inlbl, fPath, fName, fileN, i)
    
    outfile = file(outFN, 'a')
    outfile.write('Forest' + str(i) +  ',' + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(0) + ',' + str(time) + ',' + str(0)
                  +  ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)  
                  + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(time) + ',' + str(size) + '\n')
    outfile.close()
    
    return

def obj_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([obj_size(v, seen) for v in obj.values()])
        size += sum([obj_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += obj_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, z=(bytes, bytearray)):
        size += sum([obj_size(i, seen) for i in obj])
    return size

def runSciKitCluster(numClusters, fPath, fName):
    start = time.time()
    print fName
    returnCode = subprocess.call("java -jar ./RPHash.jar " + fName + " " + str(numClusters) + " " + fName + "RPOut multiproj parallel=true offlineclusterer=kmeans runs=5", shell=True)
    #copy metrics file from root to the current fPath
    if os.path.isfile(fPath + 'metrics_time_memkb_wcsse.csv'):
        os.remove(fPath + 'metrics_time_memkb_wcsse.csv')
    os.rename('./metrics_time_memkb_wcsse.csv', fPath + 'metrics_time_memkb_wcsse.csv')
    end = time.time()
    return returnCode, (end - start)


def runkMeans(argsdict, data, inlbl, fPath, fName, fileN, i,sampleType):
    start = time.time()
    est = KMeans(init=sampleType,n_clusters=int(argsdict['clusters'][0]),n_init=10)
    est.fit_predict(data)
    end = time.time()
    #print "\nmemSize(end): \n" + str(obj_size(est,None))
    #print est.cluster_centers_
    
    return runRawAnalysis(argsdict,inlbl,est.labels_, fileN + '.Results', fPath + fName + str(i) + '_SIG.csv', (end-start))

def runMiniBatchkMeans(argsdict, data, inlbl, fPath, fName, fileN, i, sampleType):
    start = time.time()
    est = MiniBatchKMeans(init=sampleType,n_clusters=int(argsdict['clusters'][0]),n_init=10)
    est.fit_predict(data)
    end = time.time()
    
    return runRawAnalysis(argsdict,inlbl,est.labels_, fileN + '.Results', fPath + fName + str(i) + '_SIG.csv', (end-start))

def runMeanShift(argsdict, data, inlbl, fPath, fName, fileN, i, sampleType):
    start = time.time()
    est = MeanShift(bandwidth=estimate_bandwidth(data,quantile=0.2))
    
    est.fit_predict(data)
    end = time.time()
    
    return runRawAnalysis(argsdict,inlbl,est.labels_, fileN + '.Results', fPath + fName + str(i) + '_SIG.csv', (end-start))



def runSciKitSeq(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime):
    data = readInputFromFile(fileN + "_RAW",'float')
    inlbl = readInputFromFile(fileN + "_LBLONLY.csv",'int')          
    
    
    if(argsdict['exec'] != 'lsh'):
            
        kmeans = ['k-means++','random']
        
        
        for t in range(0,len(kmeans)):
            ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime,execTime = runkMeans(argsdict, data, inlbl, fPath, fName, fileN, i, kmeans[t])
                    
            print "\tkmeans" + kmeans[t] + ": " + str([ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime])
                
            outfile = file(outFN, 'a')
            outfile.write('kmeans_' + kmeans[t] +  ',' + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(execTime) + ',' + str(aTime)
                          +  ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                          + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + ',' + str(execTime) + '\n')
            outfile.close()
            
        for t in range(0,len(kmeans)):
            ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime,execTime = runMiniBatchkMeans(argsdict, data, inlbl, fPath, fName, fileN, i, kmeans[t])
                    
            print "\tkmeansMini" + kmeans[t] + ": " + str([ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime])
                
            outfile = file(outFN, 'a')
            outfile.write('kminibatch_' + kmeans[t] + ',' + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(execTime) + ',' + str(aTime)
                          +  ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                          + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + ',' + str(execTime) + '\n')
            outfile.close()
        
        ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime,execTime = runMeanShift(argsdict, data, inlbl, fPath, fName, fileN, i, kmeans[t])
                    
        print "\tMeanShift" + ": " + str([ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime])
            
        outfile = file(outFN, 'a')
        outfile.write('MeanShift,' + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(execTime) + ',' + str(aTime)
                      +  ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                      + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + ',' + str(execTime) + '\n')
        outfile.close()
        
        
    else:
        print "Running LSH functionality of SciKit"
        
        
        
    return
        
        

'''****************************************'''