###########################################################################################
## Transliterated from http://algs4.cs.princeton.edu/25applications/KendallTau.java.html ##
###########################################################################################

def merge(a, aux, lo, mid, hi):
    inversions = 0
    for k in range(lo, hi+1):
        aux[k] = a[k]
    i = lo
    j = mid+1
    for k in range(lo, hi+1):
        if i > mid:
            a[k] = aux[j]
            j += 1
        elif j > hi:
            a[k] = aux[i]
            i += 1
        elif aux[j] < aux[i]:
            a[k] = aux[j]
            j += 1
            inversions += mid - i + 1
        else:
            a[k] = aux[i]
            i += 1
    return inversions

def count_5(a, b, aux, lo, hi):
    inversions = 0
    if hi <= lo:
            return 0
    mid = lo + (hi - lo) // 2
    inversions += count_5(a, b, aux, lo, mid)
    inversions += count_5(a, b, aux, mid+1, hi)
    inversions += merge(b, aux, lo, mid, hi)
    return inversions

def count_1(a):
    b = [0] * len(a)
    aux = [0] * len(a)
    for i in range(len(a)):
        b[i] = a[i]
    inversions = count_5(a, b, aux, 0, len(a) - 1)
    return inversions

def kendalltau(x,y):
    N = len(x)
    ainv = [0] * N
    for i in range(N):
        ainv[x[i]] = i
    bnew = [0] * N
    for i in range(N):
        bnew[i] = ainv[y[i]]
    return count_1(bnew)