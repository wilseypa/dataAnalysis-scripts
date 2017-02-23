from ReadResults import *
import os
import subprocess
import time


'''************** AUTHOR NICK *************'''
def checkRPFiles():
    if not os.path.exists('./RPHash.jar'):
        print "Missing RPHash.jar from root directory - copy before running generator"
        return False
    if not os.path.exists('./LabelData.jar'):
        print "Missing LabelData.jar from root directory - copy before running generator"
        return False
    return True
    
def defaultRPParams(argsDict):
    
    
    return argsDict


def runRPjava(argsdict,testPath,fName):
    numClusters = int(argsdict['clusters'][0])
    start = time.time()
    print fName
    returnCode = subprocess.call("java -jar ./RPHash.jar " + fName + " " + str(numClusters) + " " 
        + fName + "RPOut " + argsdict['clusteringmethod'][0] + " numblur=" + str(argsdict['numblur'][0])
        + " offlineclusterer=" + argsdict['offlineclusterer'][0] + " runs=" + str(argsdict['runs'][0])
        + " decodertype=" + argsdict['decodertype'][0] + " numprojections=" + str(argsdict['numprojections'][0]), shell=True)
    #copy metrics file from root to the current test filepath
    if os.path.isfile(testPath + 'metrics_time_memkb_wcsse.csv'):
        os.remove(testPath + 'metrics_time_memkb_wcsse.csv')
    if os.path.isfile('./metrics_time_memkb_wcsse.csv'):
        os.rename('./metrics_time_memkb_wcsse.csv', testPath + 'metrics_time_memkb_wcsse.csv')
    end = time.time()
    return returnCode, (end - start)


def readMetrics(fPath):
    if os.path.isfile(fPath + 'metrics_time_memkb_wcsse.csv'):
        outfile = file(fPath + 'metrics_time_memkb_wcsse.csv', 'r')
        out = outfile.read();
        outfile.close()
    return out.rstrip()


def runLabeler(fPath, fName, dataN):
    returnCode = subprocess.call("java -jar ./LabelData.jar " + fName+" " + dataN + " " + fName+".labeled", shell=True)
    return returnCode


def runSingleRP(argsdict, rootPath, fileN, fName, i, outFN, runTag, testPath, GenTime):
    rc, RPTime = runRPjava(argsdict,testPath,fileN)
        
    if(rc == 0): 
        rpMetrics = readMetrics(testPath)
        dataN = fileN
        fileN = fileN + 'RPOut.RPHashAdaptive2Pass'
        rc = runLabeler(testPath, fileN, dataN)
        
        if(rc == 0):
            inP = fileN+".labeled"
            lblN = rootPath + fName + str(i) + '_LBLONLY.csv'
            sigCol = rootPath + '/' + fName + str(i) + '_SIG.csv'
            
            ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime,tt = runAnalysis(argsdict, lblN, inP, outFN, sigCol, 1)
            
            outfile = file(outFN, 'a')
            outfile.write(runTag + ',' + testPath + str(i) + ',' + str(GenTime) + ',' + str(RPTime) + ',' + str(aTime)
                          + ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                          + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + '\n')
            outfile.close()
        else:
            print str(i) + ": Labeler Returned 1, skipping analysis"
    else:
        print str(i) + ": RPHash Returned 1, skipping labeler, analysis"
    return


def runRPSeq(argsdict, rootPath, fileN, fName, i, outFN, runTag, testPath, GenTime):
    argsdict = defaultRPParams(argsdict)
    
    for z in range(0,16):
        argsdict['numprojections'] = [z%4]
        runTag = argsdict['clusteringmethod'][0] + " - proj: " + str(z)
        
        runSingleRP(argsdict, rootPath, fileN, fName, i, outFN, runTag, testPath, GenTime)
    
    return
    
        
        

'''****************************************'''