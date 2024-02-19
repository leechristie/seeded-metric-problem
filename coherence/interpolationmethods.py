import fractions
import numbers
import time

def are_rational(s):
    for e in s:
        if not isinstance(e, numbers.Rational):
            return False
    return True


class InterpolationMethod(object):
    """A method of interpolation for points given a set of seed solutions."""

    @staticmethod
    def parse(s):
        """Converts a string representation of a metric to an interpolation metric."""
        if type(s) != str:
            raise TypeError("s should be a string")
        s = s.strip(" \t\n\r")
        tokens = [e.strip(" \t\n\r") for e in s.split(" ")]
        tokens = [e for e in tokens if len(e) != 0]
        if len(tokens) not in {2, 3, 4}:
            raise ValueError("invalid interpolation method: \"" + s + "\"")
        if tokens[0] != "interpolation":
            raise ValueError("invalid interpolation method: \"" + s + "\"")
        else:
            if len(tokens) == 2:
                if tokens[1] == "nearestneighbour":
                    return NearestNeighbourInterpolationMethod()
                else:
                    raise ValueError("invalid interpolation method: \"" + s + "\"")
            elif len(tokens) == 3:
                if tokens[1] == "inversedistanceweighting":
                    if "/" in tokens[2]:
                        nd = tokens[2].split("/")
                        if len(nd) != 2:
                            raise ValueError("invalid interpolation method: \"" + s + "\"")
                        n, d = tuple(nd)
                        n = int(n)
                        d = int(d)
                        return InverseDistanceWeightingInterpolationMethod(fractions.Fraction(n, d))
                    elif "." in tokens[2]:
                        return InverseDistanceWeightingInterpolationMethod(float(tokens[2]))
                    else:
                        return InverseDistanceWeightingInterpolationMethod(int(tokens[2]))
                else:
                    raise ValueError("invalid interpolation method: \"" + s + "\"")
            elif len(tokens) == 4:
                if tokens[1] == "inversedistanceweighting":
                    if "/" in tokens[2]:
                        nd = tokens[2].split("/")
                        if len(nd) != 2:
                            raise ValueError("invalid interpolation method: \"" + s + "\"")
                        n, d = tuple(nd)
                        n = int(n)
                        d = int(d)
                        return InverseDistanceWeightingInterpolationMethod(fractions.Fraction(n, d), int(tokens[3]))
                    elif "." in tokens[2]:
                        return InverseDistanceWeightingInterpolationMethod(float(tokens[2]), int(tokens[3]))
                    else:
                        return InverseDistanceWeightingInterpolationMethod(int(tokens[2]), int(tokens[3]))
                else:
                    raise ValueError("invalid interpolation method: \"" + s + "\"")
            else:
                raise ValueError("invalid interpolation method: \"" + s + "\"")


class NearestNeighbourInterpolationMethod(InterpolationMethod):
    """Method to use the nearest neighbour interpolation."""

    def interpolate(self, candidate, seeds, fitnesses, metric):
        """Returns the interpolated fitness of the specified candidate."""
        if len(candidate) == 0:
            raise IndexError("no candidates")
        lowest_distance = None
        nearest_neighbour_index = None
        for i in range(len(candidate)):
            distance = metric.distance(candidate, seeds[i])
            if lowest_distance is None or distance < lowest_distance:
                lowest_distance = distance
                nearest_neighbour_index = i
        return fitnesses[nearest_neighbour_index]

    def __str__(self):
        """Returns a string representation of the interpolation method"""
        return "interpolation nearestneighbour"


