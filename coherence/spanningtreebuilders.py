import unionfind


class SpanningTreeBuilder(object):
    """A method of building spanning trees on complete graphs."""
    
    def __init__(self, seeds, metric, edge_selector):
        """Returns a spanning tree builder."""
        self.seeds = seeds
        self.metric = metric
        self.edge_selector = edge_selector


class OptimisedMinSpanBuilder(SpanningTreeBuilder):
    """A builder of minimum spanning trees, optimised, does not use edge selector."""

    def __init__(self, metric):
        self.metric = metric

    def build_spanning_tree(self, seeds):
        """Returns a new spanning tree."""
        edge_list = self.metric.create_edge_list(seeds)
        edge_list.sort()
        selected_edges = set()
        uf = unionfind.UnionFind(len(seeds))
        for edge_length, vertex1, vertex2 in edge_list:
            if not uf.same_component(vertex1, vertex2):
                if vertex1 < vertex2:
                    selected_edges.add((vertex1, vertex2))
                else:
                    selected_edges.add((vertex2, vertex1))
            uf.union(vertex1, vertex2)
        return selected_edges


class OptimisedMaxSpanBuilder(SpanningTreeBuilder):
    """A builder of maximum spanning trees, optimised, does not use edge selector."""

    def __init__(self, metric):
        self.metric = metric

    def build_spanning_tree(self, seeds):
        """Returns a new spanning tree."""
        edge_list = self.metric.create_edge_list(seeds)
        edge_list.sort()
        selected_edges = set()
        uf = unionfind.UnionFind(len(seeds))
        for edge_length, vertex1, vertex2 in reversed(edge_list):
            if not uf.same_component(vertex1, vertex2):
                if vertex1 < vertex2:
                    selected_edges.add((vertex1, vertex2))
                else:
                    selected_edges.add((vertex2, vertex1))
            uf.union(vertex1, vertex2)
        return selected_edges


class PrimsSpanningTreeBuilder(SpanningTreeBuilder):
    """A spanning tree builder which decides on available edges as in Prim's algorithm. Note that the
    implementation is designed for flexibility of the edge selector and not optimised for runtime."""
    
    def __init__(self, metric, edge_selector):
        """Returns a spanning tree builder."""
        self.metric = metric
        self.edge_selector = edge_selector
    
    def build_spanning_tree(self, seeds):
        """Returns a new spanning tree."""
        edge_list = self.metric.create_edge_list(seeds)
        edge_list.sort()
        a = {0}
        b = {i for i in range(1, len(seeds))}
        selected_edges = set()
        while len(b) > 0:
            current_edges = [(w, p1, p2) for w, p1, p2 in edge_list if (p1 in a and p2 in b) or (p1 in b and p2 in a)]
            index = self.edge_selector.select_index(current_edges)
            selected_edge = current_edges[index]
            edge_length, vertex1, vertex2 = selected_edge
            if vertex1 < vertex2:
                selected_edges.add((vertex1, vertex2))
            else:
                selected_edges.add((vertex2, vertex1))
            if vertex1 in b:
                b.remove(vertex1)
                a.add(vertex1)
            else:
                b.remove(vertex2)
                a.add(vertex2)
        return selected_edges


class KruskalsSpanningTreeBuilder(SpanningTreeBuilder):
    """A spanning tree builder which decides on available edges as in Kruskal's algorithm. Note that the
    implementation is designed for flexibility of the edge selector and not optimised for runtime."""
    
    def __init__(self, metric, edge_selector):
        """Returns a spanning tree builder."""
        self.metric = metric
        self.edge_selector = edge_selector
    
    def build_spanning_tree(self, seeds):
        """Returns a new spanning tree."""
        edge_list = self.metric.create_edge_list(seeds)
        edge_list.sort()
        selected_edges = set()
        uf = unionfind.UnionFind(len(seeds))
        while len(edge_list) > 0:
            index = self.edge_selector.select_index(edge_list)
            selected_edge = edge_list[index]
            edge_length, vertex1, vertex2 = selected_edge
            if vertex1 < vertex2:
                selected_edges.add((vertex1, vertex2))
            else:
                selected_edges.add((vertex2, vertex1))
            uf.union(vertex1, vertex2)
            edge_list = [(w, p1, p2) for w, p1, p2 in edge_list if not uf.same_component(p1, p2)]
        return selected_edges

#import metrics
#import edgeselectors
#import time
#import seedgenerators
#
#seed_generator = seedgenerators.UniformIntVectorSeedGenerator([(0, 1000000), (0, 1000000)])
#seeds = seed_generator.generate_seeds(100)
#metric = metrics.EuclideanDistance()
#edge_selector = edgeselectors.MinimumEdgeSelector()
#tree_builder_1 = PrimsSpanningTreeBuilder(metric, edge_selector)
#tree_builder_2 = KruskalsSpanningTreeBuilder(metric, edge_selector)
#tree_builder_3 = OptimisedMinSpanBuilder(metric)
#
#n = 50
#
#print("Prim slow implementation    :", end=" ")
#t = time.time()
#for i in range(n):
#    tree_1 = tree_builder_1.build_spanning_tree(seeds)
#elapsed = time.time() - t
#print(elapsed / float(n))
#
#t = time.time()
#for i in range(10):
#    tree_2 = tree_builder_2.build_spanning_tree(seeds)
#elapsed = time.time() - t
#print("Kruskal slow implementation :", elapsed/1000.0)
#assert tree_1 == tree_2
#
#print("Kruskal fast implementation :", end=" ")
#t = time.time()
#for i in range(n):
#    tree_3 = tree_builder_3.build_spanning_tree(seeds)
#elapsed = time.time() - t
#print(elapsed / float(n))
#assert tree_1 == tree_3