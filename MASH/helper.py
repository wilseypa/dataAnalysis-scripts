import random as ra
import math
import numpy as np


# sigma funciton
def sigma(i,j):
    return 1 if i==j else 0

# dot product
def DP(v,p):
    return sum(i[0] * i[1] for i in zip(v, p))


# shift vector by scalar factor
def shift(c,X):
    return [x+c for x in X]

# vector linear sum of A and B with coef. C
def linear(A,C,B):
    return [A[i]*C[i]+B[i] for i in range(len(A))]

#vector sum
def v_sum(X,Y):
    return [X[i]+Y[i] for i in range(len(X))]

def distfunction(x,y):
    ans = 0
    for i in range(len(x)):
        S = x[i] - y[i]
        ans = ans + S*S
    return math.sqrt(ans)


# print Index-Value array contents
def disp_arr(A):
    for i in range(len(A)):
        print("i = {}, v = {}".format(A[i].index, A[i].value))

# parse standard csv line
def parse(line):
    #s = line.split(',')
    #return [float(g) for g in s]
    return line.strip()

def parse_num(line):
    s = line.split(',')
    return [float(g) for g in s]


# parse standard csv line (numpy)
def np_parse(line):
    return np.array(parse(line))

def numpy_parse_file(f):
    return np.loadtxt(f, delimiter=',')

# parse standard csv file
def parse_file(f):
    P = []
    with open(f) as g:
        P = [parse(l) for l in g]
    return P

def parse_gene_file(f):
    P = []
    S = open(f, 'r').read()
    S = S.split('>')
    #print(len(S))

    for s in S:
        x = s.split('\n')[1:]
        p = ''.join(x).replace(' ','')
        P = P + [p]
    
    return P


def parse_num_file(f):
    P = []
    with open(f) as g:
        P = [parse_num(l) for l in g]
    return P


# parse standard csv file (numpy)
def np_parse_file(f):
    P = []
    with open(f) as g:
        P = [parse(l) for l in g]
    return P

def write_clusters(lbls, f):
    g = open(f, 'w')
    for l in lbls:
        g.write(str(l) + '\n')

    g.close()


# dice roll
def rand(N):
    x = ra.random()
    return int(int(N)*x)


def insert(Array, index, value):
    mn,mx = 0,len(Array)-1

    if Array == [] or value > Array[mx][1]:
        Array.append([index, value])
        return

    while mn < mx:
        mid = (mn + mx)//2
        if mid == mn:
            break

        if value > Array[mid][1]:
            mn = mid
        elif value < Array[mid][1]:
            mx = mid
        else:
            mn,mx = mid,mid

    Array.insert(mn, [index,value])


# Generates a permutation data structure on some
# unspecified (possibly changing) universe of 
# elements.  Originally this was perm(U) to fit
# the feel of the definition in Marcais but I
# found that specifying our universe is not needed
def perm():
    vals = []
    Dict = {}
    def K(x):
        if x in Dict:
            return Dict[x]
        Dict[x] = ra.random()
        return Dict[x]
    return K


# gets k-mers but not with weight S is the 
# string input, k is the length of the kmers
def k_mers(S, k):

    #Dict is (kmer -> frequency in S)
    Dict = {}
    Ans = []

    #loop over all kmers
    for i in range(len(S) - k + 1):

        #get the kmer starting at i
        kmer = S[i:i+k]

        # Basic frequency dictionary...
        if kmer in Dict:
            #If seen, increment
            x = Dict[kmer]
            Dict[kmer] = x+1
        else:
            #If not yet seen add to dict
            Dict[kmer] = 1
            x = 0

        #add to the kmer list
        Ans = Ans + [(kmer, x)]
    return Ans


#Older Jaccard. Just returns lowest hash 
def Jac_no_L(Args):
    K = perm()
    def h(A):
        A = k_mers(A,Args[0])
        
        min_hash = -1
        min_val = 9999999
        for a in A:
            
            # kmers returns "weighted" (freq number)
            # with the kmers themselves.  only feed a[0]
            # for true Jaccard instead of weighted version
            x = K(a)
            
            
            
            if x < min_val:
                min_val = x
                min_hash = a
        return min_hash[0]
    return h




