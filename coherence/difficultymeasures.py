import random
from spanningtreebuilders import OptimisedMinSpanBuilder
from metrics import Metric
from vertexselectors import ForcedVertexSelector
from treefitnessassigners import IntDepthTreeFitnessAssigner
from numbers import Rational
from stats import correlation_coefficient, concordance, descriptive_statistics


class DifficultyMeasure(object):
    """A measure of problem difficulty."""

    def measure(self):
        """Runs the difficulty measure once on the function and returns the result. To be over-ridden by subclass."""
        raise(NotImplementedError("To be over-ridden by subclass."))


class Dispersion(DifficultyMeasure):
    """Dispersion measure difficulty measure."""

    def __init__(self, num_points, threshold, maximization_objective, metric, problem, generator):
        assert isinstance(num_points, int)
        assert num_points >= 2
        self.num_points = num_points
        assert isinstance(threshold, float)
        assert 0.0 <= threshold <= 1.0
        self.threshold = threshold
        assert isinstance(maximization_objective, bool)
        self.maximization_objective = maximization_objective
        assert isinstance(metric, Metric)
        self.maximization_objective = maximization_objective
        self.metric = metric
        assert hasattr(problem, '__call__')
        self.problem = problem
        assert hasattr(generator, '__call__')
        self.generator = generator

    def measure(self):
        """Runs the difficulty measure once on the function and returns the result."""
        points = self.generator(self.num_points)
        randoms = set()
        while len(randoms) < len(points):
            randoms.add(random.random())
        randoms = list(randoms)
        points = [(self.problem(points[i]), randoms[i], points[i]) for i in range(len(points))]
        points.sort()
        if self.maximization_objective:
            points.reverse()
        points = [e[2] for e in points]
        pairWiseDist = 0.0
        bestSample = int(round(self.num_points * self.threshold))
        counts = 0
        for i in range(bestSample-1):
            for j in range(i+1, bestSample):
                pairWiseDist += self.metric.distance(points[i], points[j])
                counts += 1
        return pairWiseDist / counts


class SpanningTreeCorrelation(DifficultyMeasure):

    def __init__(self, num_points, metric, problem, generator):
        assert isinstance(num_points, int)
        assert num_points >= 2
        self.num_points = num_points
        assert isinstance(metric, Metric)
        self.metric = metric
        assert hasattr(problem, '__call__')
        self.problem = problem
        assert hasattr(generator, '__call__')
        self.generator = generator

    def measure(self):
        seeds = list(self.generator(self.num_points))
        builder = OptimisedMinSpanBuilder(self.metric)
        min_span_tree = builder.build_spanning_tree(seeds)
        actual_fitnesses = [self.problem(seed) for seed in seeds]
        index_highest = actual_fitnesses.index(max(actual_fitnesses))
        vertex_selector = ForcedVertexSelector(index_highest)
        fitness_asigner = IntDepthTreeFitnessAssigner(vertex_selector)
        fitnesses_by_tree, optimum = fitness_asigner.assign_fitnesses(min_span_tree, True)
        assert index_highest == optimum
        return correlation_coefficient(fitnesses_by_tree, actual_fitnesses)


class SpanningTreeConcordance(DifficultyMeasure):

    def __init__(self, num_points, metric, problem, generator):
        assert isinstance(num_points, int)
        assert num_points >= 2
        self.num_points = num_points
        assert isinstance(metric, Metric)
        self.metric = metric
        assert hasattr(problem, '__call__')
        self.problem = problem
        assert hasattr(generator, '__call__')
        self.generator = generator

    def measure(self):
        seeds = list(self.generator(self.num_points))
        builder = OptimisedMinSpanBuilder(self.metric)
        min_span_tree = builder.build_spanning_tree(seeds)
        actual_fitnesses = [self.problem(seed) for seed in seeds]
        index_highest = actual_fitnesses.index(max(actual_fitnesses))
        vertex_selector = ForcedVertexSelector(index_highest)
        fitness_asigner = IntDepthTreeFitnessAssigner(vertex_selector)
        fitnesses_by_tree, optimum = fitness_asigner.assign_fitnesses(min_span_tree, True)
        assert index_highest == optimum
        #return correlation_coefficient(fitnesses_by_tree, actual_fitnesses)
        return concordance(fitnesses_by_tree, actual_fitnesses)


