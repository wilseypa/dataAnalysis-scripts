from ReadResults import *
import os
import subprocess
import stats
import time
from utils import *
from sklearn.cluster import KMeans, MiniBatchKMeans, MeanShift, estimate_bandwidth


'''************** AUTHOR NICK *************'''


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
            outfile.write(runTag + '_kmeans' + str(i) + kmeans[t] +  ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(execTime) + ',' + str(aTime)
                          +  ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                          + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + '\n')
            outfile.close()
            
        for t in range(0,len(kmeans)):
            ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime,execTime = runMiniBatchkMeans(argsdict, data, inlbl, fPath, fName, fileN, i, kmeans[t])
                    
            print "\tkmeansMini" + kmeans[t] + ": " + str([ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime])
                
            outfile = file(outFN, 'a')
            outfile.write(runTag + '_kmini' + str(i) + kmeans[t] + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(execTime) + ',' + str(aTime)
                          +  ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                          + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + '\n')
            outfile.close()
        
        ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime,execTime = runMeanShift(argsdict, data, inlbl, fPath, fName, fileN, i, kmeans[t])
                    
        print "\tMeanShift" + ": " + str([ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime])
            
        outfile = file(outFN, 'a')
        outfile.write(runTag + '_MeanShift' + str(i) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(execTime) + ',' + str(aTime)
                      +  ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                      + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + '\n')
        outfile.close()
        
        
    else:
        print "Running LSH functionality of SciKit"
        
        
        
    return
        
        

'''****************************************'''