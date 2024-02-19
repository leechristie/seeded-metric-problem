import math


def compare(x, y):
    if y > x:
        return 1
    elif x < y:
        return -1
    else:
        return 0


def concordance(xs, ys):
    assert isinstance(xs, list)
    assert isinstance(ys, list)
    assert len(xs) == len(ys)
    n = len(xs)
    n_pairs = (n * (n-1)) // 2
    n_pairs_seen = 0
    n_okay = 0
    for i in range(n-1):
        for j in range(i+1, n):
            if compare(xs[i], xs[j]) == compare(ys[i], ys[j]):
                n_okay += 1
            n_pairs_seen += 1
    assert n_pairs_seen == n_pairs
    return n_okay / n_pairs


def correlation_coefficient(xs, ys):
    assert isinstance(xs, list)
    assert isinstance(ys, list)
    assert len(xs) == len(ys)
    n = len(xs)
    x_bar = sum(xs) / n
    y_bar = sum(ys) / n
    num = sum([(xs[i] - x_bar)*(ys[i] - y_bar) for i in range(n)])
    den = math.sqrt(sum([(xs[i] - x_bar) ** 2 for i in range(n)]) * sum([(ys[i] - y_bar) ** 2 for i in range(n)]))
    if den != 0:
        return num / den
    else:
        return float('inf')


def descriptive_statistics(data):
    rv = {}
    data_count = len(data)
    n = data_count
    rv['count'] = data_count
    rv['n'] = data_count
    data_sum = sum(data)
    data_mean = data_sum / data_count
    rv['mean'] = data_mean
    sqr_diff = sum([(datum - data_mean) ** 2 for datum in data])
    rv['stdev'] = math.sqrt(sqr_diff / data_count)
    rv['sample_stdev'] = math.sqrt(sqr_diff / (data_count - 1))
    minimum = min(data)
    maximum = max(data)
    if n % 2 == 1:
        median = data[n // 2]
    else:
        median = (data[n // 2] + data[n // 2 - 1]) / 2
    rv['median'] = median
    rv['min'] = minimum
    rv['max'] = maximum
    rv['q0'] = minimum
    rv['q2'] = median
    rv['q4'] = maximum
    return rv
