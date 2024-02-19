import seededmetricproblems
import vertexselectors


class SeededMetricProblemGenerator(object):
    """A generator for SMP problems."""
    pass


class SpanningTreeProblemGenerator(SeededMetricProblemGenerator):
    """A generator for SMP problems based on a spanning tree."""

    @staticmethod
    def breadth_first_search(spanning_tree):
        pass

    def __init__(self, seed_generator, num_seeds, interpolation_method, interpolation_metric, tree_builder, fitness_assigner, minimise_objective=False):
        """Returns a seeded metric problem generator."""
        self.seed_generator = seed_generator
        self.num_seeds = num_seeds
        self.interpolation_method = interpolation_method
        self.interpolation_metric = interpolation_metric
        self.tree_builder = tree_builder
        self.fitness_assigner = fitness_assigner
        self.minimise_objective = minimise_objective

    def generate_problem(self):
        """Generates a seeded metric problem."""
        seeds = self.seed_generator.generate_seeds(self.num_seeds)
        spanning_tree = self.tree_builder.build_spanning_tree(seeds)
        fitnesses, optimum = self.fitness_assigner.assign_fitnesses(spanning_tree, self.minimise_objective)
        domain = self.seed_generator.get_domain()
        codomain = (min(fitnesses), max(fitnesses))
        return seededmetricproblems.SeededMetricProblem(domain,
                                                        codomain,
                                                        seeds,
                                                        fitnesses,
                                                        self.interpolation_method,
                                                        self.interpolation_metric,
                                                        self.minimise_objective,
                                                        generator="spanning tree problem generator",
                                                        spanningtreemetric=str(self.tree_builder.metric))


class SpanningTreePairProblemGenerator(SeededMetricProblemGenerator):
    """A generator for SMP problems based on a spanning tree."""

    @staticmethod
    def breadth_first_search(spanning_tree):
        pass

    def __init__(self, seed_generator, num_seeds, interpolation_method, interpolation_metric, tree_builders, fitness_assigner, minimise_objective=False, same_optimum=False):
        """Returns a seeded metric problem generator."""
        self.seed_generator = seed_generator
        self.num_seeds = num_seeds
        self.interpolation_method = interpolation_method
        self.interpolation_metric = interpolation_metric
        self.tree_builder_a, self.tree_builder_b = tree_builders
        self.fitness_assigner = fitness_assigner
        self.minimise_objective = minimise_objective
        self.same_optimum = same_optimum

    def generate_problem_pair(self):
        """Generates a seeded metric problem."""
        seeds = self.seed_generator.generate_seeds(self.num_seeds)
        spanning_tree_a = self.tree_builder_a.build_spanning_tree(seeds)
        fitnesses_a, optimum_a = self.fitness_assigner.assign_fitnesses(spanning_tree_a, self.minimise_objective)
        domain_a = self.seed_generator.get_domain()
        codomain_a = (min(fitnesses_a), max(fitnesses_a))
        rv_a = seededmetricproblems.SeededMetricProblem(domain_a,
                                                        codomain_a,
                                                        seeds,
                                                        fitnesses_a,
                                                        self.interpolation_method,
                                                        self.interpolation_metric,
                                                        self.minimise_objective,
                                                        generator="spanning tree pair problem generator",
                                                        spanningtreemetric=str(self.tree_builder_a.metric))
        spanning_tree_b = self.tree_builder_b.build_spanning_tree(seeds)
        if self.same_optimum:
            existing_vertex_selector = self.fitness_assigner.vertex_selector
            self.fitness_assigner.vertex_selector = vertexselectors.ForcedVertexSelector(optimum_a)
            fitnesses_b, optimum_b = self.fitness_assigner.assign_fitnesses(spanning_tree_b, self.minimise_objective)
            assert optimum_b == optimum_a
            self.fitness_assigner.vertex_selector = existing_vertex_selector
        else:
            fitnesses_b, optimum_b = self.fitness_assigner.assign_fitnesses(spanning_tree_b, self.minimise_objective)
        domain_b = self.seed_generator.get_domain()
        codomain_b = (min(fitnesses_b), max(fitnesses_b))
        rv_b = seededmetricproblems.SeededMetricProblem(domain_b,
                                                        codomain_b,
                                                        seeds,
                                                        fitnesses_b,
                                                        self.interpolation_method,
                                                        self.interpolation_metric,
                                                        self.minimise_objective,
                                                        generator="spanning tree pair problem generator",
                                                        spanningtreemetric=str(self.tree_builder_b.metric))
        return (rv_a, rv_b)
