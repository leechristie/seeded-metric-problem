import random


class EdgeSelector(object):
    """A method of selecting spanning tree edges from an available list."""


class MinimumEdgeSelector(EdgeSelector):
    """A selector for the smallest edges."""
    
    def select_index(self, sorted_edges):
        """Choose an index from the list of available edges."""
        if len(sorted_edges) == 0:
            raise IndexError("sorted_edges is empty")
        return 0


class MaximumEdgeSelector(EdgeSelector):
    """A selector for the smallest edges."""
    
    def select_index(self, sorted_edges):
        """Choose an index from the list of available edges."""
        if len(sorted_edges) == 0:
            raise IndexError("sorted_edges is empty")
        return len(sorted_edges) - 1


class OrderStatisticEdgeSelector(EdgeSelector):
    """A selector which chooses edges from the minimum if *p* = 0.0, maximum if
    *p* = 1.0 and in between when 0.0 < *p* < 1.0, e.g. the median edge if
    *p* = 0.5. Note that this uses floating point rounding to pick the index."""

    def __init__(self, p):
        """Return an order-statistic edge selector for p = *p*."""
        if p < 0.0 or p > 1.0:
            raise ValueError("p = " + str(p) + ", expected 0.0 < p < 1.0")
        self.p = p

    def select_index(self, sorted_edges):
        """Choose an index from the list of available edges."""
        if len(sorted_edges) == 0:
            raise IndexError("sorted_edges is empty")
        return round((len(sorted_edges) - 1) * self.p)


class RandomMinimumMaximumEdgeSelector(EdgeSelector):
    """A selector which chooses the maximum edge with probability *p* otherwise
    chooses the minimum edge."""

    def __init__(self, p):
        """Return a random minimum/maximum edge selector for p = *p*."""
        if p < 0.0 or p > 1.0:
            raise ValueError("p = " + str(p) + ", expected 0.0 < p < 1.0")
        self.p = p

    def select_index(self, sorted_edges):
        """Choose an index from the list of available edges."""
        if len(sorted_edges) == 0:
            raise IndexError("sorted_edges is empty")
        if self.p <= random.random():
            return 0
        else:
            return len(sorted_edges) - 1


class UniformRandomEdgeSelector(EdgeSelector):
    """A selector which chooses edges completely at random."""

    def select_index(self, sorted_edges):
        """Choose an index from the list of available edges."""
        if len(sorted_edges) == 0:
            raise IndexError("sorted_edges is empty")
        return random.randint(0, len(sorted_edges)-1)
