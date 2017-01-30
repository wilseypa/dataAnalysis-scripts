import os
import subprocess
import time


'''************** AUTHOR NICK *************'''


def runRPjava(numClusters, fPath, fName):
    start = time.time()
    returnCode = subprocess.call("java -jar ./RPHash.jar " + fName + " " + str(numClusters) + " " + fName + "RPOut multiproj parallel=true offlineclusterer=kmeans runs=5")
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


def runRPSeq():
    fPath = './' + foName + '/' + foName + str(i) + '/'
    fileN = fPath + foName + str(i) + '_RAW'
    start = time.time()
    rc = runRPjava(int(argsdict['clusters'][0]),fPath ,fileN)
    end = time.time()
    RPTime = (end-start)
    if(rc == 0): 
        dataN=fileN
        fileN = fileN + 'RPOut.RPHashMultiProj'
        rc = runLabeler(fPath, fileN, dataN)
        
        if(rc == 0):
            inP = fileN+".labeled"
            lblN = fPath + foName + str(i) + '_LBLONLY.csv'
            sigCol = fPath + foName + str(i) + '_SIG.csv'
            start = time.time()
            purity = runAnalysis(lblN, inP, fileN + '.Results', sigCol)
            end = time.time()
            aTime = (end-start)
        
        
            outfile = file(outFN, 'a')
            outfile.write(str(i) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(RPTime) + ',' + str(aTime) + ',' + str(purity) + '\n')
            outfile.close()
        else:
            print str(i) + ": Labeler Returned 1, skipping analysis"
    else:
        print str(i) + ": RPHash Returned 1, skipping labeler, analysis"
        
        
        

'''****************************************'''