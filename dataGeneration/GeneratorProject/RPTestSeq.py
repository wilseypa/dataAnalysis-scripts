from ReadResults import *
import os
import subprocess
import time


'''************** AUTHOR NICK *************'''


def runRPjava(numClusters, fPath, fName):
    start = time.time()
    print fName
    returnCode = subprocess.call("java -jar ./RPHash.jar " + fName + " " + str(numClusters) + " " + fName + "RPOut multiproj parallel=true offlineclusterer=kmeans runs=5", shell=True)
    #copy metrics file from root to the current fPath
    if os.path.isfile(fPath + 'metrics_time_memkb_wcsse.csv'):
        os.remove(fPath + 'metrics_time_memkb_wcsse.csv')
    os.rename('./metrics_time_memkb_wcsse.csv', fPath + 'metrics_time_memkb_wcsse.csv')
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

def runReadResults():
    purity = runAnalysis()
    return purity


def runRPSeq(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime):
    rc, RPTime = runRPjava(int(argsdict['clusters'][0]),fPath ,fileN)
        
    if(rc == 0): 
        rpMetrics = readMetrics(fPath)
        dataN = fileN
        fileN = fileN + 'RPOut.RPHashMultiProj'
        
        rc = runLabeler(fPath, fileN, dataN)
        
        if(rc == 0):
            inP = fileN+".labeled"
            lblN = fPath + fName + str(i) + '_LBLONLY.csv'
            sigCol = fPath + fName + str(i) + '_SIG.csv'
            
            purity, aTime = runAnalysis(lblN, inP, fileN + '.Results', sigCol)
            
            outfile = file(outFN, 'a')
            outfile.write(runTag + '_' + str(i) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(RPTime) + ',' + str(aTime) + ',' + str(purity) + ',' + str(rpMetrics) + '\n')
            outfile.close()
        else:
            print str(i) + ": Labeler Returned 1, skipping analysis"
    else:
        print str(i) + ": RPHash Returned 1, skipping labeler, analysis"
    return
        
        

'''****************************************'''