class InverseDistanceWeightingInterpolationMethod(InterpolationMethod):
    """Method to use the inverse distance weighting interpolation."""

    def __init__(self, p, n=None):
        """Returns an IDW interpolation metric with p value *p*, and optionally restricted to the nearest *n* seeds."""
        self.p = p
        if n is not None:
            if type(n) != int:
                raise TypeError("n should be int or None")
            if n < 2:
                raise ValueError("n < 2")
        self.n = n

    @staticmethod
    def nearest(candidate, seeds, metric, n):
        """Returns the list of *n* nearest seeds"""
        indices = [None] * len(seeds)
        for i in range(len(seeds)):
            indices[i] = (metric.distance(candidate, seeds[i]), i)
        indices.sort()
        used_seeds = [None] * n
        for i in range(n):
            distance, index = indices[i]
            used_seeds[i] = seeds[index]
        return used_seeds

    def interpolate(self, candidate, seeds, fitnesses, metric):
        """Returns the interpolated fitness of the specified candidate."""
        if self.n is None:
            used_seeds = seeds
            if len(seeds) < 2:
                raise IndexError("fewer than 2 seeds")
        else:
            if len(seeds) < self.n:
                raise IndexError("fewer than " + str(self.n) + " seeds")
            used_seeds = InverseDistanceWeightingInterpolationMethod.nearest(candidate, seeds, metric, self.n)
        for i in range(len(used_seeds)):
            if metric.distance(candidate, used_seeds[i]) == 0:
                return fitnesses[seeds.index(used_seeds[i])]
        sum_top = fractions.Fraction(0)
        sum_bottom = fractions.Fraction(0)
        for seed in used_seeds:
            i = seeds.index(seed)
            distance = metric.distance(candidate, seed)
            if are_rational({fitnesses[i], sum_top, self.p, distance}):
                inc_den = distance ** self.p
                if isinstance(inc_den, numbers.Rational):
                    sum_top += fractions.Fraction(fitnesses[i], inc_den)
                else:
                    sum_top += fitnesses[i] / inc_den
            else:
                sum_top += fitnesses[i] / (distance ** self.p)
            if are_rational({fitnesses[i], sum_bottom, self.p, distance}):
                inc_den = distance ** self.p
                if isinstance(inc_den, numbers.Rational):
                    sum_bottom += fractions.Fraction(1, inc_den)
                else:
                    sum_bottom += 1 / inc_den
            else:
                sum_bottom += 1 / (distance ** self.p)
        if are_rational({sum_top, sum_bottom}):
            rv = fractions.Fraction(sum_top, sum_bottom)
        else:
            rv = sum_top / sum_bottom
        return rv

    def __str__(self):
        """Returns a string representation of the interpolation method"""
        if self.n is None:
            if type(self.p) == fractions.Fraction:
                return "interpolation inversedistanceweighting " + str(self.p.numerator) + "/" + str(self.p.denominator)
            else:
                return "interpolation inversedistanceweighting " + str(self.p)
        else:
            if type(self.p) == fractions.Fraction:
                return "interpolation inversedistanceweighting " + str(self.p.numerator) + "/" + str(self.p.denominator) + " " + str(self.n)
            else:
                return "interpolation inversedistanceweighting " + str(self.p) + " " + str(self.n)

#test = InverseDistanceWeightingInterpolationMethod(1, 2)
#from metrics import *
#seeds = ([1, 0, 0], [1, 0, 1], [0, 1, 1])
#fitnesses = (5, 7, 11)
#metric = HammingDistance()
#print("000", test.nearest([0, 0, 0], seeds, metric, 2), test.interpolate([0, 0, 0], seeds, fitnesses, metric), sep="\t")
#print("100", test.nearest([1, 0, 0], seeds, metric, 2), test.interpolate([1, 0, 0], seeds, fitnesses, metric), sep="\t")
#print("010", test.nearest([0, 1, 0], seeds, metric, 2), test.interpolate([0, 1, 0], seeds, fitnesses, metric), sep="\t")
#print("110", test.nearest([1, 1, 0], seeds, metric, 2), test.interpolate([1, 1, 0], seeds, fitnesses, metric), sep="\t")
#print("001", test.nearest([0, 0, 1], seeds, metric, 2), test.interpolate([0, 0, 1], seeds, fitnesses, metric), sep="\t")
#print("101", test.nearest([1, 0, 1], seeds, metric, 2), test.interpolate([1, 0, 1], seeds, fitnesses, metric), sep="\t")
#print("011", test.nearest([0, 1, 1], seeds, metric, 2), test.interpolate([0, 1, 1], seeds, fitnesses, metric), sep="\t")
#print("111", test.nearest([1, 1, 1], seeds, metric, 2), test.interpolate([1, 1, 1], seeds, fitnesses, metric), sep="\t")
