import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import inspect
import numpy as np

'''************** AUTHOR NICK *************'''
'''
    Generate plots in to the filepath
'''
def generatePlots(fPathRaw, type):
    plt.figure(1)
    if type == 'pdf' or type == 'all':
        plt.savefig(fPathRaw + '.pdf', bbox_inches='tight')
    if type == 'png' or type == 'all':
        plt.savefig(fPathRaw + '.png', bbox_inches='tight')

'''
    Clear the in-memory plot
'''
def clearPlots():
    plt.clf()
    return

'''
    Show the in-memory plot
'''
def showPlots():
    plt.show()
    return

'''
    Generate 3D plot for generation and result matching
'''
def r3DPlot(xTestPts, yTestPts, zTestPts, ids, pos, cents, match):
    x_val = [x for x in xTestPts]
    y_val = [y for y in yTestPts]
    z_val = [z for z in zTestPts]

    fig = plt.figure(1)
    ax = fig.add_subplot(pos,projection='3d')

    markers = ['o','x']

    colors = ['r', 'c', 'y', 'g', 'b', 'm', 'k', 'ro']
    for i in range(0, len(x_val)):
        if(match == {}):
            ax.scatter(x_val[i], y_val[i],z_val[i],c=colors[ids[i]],s=0.5)
        else:
            ax.scatter(x_val[i], y_val[i],z_val[i],marker=markers[match[i]],c=colors[ids[i]],s=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
'''
    Generate 2D plot for generation and result matching
'''
def simplePlot(xTestPts, yTestPts, ids, cents, match):
    clearPlots()
    x_val = [x for x in xTestPts]
    y_val = [x for x in yTestPts]
    

    markers = ['o','x']
    colors = ['r', 'c', 'y', 'g', 'b', 'm', 'k', 'ro']

    plt.figure(1)
    plt.subplot(221)
    
    for i in range(0, len(x_val)):
        if (match == {}):
            plt.scatter(x_val[i], y_val[i], c=colors[ids[i]],s=1)
        else:
            plt.scatter(x_val[i], y_val[i],marker=markers[match[i]],c=colors[ids[i]],s=1)

    #minx, maxx = checkPlotBoundaries(x_val, minx, maxx)
    #miny, maxy = checkPlotBoundaries(y_val, miny, maxy)

    #plt.axis([minx,maxx,miny,maxy])

    plt.grid(True, which='both')


'''
    Generate EUC distance plot for generation and result matching
'''
def eucPlot(testPts,ids,cents, match):
    x_val = []
    markers = ['o','x']
    colors = ['r', 'c', 'y', 'g', 'b', 'm', 'k', 'ro']
    for row in testPts:
        x_val.append([np.linalg.norm(row)])
    plt.figure(1)
    plt.subplot(223)

    for i in range(0, len(x_val)):
        if(match == {}):
            plt.scatter(ids[i],x_val[i], c=colors[ids[i]],s=3)
        else:
            plt.scatter(ids[i], x_val[i],marker=markers[match[i]],c=colors[ids[i]], s=3)

    plt.grid(True, which='both')
    return

'''
    Check and set the plot boundaries (not used)
'''
def checkPlotBoundaries(xTestPts, minx, maxx):
    if(min(xTestPts) < minx):
        minx = min(xTestPts) - 1
    if(max(xTestPts) > maxx):
        maxx = max(xTestPts) + 1

    return minx, maxx

'''
    Generate squared distance plot for generation (not used)
'''
def sqDistPlot(testPts, minx, miny, maxx, maxy):
    vals = [];    
    i=0
    for x in testPoints:
        i = i + 1
        euc = 0;
        for z in len(x):
            euc += pow(x[z] ,2)
	vals[i] = euc

    simplePlot(vals, vals, minx, miny, maxx, maxy)
    
'''****************************************'''
