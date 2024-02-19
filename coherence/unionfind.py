class UnionFind(object):
    """A simple union-find data structure."""

    def __init__(self, n):
        """Returns a union-find data structure."""
        self.n = n
        self.leaders = [i for i in range(n)]
        self.component_size = [1 for i in range(n)]

    def union(self, i, j):
        """Unions indices *i* and *j*."""
        leader_of_i = self.find(i)
        size_of_set_of_i = self.component_size[leader_of_i]
        leader_of_j = self.find(j)
        size_of_set_of_j = self.component_size[leader_of_j]
        if size_of_set_of_i > size_of_set_of_j:
            self.leaders[leader_of_j] = self.leaders[leader_of_i]
        else:
            self.leaders[leader_of_i] = self.leaders[leader_of_j]
        new_size = size_of_set_of_i + size_of_set_of_j
        self.component_size[leader_of_i] = new_size
        self.component_size[leader_of_j] = new_size

    def find(self, i):
        """Find the partition ID for index *i*."""
        index = i
        while self.leaders[index] != index:
            index = self.leaders[index]
        return index

    def same_component(self, i, j):
        """Determines whether *i* and *j* are in the same partition."""
        return self.find(i) == self.find(j)

    def __str__(self):
        """Returns a string representation of the the state of the union-find
        data structure for testing purposes."""
        leaders = self.leaders
        found = [self.find(i) for i in range(self.n)]
        return "pointers : " + str(leaders) + ", IDs : " + str(found) + "; " + str(len(set(found))) + " components"