class FitnessDistanceCorrelation(DifficultyMeasure):

    def __init__(self, problem, global_optimum, optimum_fitness, num_evals, generator, metric):
        assert hasattr(problem, '__call__')
        self.problem = problem
        assert isinstance(length, int)
        self.length = length
        assert hasattr(global_optimum, '__iter_') or hasattr(global_optimum, '__getitem__')
        assert len(global_optimum) == length
        self.global_optimum = global_optimum
        assert isinstance(optimum_fitness, Rational)
        self.optimum_fitness = optimum_fitness
        assert isinstance(num_evals, int)
        assert num_evals > 0
        self.num_evals = num_evals
        assert hasattr(generator, '__call__')
        self.generator = generator
        assert isinstance(metric, Metric)
        self.metric = metric

    def measure(self):
        fitnesses = [None] * self.num_evals
        distances = [None] * self.num_evals
        average_distance = 0
        average_fitness = 0
        sample = list(self.generator(self.num_evals, blacklist = frozenset({tuple(self.global_optimum)})))
        for i in range(self.num_evals):
            fitnesses[i] = self.problem(sample[i])
            distances[i] = self.metric.distance(sample[i], self.global_optimum)
            average_distance += distances[i]
            average_fitness += fitnesses[i]
        stats_distance = descriptive_statistics(distances)
        stats_fitness = descriptive_statistics(fitnesses)
        stdev_distance = stats_distance['stdev']
        stdev_fitness = stats_fitness['stdev']
        avg_distance = stats_distance['mean']
        avg_fitness = stats_fitness['mean']
        correlation = (1 / self.num_evals) * sum([(fitnesses[i] - avg_fitness) * (distances[i] - avg_distance) for i in range(num_evals)])
        if stdev_distance * stdev_fitness == 0:
            return float('inf')
        else:
            return correlation / (stdev_distance * stdev_fitness)


if __name__ == "__main__":
    from seededmetricproblems import SeededMetricProblem
    def smp_as_benchmark(smp_instance):
        assert isinstance(smp_instance, SeededMetricProblem)
        class wrapper(BenchmarkFunction):
            def __init__(self, smp_instance):
                assert isinstance(smp_instance, SeededMetricProblem)
                self.smp_instance = smp_instance
                self.seeds = self.smp_instance.seeds
                self.fitnesses = self.smp_instance.fitnesses
                if smp_instance.minimise_objective:
                    best_f = min(self.fitnesses)
                else:
                    best_f = max(self.fitnesses)
                assert self.fitnesses.count(best_f) == 1
                best_i = self.fitnesses.index(best_f)
                best_x = self.seeds[best_i]
                self.opt = best_x
                self.fit = best_f
            def __call__(self, x):
                return self.smp_instance.evaluate(x)
            def global_optima(self):
                return [self.opt]
            def optimum_value(self):
                return self.fit
        rv = wrapper(smp_instance)
        return rv
    from seedgenerators import UniformBitStringSeedGenerator
    from metrics import HammingDistance
    def short(optimum):
        string = str(optimum)
        if len(string) < 53:
            return string
        else:
            return string[:50] + "..."
    from benchmarks import BenchmarkFunction, suite_100

    #suite = suite_100()

    #minspan_instance = SeededMetricProblem.load("../instances-bit-string-hamming/bit-string-hamming-seeds50-len100-inst0-minspan.smp")
    #maxspan_instance = SeededMetricProblem.load("../instances-bit-string-hamming/bit-string-hamming-seeds50-len100-inst0-maxspan.smp")
    #suite = {'Min Span Instance (Bit String Hamming Len 100 Inst 0)': smp_as_benchmark(minspan_instance),
    #         'Max Span Instance (Bit String Hamming Len 100 Inst 0)': smp_as_benchmark(maxspan_instance)}

    suite = {}
    for i in range(10):
        minspan_instance = SeededMetricProblem.load("../instances-bit-string-hamming/bit-string-hamming-seeds50-len100-inst" + str(i) + "-minspan.smp")
        maxspan_instance = SeededMetricProblem.load("../instances-bit-string-hamming/bit-string-hamming-seeds50-len100-inst" + str(i) + "-maxspan.smp")
        suite['Min Span Instance (Bit String Hamming Len 100 Inst ' + str(i) + ')'] = smp_as_benchmark(minspan_instance)
        suite['Max Span Instance (Bit String Hamming Len 100 Inst ' + str(i) + ')'] = smp_as_benchmark(maxspan_instance)

    max_optima = 4
    num_evals = 1000
    num_samples = 100
    length = 100
    generator = UniformBitStringSeedGenerator(length).generate_seeds
    metric = HammingDistance()
    for name in sorted(suite):
        print("Problem :", name)
        problem = suite[name]
        assert isinstance(problem, BenchmarkFunction)
        opt_fitness = problem.optimum_value()
        print("Optimum Fitness :", opt_fitness)
        num_optima = problem.global_optima().__len__()
        print("Num. Global Optima :", num_optima)
        optima_done = 0
        for optimum in problem.global_optima():
            optima_done += 1
            print("Optima", optima_done, "of", num_optima, ":", short(optimum))
            measure = FitnessDistanceCorrelation(problem, optimum, opt_fitness, num_evals, generator, metric)
            print("Mean FDC :", end = " ", flush = True)
            sample = [measure.measure() for i in range(num_samples)]
            stat = descriptive_statistics(sample)
            print(stat['mean'])
            print("Stdev FDC :", stat['stdev'])
            if optima_done == max_optima and num_optima > max_optima:
                print("Stopping at", max_optima, "optima!")
                break
        print("\n")


