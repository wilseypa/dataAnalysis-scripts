import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import inspect
import numpy as np

def generatePlots(fPathRaw):
    plt.figure(1)
    plt.savefig(fPathRaw + '.pdf', bbox_inches='tight')
    plt.savefig(fPathRaw + '.png', bbox_inches='tight')


def showPlots():
    plt.show()


def r3DPlot(xTestPts, yTestPts, zTestPts, ids, pos, cents):
    x_val = [x for x in xTestPts]
    y_val = [y for y in yTestPts]
    z_val = [z for z in zTestPts]

    fig = plt.figure(1)
    ax = fig.add_subplot(pos,projection='3d')

    marker = 'o'

    colors = [ ' ', 'r', 'c', 'y', 'g', 'b', 'm', 'k', 'ro']

    for i in range(0, len(x_val)):
        ax.scatter(x_val[i], y_val[i],z_val[i],c=colors[ids[i]])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    

def simplePlot(xTestPts, yTestPts, ids, cents):
    x_val = [x for x in xTestPts]
    y_val = [x for x in yTestPts]

    colors = [ ' ', 'r', 'c', 'y', 'g', 'b', 'm', 'k', 'ro']

    plt.figure(1)
    plt.subplot(221)
    
    for i in range(0, len(x_val)):
        plt.scatter(x_val[i], y_val[i], c=colors[ids[i]])

    #minx, maxx = checkPlotBoundaries(x_val, minx, maxx)
    #miny, maxy = checkPlotBoundaries(y_val, miny, maxy)

    #plt.axis([minx,maxx,miny,maxy])

    plt.grid(True, which='both')



def eucPlot(testPts,ids,cents):
    x_val = []
    colors = [ ' ', 'r', 'c', 'y', 'g', 'b', 'm', 'k', 'ro']
    for row in testPts:
        x_val.append([np.linalg.norm(row)])
    plt.figure(1)
    plt.subplot(223)

    for i in range(0, len(x_val)):
        
        plt.scatter(ids[i],x_val[i], c=colors[ids[i]])

    plt.grid(True, which='both')



def checkPlotBoundaries(xTestPts, minx, maxx):
    if(min(xTestPts) < minx):
        minx = min(xTestPts) - 1
    if(max(xTestPts) > maxx):
        maxx = max(xTestPts) + 1

    return minx, maxx


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
    
