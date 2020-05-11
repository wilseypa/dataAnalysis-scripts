import random as ra


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


def u_k_mers(S, k):
    ANS = []
    
    for i in range(len(S) - k + 1):

        #get the kmer starting at i
        kmer = S[i:i+k]

        #add to the kmer list
        ANS = ANS + [kmer]
    return ANS



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



def Jac(l):
    
    K = perm()

    def h(A):
        ANS = []
        count = 0
        for a in A:

            # kmers returns "weighted" (freq number)
            # with the kmers themselves.  only feed a[0]
            # for true Jaccard instead of weighted version
            x = K(a)

            #basic log-time sorted insert
            #elements of Ans are tuple (a,x)
            sorted_insert(a,x,ANS)

            #if we have seen l-items already get rid
            #of the worst one (on top because sorted)

            if count == l:
                ANS.pop()
            else:
                count = count+1

        return ANS
    return h
    

# inserts (a,x) into Ans ordered by x.
# x is in [0,1]
def sorted_insert(a,x,Ans):
    l = len(Ans)

    if l==0:
        Ans.append((a,x))
        return

    low = 0
    high = l-1
    mid = 0
    while high-low > 1:
        mid = (low + high) // 2
        if Ans[mid][1] > x:
            high = mid
        else:
            low = mid

    if Ans[low][1] > x:
        Ans.insert(low, (a,x))
    elif Ans[high][1] > x:
        Ans.insert(high, (a,x))
    else:
        Ans.insert(high+1, (a,x))




def Jac_est(s1,s2,k,l, trials):
    ans = 0
    s1 = k_mers(s1,k)
    s2 = k_mers(s2,k)
    for i in range(trials):
        h = Jac(l)
        if h(s1) == h(s2):
            ans = ans+1
    return ans / trials



def u_Jac_est(s1,s2,k,l, trials):
    ans = 0
    s1 = u_k_mers(s1,k)
    s2 = u_k_mers(s2,k)
    for i in range(trials):
        h = Jac(l)
        if h(s1) == h(s2):
            ans = ans+1
    return ans / trials


#not complete.  See sketches
def mash_Jac_est(s1,s2,k,l, S):
    ans = 0
    s1 = u_k_mers(s1,k)
    s2 = u_k_mers(s2,k)

    

    for i in range(trials):
        h = Jac(l)
        if h(s1) == h(s2):
            ans = ans+1
    return ans / trials