if __name__ == "__main__" and 0 == 1:

    from benchmarks import BenchmarkFunction, suite_100
    from metrics import HammingDistance
    from seedgenerators import UniformBitStringSeedGenerator
    from stats import descriptive_statistics

    def run_measure(measure, samples, name):
        print(name, "(n) :", samples)
        print(name, "(Mean) : ", end="", flush=True)
        summary = descriptive_statistics([measure.measure() for i in range(samples)])
        print(summary['mean'])
        print(name, "(Stdev) :", summary['stdev'])
        print(name, "(Min) :", summary['min'])
        print(name, "(Median) :", summary['median'])
        print(name, "(Max) :", summary['max'])
        print()

    suite = suite_100()

    #from seededmetricproblems import SeededMetricProblem

    #minspan_instance = SeededMetricProblem.load("../instances-bit-string-hamming/bit-string-hamming-seeds50-len100-inst0-minspan.smp").evaluate

    #maxspan_instance = SeededMetricProblem.load("../instances-bit-string-hamming/bit-string-hamming-seeds50-len100-inst0-maxspan.smp").evaluate

    #suite = {'Min Span Instance (Bit String Hamming Len 100 Inst 0)': minspan_instance,
    #         'Max Span Instance (Bit String Hamming Len 100 Inst 0)': maxspan_instance}

    for name in sorted(suite):

        print("Function :", name)
        print()

        function = suite[name]
        #assert isinstance(function, BenchmarkFunction)
        if hasattr(function, 'global_optima'):
            print("Number of Global Optima :", function.global_optima().__len__())
            first = next(function.global_optima().__iter__())
            print("First Global Optima :", str(first)[:70], ". . .")
        else:
            print("Number of Global Optima : UNKNOWN")
            print("First Global Optima : UNKNOWN")

        if hasattr(function, 'optimum_value'):
            print("Optimal Fitness :", function.optimum_value())
        else:
            print("Optimal Fitness : UNKNOWN")
        print()

        length = 100
        samples = 10
        points = 1000

        threshold = 0.01
        measure = Dispersion(points, threshold, True, HammingDistance(),
                             function, UniformBitStringSeedGenerator(length).generate_seeds)
        run_measure(measure, samples, "Dispersion Measure")

        #measure = SpanningTreeCorrelation(points, HammingDistance(), function,
        #                                  UniformBitStringSeedGenerator(length).generate_seeds)
        #run_measure(measure, samples, "Spanning Tree Correlation")

        #measure = SpanningTreeConcordance(points, HammingDistance(), function,
        #                                  UniformBitStringSeedGenerator(length).generate_seeds)
        #run_measure(measure, samples, "Spanning Tree Concordance")

        print()
        print()
