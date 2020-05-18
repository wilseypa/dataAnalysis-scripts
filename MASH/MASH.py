
# ANI is baseline for MASH results
# IMPORTANT:   AS an estimator, the gapped 
#  might not be a good approx.  Check paper
#  BUT!!!!!   For streaming TDA?????
#  Being able to change L and k while 
#  knowing the effects this will have!
#  HUGE!!!
#




import time
import helper
from os.path import exists
import math
from math import log
import numpy as np
import jac
from jac import sorted_insert


dist_file = 'datasets/rightDistMat.csv'
ofile = 'output/concatUnaligned_s{}_c{}_k{}.csv'
in_file = 'concatUnaligned.fa'

def import_files(If, Df=''):
    P = helper.parse_gene_file( in_file )[1:]
    D = []
    if Df:
        D = helper.parse_num_file( dist_file )
    
    return P,D


def sketch( S, s, c, k, h ):
    Dict = {}
    ANS = []
    MAX = 9999999
    #loop over all kmers
    for i in range(len(S) - k + 1):
            
        #get the kmer starting at i
        kmer = S[i:i+k]

        v = h(kmer)
        if v < MAX:

            # Basic frequency dictionary...
            if kmer in Dict:
                #If seen, increment
                x = Dict[kmer]
                Dict[kmer] = x+1
            else:
                #If not yet seen add to dict
                Dict[kmer] = 1
                x = 0
            
            if x == c-1: # make this >= for multiple of same kmer?
                
                #add to the kmer list
                sorted_insert(kmer, v, ANS)
                while len(ANS) > s:
                    ANS.pop()
                    MAX = ANS[s-1][1]
    return ANS


def dist( s1, s2, s, c, k):
    h = jac.perm()
    
    Sk1 = sketch(s1, s, c, k, h)
    Sk2 = sketch(s2, s, c, k, h)

    return mash_jac( Sk1, Sk2, s)

def mash_jac(sk1, sk2, s):
    Sk1 = [ stuff for stuff in sk1 ]
    Sk2 = [ stuff for stuff in sk2 ]
    
    count = 0
    hits = 0
    while Sk1 and Sk2 and count < s:
        count = count+1
        x,y = Sk1[0], Sk2[0]
        if x == y:
            Sk1.pop(0)
            Sk2.pop(0)
            hits = hits+1
        elif x[1] > y[1]:
            Sk2.pop(0)
        else:
            Sk1.pop(0)
    if not Sk1:
        Sk1 = Sk2

    while count<s and Sk1:
        count = count+1
        Sk1.pop(0)

    if count==0:
        return count

    return hits / count

def mash_D(k,j):
    if j==0:
        return j
    return (-1/k) * math.log( 2*j/(1+j) )


def get_k(n, q, alph_size=4):
   x = log( n*(1-q)/q ) / log(alph_size)
   if x == int(x):
       return int(x)
   return int(x)+1


def comp_dists( size, s, c, k ):
    P, D = import_files(in_file, dist_file)
    
    SIZE = range( size )

    sketches = []
    dists = [[-1 for l in SIZE ] for k in SIZE]

    out = 'loc: ({}, {})\nJac est: {}\ndist: {}\nactual: {}\n\n'

    q = .001
    
    h = jac.perm()

    for x in SIZE:
        #  k = get_k( len(P[x]), q, 4)  Do this????
        sketches.append( sketch( P[x], s, c, k, h ) )
    

    for x in SIZE:
        for y in range( x + 1 ):
            Sk1,Sk2 = sketches[x], sketches[y]
            
            v = mash_jac( Sk1, Sk2, s)
            n = min( len(P[x]), len(P[y]) )

            k = get_k( n, q, 4 )
            d = mash_D(k, v)
            
            dists[x][y] = d
            dists[y][x] = d

    return dists

def disp(dists, D):
    for x in range(len(dists)):
        s = ''
        for y in range(len(dists[x])):
            v = D[x][y] - dists[x][y]
            s= s+ str(v) + ', '
        print(s)

def query(dists, D):
    x = int(input())
    y = int(input())

    s = 'hash: {}, actual: {}'.format(dists[x][y], D[x][y])
    print(s)


def test2():
    P,D = import_files(in_file, dist_file)
    print( P[1] )

    time_file = open('output/times.txt','w')
    time_line = '{} ---->  {} '
    
    # 4^12  =  16777216
    # len   =  4500
    S,C,K = range(1000,8500,1000),[2,1],[4,8,12,16,20,24,28]
        
    for k in K:
        for c in C:
            for s in S:
                start = time.time()
                
                out_fp = ofile.format(s,c,k)
                g = open(out_fp, 'w')

                
                dists = comp_dists( len(P), s, c, k)
                

                taken = time.time() - start
                mess = time_line.format(out_fp, taken)
                time_file.write(mess)
                print(mess)

                for d in dists:
                    s =''
                    for elem in d:
                        s = s + str(elem) + ','
                    g.write(s[:-1] + '\n')
                g.close()

    time_file.close()

test2()

def test():
    g = open('output/umJac_100_1000.txt', 'w')
    P, D = import_files()
    for y in range(len(P)):
        s1 = P[0]
        s2 = P[y]
        
        k = 10
        j = jac.Jac_est( s1, s2, k, 1, 1000)
        u_j = jac.u_Jac_est( s1, s2, k, 1, 1000)
        m_j = dist( s1, s2, 100, 1, k)

        s = 'jac: {}, ujac: {}\nmjac: {}\nMASH: {}, uMASH: {}\nmMASH: {}\nreal: {}\n'
        s = s.format(1 - j ,1 - u_j, 1-m_j, mash_D(k,j), mash_D(k,u_j), mash_D(k,m_j), D[0][y] )
        print(s)
        g.write(s)



