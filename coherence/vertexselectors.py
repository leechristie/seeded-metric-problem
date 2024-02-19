import random


class VertexSelector(object):
    """A method of selecting spanning tree vertices from an available list of edges."""

    @staticmethod
    def number_of_vertices(edges):
        """Counts the vertices in a tree"""
        vertices = set()
        for edge in edges:
            v1, v2 = edge
            vertices.add(v1)
            vertices.add(v2)
        assert vertices == {i for i in range(len(vertices))}
        return len(vertices)


class UniformRandomVertexSelector(VertexSelector):
    """A selector which chooses vertices completely at random."""

    def select_index(self, edges):
        """Choose an index from the list of available edges."""
        n = VertexSelector.number_of_vertices(edges)
        if n == 0:
            raise IndexError("no vertices")
        return random.randint(0, n-1)


class UniformRandomLeafVertexSelector(VertexSelector):
    """A selector which chooses vertices completely at random."""

    def select_index(self, edges):
        """Choose an index from the list of available edges."""
        n = VertexSelector.number_of_vertices(edges)
        num_edges = [0] * n
        for v1, v2 in edges:
            num_edges[v1] += 1
            num_edges[v2] += 1
        with_1_edge = set()
        for i in range(len(num_edges)):
            if num_edges[i] == 1:
                with_1_edge.add(i)
        if len(with_1_edge) == 0:
            raise IndexError("no leaf vertices")
        return random.choice(list(with_1_edge))


class ForcedVertexSelector(VertexSelector):
    """A selector which chooses a preset vertex."""

    def __init__(self, vertex_id):
        self.vertex_id = vertex_id

    def select_index(self, edges):
        """Choose an index from the list of available edges."""
        n = VertexSelector.number_of_vertices(edges)
        if n > self.vertex_id:
            return self.vertex_id
        else:
            raise IndexError("Cannot force vertex " + str(self.vertex_id) + ", vertex does not exist.")

