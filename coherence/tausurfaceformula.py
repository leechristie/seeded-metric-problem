from scipy import special
from weightedchoice import cumulative_weights


class Memo2(object):

    def __init__(self, f):
        self.f = f
        self.memo = [[None] * int(special.binom(n, 2)+1) for n in range(101)]

    def __call__(self, n, k):
        if n < 0:
            return 0
        elif k < 0:
            return 0
        elif n >= len(self.memo):
            raise NotImplementedError
        elif k >= len(self.memo[n]):
            return 0
        elif self.memo[n][k] is not None:
            return self.memo[n][k]
        else:
            value = self.f(n, k)
            self.memo[n][k] = value
            return value


class Memo3(object):

    def __init__(self, f):
        self.f = f
        self.memo = [None for n in range(101)]

    def __call__(self, n):
        if n < 0:
            return 0
        elif n >= len(self.memo):
            raise NotImplementedError
        elif self.memo[n] is not None:
            return self.memo[n]
        else:
            value = self.f(n)
            self.memo[n] = value
            return value


@Memo2
def points_on_surface_of_kendal_tau(dimensions, radius):
    if dimensions < 0:
        return 0
    elif radius < 0:
        return 0
    elif radius == 0:
        return 1
    elif radius > int(special.binom(dimensions, 2)):
        return 0
    elif dimensions == 1 and radius == 1:
        return 1
    elif dimensions == 1:
        return 0
    else:
        return points_on_surface_of_kendal_tau(dimensions-1, radius)\
               + points_on_surface_of_kendal_tau(dimensions, radius-1)\
               - points_on_surface_of_kendal_tau(dimensions-1,
                                                 radius-dimensions)


KT_WEIGHTS = [None for n in range(101)]
KT_CUMULATIVE = [None for n in range(101)]
for n in range(101):
    KT_WEIGHTS[n] = [None] * int(special.binom(n, 2)+1)
    for r in range(int(special.binom(n, 2)+1)):
        KT_WEIGHTS[n][r] = points_on_surface_of_kendal_tau(n, r)


def kt_weights(dimension):
    global KT_WEIGHTS
    assert dimension >= 0
    if dimension >= len(KT_WEIGHTS):
        raise NotImplementedError
    return KT_WEIGHTS[dimension]


@Memo3
def kt_cumulative(dimension):
    return cumulative_weights(KT_WEIGHTS[dimension])


def main():
    global KT_WEIGHTS
    global KT_CUMULATIVE
    for n in range(0, 11):
        print(n, end=":\t")
        for k in range(int(special.binom(n, 2)) + 1):
            print("\t", points_on_surface_of_kendal_tau(n, k), sep="", end="")
        print()
    for n in range(0, 11):
        print(n, end=":\t")
        for k in range(int(special.binom(n, 2)) + 1):
            print("\t", KT_WEIGHTS[n][k], sep="", end="")
        print()
    for n in range(0, 11):
        print(n, ":\t", str(), kt_weights(n), sep="")
    import math
    for n in range(0, 11):
        print(n, ":\t", str(), kt_cumulative(n), sep="")



if __name__ == "__main__":
    main()
