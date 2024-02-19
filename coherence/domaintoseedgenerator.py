from seedgenerators import UniformBitStringSeedGenerator, UniformIntVectorSeedGenerator, UniformPermutationSeedGenerator

def domain_to_seed_generator(problem):
    domain = problem.domain
    length = problem.length
    assert isinstance(length, int)
    if domain == (0, 1):
        return UniformBitStringSeedGenerator(length)
    elif type(domain) == tuple:
        assert isinstance(domain, tuple)
        if len(domain) != 2:
            raise Exception("seed generator converter not implemented for this domain")
        assert len(domain) == 2
        return UniformIntVectorSeedGenerator([(min(domain), max(domain))] * length)
    else:
        if type(domain) != set:
            raise Exception("seed generator converter not implemented for this domain")
        assert isinstance(domain, set)
        assert len(domain) == length
        return UniformPermutationSeedGenerator(domain)
