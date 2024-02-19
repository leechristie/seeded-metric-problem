import metrics
import fractions
import interpolationmethods
import difficultymeasures
import domaintoseedgenerator


class SeededMetricProblem(object):
    """An instance of the seeded metric problem."""

    def __init__(self, domain, codomain, seeds, fitnesses, interpolation_method, interpolation_metric, minimise_objective, **meta_data):
        """Returns a seeded metric problem."""
        if len(domain) == 3 and (type(domain[0]) == fractions.Fraction or type(domain[1]) == fractions.Fraction or type(domain[2]) == fractions.Fraction):
            domain = (fractions.Fraction(domain[0]), fractions.Fraction(domain[1]), fractions.Fraction(domain[2]))
        self.domain = domain
        self.codomain = codomain
        self.length = len(seeds[0])
        self.seeds = seeds
        self.fitnesses = fitnesses
        self.interpolation_method = interpolation_method
        self.interpolation_metric = interpolation_metric
        self.minimise_objective = minimise_objective
        self.meta_data = meta_data
        #self.difficulty_measures = object()
        #generator = domaintoseedgenerator.domain_to_seed_generator(self).generate_seeds
        #def dispersion(num_points, threshold):
        #    if minimise_objective:
        #        maximization_objective = False
        #    else:
        #        maximization_objective = True
        #    measure = difficultymeasures.Dispersion(num_points, threshold, maximization_objective, interpolation_metric, self.evaluate, generator)
        #    return measure.measure()
        #self.difficulty_measures.dispersion = dispersion
        #def spanning_tree_correlation(num_points):
        #    measure = difficultymeasures.SpanningTreeCorrelation(num_points, interpolation_metric, self.evaluate, generator)
        #    return measure.measure()
        #self.difficulty_measures.spanning_tree_correlation = spanning_tree_correlation

    def evaluate(self, candidate):
        """Return the fitness of the specified *candidate*."""
        return self.interpolation_method.interpolate(candidate, self.seeds, self.fitnesses, self.interpolation_metric)

    def save(self, file):
        """Saves this problem instance to the specified *file*."""
        if type(file) == str:
            do_close = True
            file = open(file, "w")
        else:
            do_close = False
        file.write("seededmetricproblem 4.0\n")
        for k in sorted(self.meta_data.keys()):
            file.write("# meta " + str(k) + " \"" + str(self.meta_data[k]) + "\"\n")
        if self.minimise_objective:
            file.write("objective min\n")
        else:
            file.write("objective max\n")
        if type(self.domain) == set:
            file.write("domain permutation")
            for e in sorted(list(self.domain)):
                file.write(" " + str(e))
            file.write("\n")
        elif type(self.domain) == tuple:
            min_value = min(self.domain)
            max_value = max(self.domain)
            if type(min_value) == fractions.Fraction and len(self.domain) == 3:
                min_value = self.domain[0]
                max_value = self.domain[1]
                inc_value = self.domain[2]
            if type(min_value) != type(max_value):
                raise TypeError("max and min in domain are not the same type")
            if type(min_value) == float:
                file.write("domain float " + str(min_value) + " " + str(max_value) + "\n")
            elif type(min_value) == int:
                file.write("domain int " + str(min_value) + " " + str(max_value) + "\n")
            elif type(min_value) == fractions.Fraction and len(self.domain) == 3:
                file.write("domain fraction " + str(min_value.numerator) + "/" + str(min_value.denominator) + " "
                           + str(max_value.numerator) + "/" + str(max_value.denominator) + " "
                           + str(inc_value.numerator) + "/" + str(inc_value.denominator) + "\n")
            else:
                raise TypeError("unknown domain")
        min_covalue = min(self.codomain)
        max_covalue = max(self.codomain)
        if type(min_covalue) != type(max_covalue):
            raise TypeError("max and min in domain are not the same type")
        if type(min_covalue) == float:
            file.write("codomain float " + str(min_covalue) + " " + str(max_covalue) + "\n")
        elif type(min_covalue) == int:
            file.write("codomain int " + str(min_covalue) + " " + str(max_covalue) + "\n")
        elif type(min_covalue) == fractions.Fraction:
            file.write(
                "codomain fraction " + str(min_covalue.numerator) + "/" + str(min_covalue.denominator) + " " + str(
                    max_covalue.numerator) + "/" + str(max_covalue.denominator) + "\n")
        else:
            raise TypeError("unknown codomain")
        file.write("numseeds " + str(len(self.seeds)) + "\n")  # write numseeds
        file.write("length " + str(self.length) + "\n")  # write length
        file.write(str(self.interpolation_method) + "\n")  # write interpolation
        file.write(str(self.interpolation_metric) + "\n")  # write metric
        file.write("start seeds\n")
        for i in range(len(self.seeds)):
            fitness = self.fitnesses[i]
            seed = self.seeds[i]
            for e in seed:
                if type(e) == fractions.Fraction:
                    file.write(str(e.numerator) + "/" + str(e.denominator) + " ")
                else:
                    file.write(str(e) + " ")
            file.write(": ")
            if type(fitness) == fractions.Fraction:
                file.write(str(fitness.numerator) + "/" + str(fitness.denominator))
            else:
                file.write(str(fitness))
            file.write("\n")
        file.write("end seeds\n")
        file.flush()
        if do_close:
            file.close()

    @staticmethod
    def parse_domain(tokens):
        if tokens[0] == 'permutation':
            tokens = tokens[1:]
            length = len(tokens)
            rv = [None] * length
            for i in range(length):
                if tokens[i].startswith("'") and tokens[i].endswith("'"):
                    rv[i] = tokens[i][1:-1]
                elif tokens[i].startswith('"') and tokens[i].endswith('"'):
                    rv[i] = tokens[i][1:-1]
                elif "/" in tokens[i]:
                    rv[i] = fractions.Fraction(tokens[i])
                elif "." in tokens[i]:
                    rv[i] = float(tokens[i])
                else:
                    rv[i] = int(tokens[i])
            if len(set(rv)) != len(rv):
                raise ValueError("repeated item in permutation")
            return set(rv)
        elif tokens[0] == 'int':
            if len(tokens) != 3:
                raise ValueError("expected 3 tokens")
            minimum = int(tokens[1])
            maximum = int(tokens[2])
            if minimum < maximum:
                return minimum, maximum
            else:
                raise ValueError("maximum <= minimum")
        elif tokens[0] == 'float':
            if len(tokens) != 3:
                raise ValueError("expected 3 tokens")
            minimum = float(tokens[1])
            maximum = float(tokens[2])
            if minimum < maximum:
                return minimum, maximum
            else:
                raise ValueError("maximum <= minimum")
        elif tokens[0] == 'fraction':
            if len(tokens) == 3:
                minimum = fractions.Fraction(tokens[1])
                maximum = fractions.Fraction(tokens[2])
                if minimum < maximum:
                    return minimum, maximum
                else:
                    raise ValueError("maximum <= minimum")
            if len(tokens) == 4:
                minimum = fractions.Fraction(tokens[1])
                maximum = fractions.Fraction(tokens[2])
                increment = fractions.Fraction(tokens[3])
                if minimum < maximum:
                    return minimum, maximum, increment
                else:
                    raise ValueError("maximum <= minimum")
            else:
                print(tokens)
                raise ValueError("expected 3 or 4 tokens")
        else:
            raise ValueError("unknown type " + tokens[0])

    @staticmethod
    def load(file):
        """Loads a problem instance from the specified *file*."""
        if type(file) == str:
            do_close = True
            file = open(file)
        else:
            do_close = False
        lines = [line.strip(" \t\n\r") for line in file]
        i = 0
        while (lines[i].startswith("#") and not lines[i].startswith("# meta")) or len(lines[i].strip(" \n\t\r")) == 0:
            i += 1
        if lines[i] != "seededmetricproblem 4.0":
            raise IOError("invalid file format: expected 'seededmetricproblem 4.0' before any parameters or metadata")
        i += 1
        meta = {}
        minimise_objective = None
        length = None
        numseeds = None
        interpolation = None
        metric = None
        domain = None
        codomain = None
        fitnesses = []
        seeds = []
        while i < len(lines):
            line = lines[i]
            assert isinstance(line, str)
            if line.startswith("# meta "):
                tokens = line[len("# meta "):]
                tokens = tokens.split(" ", 1)
                if not tokens[1].startswith('"') or not tokens[1].endswith('"'):
                    raise IOError("invalid file format: invalid meta '" + line + "'")
                if tokens[0] in meta:
                    raise IOError("invalid file format: meta data key " + tokens[0] + " appears more than once")
                meta.update({tokens[0]: tokens[1].strip('"')})
            elif len(line.strip(" \t\n\r")) == 0:
                pass
            elif line.startswith("#"):
                pass
            elif line.startswith("objective "):
                token = line[len("objective "):]
                if minimise_objective is not None:
                    raise IOError("invalid file format: repeated 'objective'")
                if token == 'max':
                    minimise_objective = False
                elif token == 'min':
                    minimise_objective = True
                else:
                    raise IOError("invalid file format: invalid objective '" + token + "'")
            elif line.startswith("length "):
                token = line[len("length "):]
                if length is not None:
                    raise IOError("invalid file format: repeated 'length'")
                try:
                    token = int(token)
                except ValueError:
                    raise IOError("invalid file format: invalid length '" + token + "', expected integer")
                if token <= 0:
                    raise IOError("invalid file format: invalid length " + str(token), ", expected > 0")
                length = token
            elif line.startswith("numseeds "):
                token = line[len("numseeds "):]
                if numseeds is not None:
                    raise IOError("invalid file format: repeated 'numseeds'")
                try:
                    token = int(token)
                except ValueError:
                    raise IOError("invalid file format: invalid length '" + token + "', expected integer")
                if token < 2:
                    raise IOError("invalid file format: invalid length " + str(token), ", expected >= 2")
                numseeds = token
            elif line.startswith("interpolation "):
                if interpolation is not None:
                    raise IOError("invalid file format: repeated 'interpolation'")
                try:
                    interpolation = interpolationmethods.InterpolationMethod.parse(line)
                except ValueError:
                    raise IOError("invalid file format: invalid interpolation " + line, ", unknown, failed to parse")
            elif line.startswith("metric "):
                if metric is not None:
                    raise IOError("invalid file format: repeated 'metric'")
                try:
                    metric = metrics.Metric.parse(line)
                except ValueError:
                    raise IOError("invalid file format: invalid metric " + line, ", unknown, failed to parse")
            elif line.startswith("domain"):
                if domain is not None:
                    raise IOError("invalid file format: repeated 'domain'")
                tokens = line[len("domain "):].split(" ")
                try:
                    domain = SeededMetricProblem.parse_domain(tokens)
                except ValueError:
                    raise IOError("invalid file format: invalid domain " + line, ", unknown, failed to parse")
            elif line.startswith("codomain"):
                if codomain is not None:
                    raise IOError("invalid file format: repeated 'codomain'")
                tokens = line[len("codomain "):].split(" ")
                try:
                    codomain = SeededMetricProblem.parse_domain(tokens)
                except:
                    raise IOError("invalid file format: invalid codomain " + line, ", unknown, failed to parse")
                if type(codomain) == set:
                    raise IOError("invalid file format: invalid codomain, permutation not supported as co-domain")
            elif line == 'start seeds':
                i += 1
                line = lines[i]
                while i < len(lines) and line != 'end seeds':
                    fitness = None
                    if " : " not in line:
                        raise IOError("invalid file format: invalid seed '" + line + "'")
                    tokens = line.split(" : ")
                    if len(tokens) != 2:
                        raise IOError("invalid file format: invalid seed '" + line + "'")
                    if tokens[1].startswith("'") and tokens[1].endswith("'"):
                        fitness = tokens[i][1:-1]
                    elif tokens[1].startswith('"') and tokens[1].endswith('"'):
                        fitness = tokens[i][1:-1]
                    elif "/" in tokens[1]:
                        fitness = fractions.Fraction(tokens[1])
                    elif "." in tokens[1]:
                        fitness = float(tokens[1])
                    else:
                        fitness = int(tokens[1])
                    fitnesses.append(fitness)
                    seed = []
                    for token in tokens[0].split(" "):
                        coordinate = None
                        if token.startswith("'") and token.endswith("'"):
                            coordinate = token[1:-1]
                        elif token.startswith('"') and token.endswith('"'):
                            coordinate = token[1:-1]
                        elif "/" in token:
                            coordinate = fractions.Fraction(token)
                        elif "." in token:
                            coordinate = float(token)
                        else:
                            coordinate = int(token)
                        seed.append(coordinate)
                    seeds.append(seed)
                    i += 1
                    line = lines[i]
            else:
                raise IOError("invalid file format: invalid line: '" + line, "'")
            i += 1
        if minimise_objective is None:
            raise IOError("invalid file format: missing 'objective'")
        if length is None:
            raise IOError("invalid file format: missing 'length'")
        if numseeds is None:
            raise IOError("invalid file format: missing 'numseeds'")
        if interpolation is None:
            raise IOError("invalid file format: missing 'interpolation'")
        if metric is None:
            raise IOError("invalid file format: missing 'metric'")
        if domain is None:
            raise IOError("invalid file format: missing 'domain'")
        if codomain is None:
            raise IOError("invalid file format: missing 'codomain'")
        if len(fitnesses) < 2 or len(seeds) < 2:
            raise IOError("invalid file format: expected: 2 or more seeds")
        if len(fitnesses) != numseeds:
            raise IOError("invalid file format: stated " + str(numseeds) + " seeds, only found " + str(len(fitnesses)))
        for i in range(len(fitnesses)):
            if len(seeds[i]) != length:
                raise IOError("invalid file format: not all seeds of stated length")
        rv = SeededMetricProblem(domain, codomain, seeds, fitnesses, interpolation, metric, minimise_objective)
        rv.meta_data = meta
        if do_close:
            file.close()
        return rv
