import random
import fractions


class SeedGenerator(object):
    """A generator of seeds in a search space."""

    def generate_seeds(self, n, blacklist=frozenset()):
        """Return *n* randomly-selected elements from the search space."""
        seeds = set()
        while len(seeds) < n:
            new_seed = self.generate_seed()
            if not new_seed in blacklist:
                seeds.add(self.generate_seed())
        return list(seeds)

    def generate_evaluated_seeds(self, f, n, blacklist=frozenset(), sort=False):
        samples = self.generate_seeds(n, blacklist=blacklist)
        if sort:
            r = set()
            while len(r) < n:
                r.add(random.uniform(0, 1))
            r = list(r)
            samples = [(f(sample), r.pop(), sample) for sample in samples]
            samples.sort()
            return [(e[0], e[2]) for e in samples]
        else:
            return [(f(sample), sample) for sample in samples]


class UniformBitStringSeedGenerator(SeedGenerator):
    """A generator of bit strings selected uniformly at random.
    
    Example:
        generator = UniformBitStringSeedGenerator(10)
        generator.generate_seeds(5)"""

    def __init__(self, length):
        """Return a seed generator for bit strings of length *length*.""" 
        self.length = length

    def generate_seed(self):
        """Return a single randomly-selected bit string."""
        seed = [None] * self.length
        for i in range(self.length):
            seed[i] = random.randint(0, 1)
        return tuple(seed)

    def get_domain(self):
        """Returns the domain."""
        return (0, 1)


class UniformIntVectorSeedGenerator(SeedGenerator):
    """A generator of int vectors selected uniformly at random.
    
    Example:
        generator = UniformIntVectorSeedGenerator([(1, 100)] * 10)
        generator.generate_seeds(5)
    
    Example:
        generator = UniformIntVectorSeedGenerator([(0, 5), (2, 4), (1, 10)])
        generator.generate_seeds(5)"""

    def __init__(self, ranges):
        """Return a seed generator for int vectors with allel ranges specified
        by *ranges* (inclusive).""" 
        self.length = len(ranges)
        self.ranges = ranges

    def generate_seed(self):
        """Return a single randomly-selected int vector."""
        seed = [None] * self.length
        for i in range(self.length):
            seed[i] = random.randint(min(self.ranges[i]), max(self.ranges[i]))
        return tuple(seed)

    def get_domain(self):
        """Returns the domain."""
        min_domain = min(self.ranges[0])
        max_domain = max(self.ranges[0])
        for i in range(len(self.ranges)):
            if min(self.ranges[i]) != min_domain or max(self.ranges[i]) != max_domain:
                raise ValueError("heterogeneous domains not supported for output")
        return (min_domain, max_domain)


class UniformFloatVectorSeedGenerator(SeedGenerator):
    """A generator of float vectors selected uniformly at random.
    
    Example:
        generator = UniformFloatVectorSeedGenerator([(0.0, 1.0)] * 10)
        generator.generate_seeds(5)
        
    Example:
        generator = UniformFloatVectorSeedGenerator([(0.0, 5.0), (0.0, 2.0)])
        generator.generate_seeds(5)"""

    def __init__(self, ranges):
        """Return a seed generator for float vectors with allel ranges specified
        by *ranges* (inclusive).""" 
        self.length = len(ranges)
        self.ranges = ranges

    def generate_seed(self):
        """Return a single randomly-selected float vector."""
        seed = [None] * self.length
        for i in range(self.length):
            seed[i] = random.uniform(min(self.ranges[i]), max(self.ranges[i]))
        return tuple(seed)

    def get_domain(self):
        """Returns the domain."""
        min_domain = min(self.ranges[0])
        max_domain = max(self.ranges[0])
        for i in range(len(self.ranges)):
            if min(self.ranges[i]) != min_domain or max(self.ranges[i]) != max_domain:
                raise ValueError("heterogeneous domains not supported for output")
        return (min_domain, max_domain)


class UniformFractionVectorSeedGenerator(SeedGenerator):
    """A generator of fraction vectors selected uniformly at random.
    
    Example:
        from fractions import Fraction
        generator = UniformFractionVectorSeedGenerator([(0, 1)] * 10,
                                                       [Fraction(1, 10)] * 10)
        generator.generate_seeds(5)
        
    Example:
        from fractions import Fraction
        generator = UniformFractionVectorSeedGenerator(
                    [(Fraction(1, 2), Fraction(5)), (0, 2)],
                    [Fraction(1, 10), Fraction(1, 100)])
        generator.generate_seeds(5)"""

    def __init__(self, ranges, increments):
        """Return a seed generator for fraction vectors with allel ranges
        specified by *ranges* (inclusive) which are multiples of the increments
        specified by *increments*.""" 
        self.length = len(ranges)
        self.ranges = ranges
        self.increments = increments

    def generate_seed(self):
        """Return a single randomly-selected fractions vectors."""
        seed = [None] * self.length
        for i in range(self.length):
            minimum = fractions.Fraction(min(self.ranges[i]))
            maximum = fractions.Fraction(max(self.ranges[i]))
            total_range = maximum - minimum
            steps = total_range / self.increments[i]
            seed[i] = random.randint(0, steps) * self.increments[i] + minimum
        return tuple(seed)

    def get_domain(self):
        """Returns the domain."""
        min_domain = min(self.ranges[0])
        max_domain = max(self.ranges[0])
        inc_domain = self.increments[0]
        for i in range(len(self.ranges)):
            if min(self.ranges[i]) != min_domain or max(self.ranges[i]) != max_domain or self.increments[i] != inc_domain:
                raise ValueError("heterogeneous domains not supported for output")
        return fractions.Fraction(min_domain), fractions.Fraction(max_domain), fractions.Fraction(inc_domain)


class UniformPermutationSeedGenerator(SeedGenerator):
    """A generator of permutation vectors selected uniformly at random.
    
    Example:
        generator = UniformPermutationSeedGenerator(10)
        generator.generate_seeds(5)
    
    Example:
        generator = UniformPermutationSeedGenerator(['A', 'J', 'Q', 'K'])
        generator.generate_seeds(5)"""

    def __init__(self, length_or_range):
        """Return a seed generator for permutations of *length_or_range*
        integers starting from 0 if length_or_range is an integer, otherwise
        *length_or_range* is used as a range or list of objects.""" 
        if type(length_or_range) == int:
            self.length = length_or_range
            self.perm_range = list(range(length_or_range))
        else:
            self.length = len(length_or_range)
            self.perm_range = list(length_or_range)

    def generate_seed(self):
        """Return a single randomly-selected permutation."""
        unselected = list(self.perm_range)
        seed = [None] * self.length
        i = 0
        while len(unselected) > 0:
            selection = random.choice(unselected)
            unselected.remove(selection)
            seed[i] = selection
            i += 1
        return tuple(seed)

    def get_domain(self):
        """Returns the domain."""
        return set(self.perm_range)
