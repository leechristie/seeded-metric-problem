import random
import numbers
import fractions
import collections
import vertexselectors


class TreeFitnessAssigner(object):
    """An assigner of fitnesses to a spanning tree."""

    @staticmethod
    def to_adjacency_list(edges):
        """Converts an edge list to an adjacency list."""
        n = vertexselectors.VertexSelector.number_of_vertices(edges)
        rv = [[] for i in range(n)]
        for v1, v2 in edges:
            rv[v1].append(v2)
            rv[v2].append(v1)
        for i in range(n):
            rv[i].sort()
        return rv

    @staticmethod
    def breadth_first_search(adjacency_list, source):
        """Counts the depths of each vertex from a source"""
        n = len(adjacency_list)
        discovered = [-1] * n;
        discovered[source] = 0
        queue = collections.deque([source])
        while len(queue) > 0:
            i = queue.popleft()
            depth = discovered[i]
            for j in adjacency_list[i]:
                if discovered[j] == -1:
                    discovered[j] = depth + 1
                    queue.append(j)
        return discovered


class RandomFloatTreeFitnessAssigner(TreeFitnessAssigner):
    """A fitness assigner of random floats."""

    def __init__(self, minimum, maximum):
        """Returns a fitness assigner"""
        self.minimum = float(minimum)
        self.maximum = float(maximum)

    def assign_fitnesses(self, spanning_tree, minimise_objective=False):
        """Assigns fitnesses"""
        n = vertexselectors.VertexSelector.number_of_vertices(spanning_tree)
        rv = [random.uniform(self.minimum, self.maximum) for i in range(n)]
        if minimise_objective:
            return rv, rv.index(min(rv))
        else:
            return rv, rv.index(max(rv))


class RandomIntTreeFitnessAssigner(TreeFitnessAssigner):
    """A fitness assigner of random floats."""

    def __init__(self, minimum, maximum):
        """Returns a fitness assigner"""
        assert isinstance(minimum, int)
        assert isinstance(maximum, int)
        self.minimum = minimum
        self.maximum = maximum

    def assign_fitnesses(self, spanning_tree, minimise_objective=False):
        """Assigns fitnesses"""
        n = vertexselectors.VertexSelector.number_of_vertices(spanning_tree)
        rv = [random.randint(self.minimum, self.maximum) for i in range(n)]
        if minimise_objective:
            return rv, rv.index(min(rv))
        else:
            return rv, rv.index(max(rv))


class RandomFractionTreeFitnessAssigner(TreeFitnessAssigner):
    """A fitness assigner of random fractions."""

    def __init__(self, minimum, maximum, increment):
        """Returns a fitness assigner"""
        assert isinstance(minimum, numbers.Rational)
        assert isinstance(maximum, numbers.Rational)
        assert isinstance(increment, numbers.Rational)
        self.minimum = fractions.Fraction(minimum)
        self.maximum = fractions.Fraction(maximum)
        self.increment = fractions.Fraction(increment)

    def assign_fitnesses(self, spanning_tree, minimise_objective=False):
        """Assigns fitnesses"""
        n = vertexselectors.VertexSelector.number_of_vertices(spanning_tree)
        total_range = self.maximum - self.minimum
        steps = total_range / self.increment
        rv = [random.randint(0, steps) * self.increment + self.minimum for i in range(n)]
        if minimise_objective:
            return rv, rv.index(min(rv))
        else:
            return rv, rv.index(max(rv))


class IntDepthTreeFitnessAssigner(TreeFitnessAssigner):
    """A fitness assigner based on a spanning tree."""

    def __init__(self, vertex_selector):
        """Returns a fitness assigner"""
        self.vertex_selector = vertex_selector

    def assign_fitnesses(self, spanning_tree, minimise_objective=False):
        """Assigns fitnesses"""
        n = vertexselectors.VertexSelector.number_of_vertices(spanning_tree)
        source = self.vertex_selector.select_index(spanning_tree)
        adj = TreeFitnessAssigner.to_adjacency_list(spanning_tree)
        depths = TreeFitnessAssigner.breadth_first_search(adj, source)
        if minimise_objective:
            rv = depths
        else:
            max_depth = max(depths)
            rv = [max_depth - e for e in depths]
        return rv, source


class FractionDepthTreeFitnessAssigner(TreeFitnessAssigner):
    """A fitness assigner based on a spanning tree."""

    def __init__(self, vertex_selector, minimum, maximum):
        """Returns a fitness assigner"""
        self.vertex_selector = vertex_selector
        assert isinstance(minimum, numbers.Rational)
        assert isinstance(maximum, numbers.Rational)
        assert maximum > minimum
        self.minimum = fractions.Fraction(minimum)
        self.maximum = fractions.Fraction(maximum)

    def assign_fitnesses(self, spanning_tree, minimise_objective=False):
        """Assigns fitnesses"""
        n = vertexselectors.VertexSelector.number_of_vertices(spanning_tree)
        source = self.vertex_selector.select_index(spanning_tree)
        adj = TreeFitnessAssigner.to_adjacency_list(spanning_tree)
        depths = TreeFitnessAssigner.breadth_first_search(adj, source)
        total_range = self.maximum - self.minimum
        max_depth = max(depths)
        depths = [fractions.Fraction(e * total_range, max_depth) + self.minimum for e in depths]
        if minimise_objective:
            rv = depths
        else:
            max_depth = max(depths)
            min_depth = min(depths)
            total_range = max_depth - min_depth
            rv = [min_depth + (total_range - (e - min_depth)) for e in depths]
        return rv, source
