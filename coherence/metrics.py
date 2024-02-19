import math
import fractions
from kendalltau import kendalltau


def abs(x):
    if x < 0:
        return -x
    else:
        return x


class Metric(object):
    """A metric on a search space."""

    def create_distance_matrix(self, vertices):
        """Returns a 2-d list of distances, this will be a symmetric matrix with
        zeros on the diagonal."""
        n = len(vertices)
        rv = [[None] * n for i in range(n)]
        for i in range(n):
            for j in range(n):
                rv[i][j] = self.distance(vertices[i], vertices[j])
        return rv

    def create_edge_list(self, vertices):
        """Returns a list of the vertices with distances and vertex indices
        (distance, vertex1, vertex2). Each edge is included only once and there
        are no self-loop edges as the distances are symmetric."""
        n = len(vertices)
        rv = [None] * (n * (n-1) // 2)
        index = 0
        for i in range(n-1):
            for j in range(i+1, n):
                rv[index] = (self.distance(vertices[i], vertices[j]), i, j)
                index += 1
        return rv

    @staticmethod
    def parse(s):
        """Converts a string representation of a metric to an instance."""
        if type(s) != str:
            raise TypeError("s should be a string")
        s = s.strip(" \t\n\r")
        tokens = [e.strip(" \t\n\r") for e in s.split(" ")]
        tokens = [e for e in tokens if len(e) != 0]
        if len(tokens) < 2:
            raise ValueError("invalid metric: \"" + s + "\"")
        if tokens[0] != "metric":
            raise ValueError("invalid metric: \"" + s + "\"")
        else:
            if len(tokens) == 2:
                if tokens[1] == "hamming":
                    return HammingDistance()
                elif tokens[1] == "manhattan":
                    return ManhattanDistance()
                elif tokens[1] == "euclidean":
                    return EuclideanDistance()
                elif tokens[1] == "maximum":
                    return MaximumNormDistance()
                elif tokens[1] == "kendalltau":
                    return KendallTauRankDistance()
                else:
                    print(s)
                    raise ValueError("invalid metric: \"" + s + "\"")
            elif len(tokens) == 3:
                if tokens[1] == "kendalltau":
                    if tokens[2] != "normalised":
                        raise ValueError("invalid metric: \"" + s + "\"")
                    return KendallTauRankDistance(True)
                elif tokens[1] == "pnorm":
                    if "/" in tokens[2]:
                        nd = tokens[2].split("/")
                        if len(nd) != 2:
                            raise ValueError("invalid metric: \"" + s + "\"")
                        n, d = tuple(nd)
                        n = int(n)
                        d = int(d)
                        return PNormDistance(fractions.Fraction(n, d))
                    elif "." in tokens[2]:
                        return PNormDistance(float(tokens[2]))
                    else:
                        return PNormDistance(int(tokens[2]))
                else:
                    raise ValueError("invalid metric: \"" + s + "\"")
            else:
                raise ValueError("invalid metric: \"" + s + "\"")


class HammingDistance(Metric):
    """A hamming metric for two bit strings. Resulting distance is an int.
    
    Example:
        metric = HammingDistance()
        metric.distance((0, 1, 1), (1, 0, 1))"""

    def distance(self, point1, point2):
        """Return the distance between two points."""
        if len(point1) != len(point2):
            print("point1 and point2 are not the same length\npoint1 (" + str(len(point1)) + ") :", str(point1), "\npoint2 (" + str(len(point2)) + ") :", str(point2))
            raise IndexError("point1 and point2 are not the same length.")
        dist = 0
        for i in range(len(point1)):
            if point1[i] == 0 and point2[i] == 0:
                pass
            elif point1[i] == 1 and point2[i] == 1:
                pass
            elif point1[i] == 0 and point2[i] == 1:
                dist += 1
            elif point1[i] == 1 and point2[i] == 0:
                dist += 1
            else:
                raise TypeError("point1 and point2 are not both bit strings")
        return dist

    def __str__(self):
        """Returns a string representation of the metric"""
        return "metric hamming"


class ManhattanDistance(Metric):
    """A mahattan (taxi cab) metric for two vectors. Resulting distance data
    type depends on the data type of the co-ordinates.
    
    Example:
        metric = ManhattanDistance()
        metric.distance((5, 42, 16, 9), (1, 10, 100, 50))
    
    Example:
        metric = ManhattanDistance()
        metric.distance((5.0, 42.0, 16.0, 9.0), (1.0, 10.0, 100.0, 50.0))"""

    def distance(self, point1, point2):
        """Return the distance between two points."""
        if len(point1) != len(point2):
            raise IndexError("point1 and point2 are not the same length")
        dist = type(point1[0])(0)
        for i in range(len(point1)):
            dist += abs(point1[i] - point2[i])
        return dist

    def __str__(self):
        """Returns a string representation of the metric"""
        return "metric manhattan"


class EuclideanDistance(Metric):
    """A Euclidean metric for two vectors. Resulting distance is a float.
    
    Example:
        metric = EuclideanDistance()
        metric.distance((1.0, 6.0), (-2.0, 2.0))
    
    Example:
        metric = EuclideanDistance()
        metric.distance((16.0, 5.25, 3.8, 63.77), (22.0, 6.0, 9.0, 10.1))"""

    def distance(self, point1, point2):
        """Return the distance between two points."""
        if len(point1) != len(point2):
            raise IndexError("point1 and point2 are not the same length")
        dist_square = 0.0
        for i in range(len(point1)):
            dist_square += (point1[i] - point2[i]) ** 2
        return math.sqrt(dist_square)

    def __str__(self):
        """Returns a string representation of the metric"""
        return "metric euclidean"


class PNormDistance(Metric):
    """A p-norm metric for a two vectors. Resulting distance is a float.
    
    Example:
        metric = PNormDistance(2)
        metric.distance((1.0, 6.0), (-2.0, 2.0))
    
    Example:
        metric = PNormDistance(1)
        metric.distance((5.0, 42.0, 16.0, 9.0), (1.0, 10.0, 100.0, 50.0))
    
    Example:
        metric = PNormDistance(2/3)
        metric.distance((10.0, 15.0), (52.0, 100.0))"""

    def __init__(self, p):
        """Return a p-norm metric p = *p*.""" 
        self.p = p

    def distance(self, point1, point2):
        """Return the distance between two points."""
        if len(point1) != len(point2):
            raise IndexError("point1 and point2 are not the same length")
        dist_p = 0.0
        for i in range(len(point1)):
            dist_p += math.sqrt((point1[i] - point2[i]) ** 2) ** self.p
        return dist_p ** (1/self.p)

    def __str__(self):
        """Returns a string representation of the metric"""
        if type(self.p) == fractions.Fraction:
            return "metric pnorm " + str(self.p.numerator) + "/" + str(self.p.denominator)
        else:
            return "metric pnorm " + str(self.p)


class MaximumNormDistance(Metric):
    """A p-norm metric for p=infinity for a two vectors. Resulting distance data
    type depends on the data type of the co-ordinates.
    
    Example:
        metric = MaximumNormDistance()
        metric.distance((1, 6), (-2, 2))
    
    Example:
        metric = MaximumNormDistance()
        metric.distance((5.0, 42.0, 16.0, 9.0), (1.0, 10.0, 100.0, 50.0))"""

    def __init__(self):
        """Return a p-norm metric p=infinity."""

    def distance(self, point1, point2):
        """Return the distance between two points."""
        if len(point1) != len(point2):
            raise IndexError("point1 and point2 are not the same length")
        return max([abs(point1[i] - point2[i]) for i in range(len(point1))])

    def __str__(self):
        """Returns a string representation of the metric"""
        return "metric maximum"


class KendallTauRankDistance(Metric):
    """A Kendall tau rank distance metric for two permutations. Resulting
    distance and in in.
    
    Example:
        metric = KendallTauRankDistance()
        metric.distance((0, 1, 2, 3, 4), (2, 3, 0, 1, 4))
    
    Example:
        metric = KendallTauRankDistance()
        metric.distance(('A', 'B', 'C', 'D', 'E'), ('C', 'D', 'A', 'B', 'E'))
    
    Example:
        metric = KendallTauRankDistance()
        metric.distance(('ABCDE'), ('CDABE'))
    
    Example:
        metric = KendallTauRankDistance(normalised=False)
        metric.distance(('ABCDE'), ('CDABE'))"""

    def __init__(self, normalised=True):
        """Return a Kendall tau distance metric, normalised by default,
        non-normalised if *normalised* is set to False.""" 
        self.normalised = normalised
    
    def distance(self, point1, point2):
        """Return the distance between two points."""
        ##items = set(point1)
        n = len(point1)
        ##n = len(items)
        ##typical = {i for i in range(n)}
        if True: ##type(point1[0]) == int and len(point1) == len(items) and len(point2) == len(items) and items == typical and set(point2) == typical:
            if self.normalised:
                inverted = kendalltau(point1, point2)
                pairs = (n * (n-1)) // 2
            else:
                return kendalltau(point1, point2)
        else:
            point1 = list(point1)
            point2 = list(point2)
            if len(set(point1)) != len(point1):
                raise TypeError("point1 is not a permutation")
            if len(set(point2)) != len(point2):
                raise TypeError("point2 is not a permutation")
            if len(point1) != len(point2):
                raise IndexError("point1 and point2 are not the same length")
            inverted = 0
            pairs = 0
            for e in point1:
                for f in point1:
                    if e != f:
                        pairs += 1
                        if point1.index(e) > point1.index(f):
                            if point2.index(e) < point2.index(f):
                                inverted += 1
                        elif point1.index(e) < point1.index(f):
                            if point2.index(e) > point2.index(f):
                                inverted += 1
        if self.normalised:
            return fractions.Fraction(inverted, pairs)
        else:
            return inverted // 2 # note: double counted, so divide by 2

    def __str__(self):
        """Returns a string representation of the metric"""
        if self.normalised:
            return "metric kendalltau normalised"
        else:
            return "metric kendalltau"
