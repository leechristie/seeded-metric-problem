import random


def cumulative_weights(weights):
    return [sum(weights[:i+1]) for i in range(len(weights))]


def random_choice(cumulative, maximum=None):
    if maximum is None:
        pointer = random.randint(0, cumulative[-1]-1)
    else:
        pointer = random.randint(0, cumulative[maximum]-1)
    for i in range(len(cumulative)):
        if cumulative[i] > pointer:
            return i


def leftpad(s, l):
    while len(s) < l:
        s = " " + s
    return s


def percent(x, dp=0):
    if dp == 0:
        return str(int(x * 100)) + "%"
    else:
        return (("%0." + str(dp) + "f") % (x * 100)) + "%"


def main():
    from collections import Counter
    cumulative = cumulative_weights([10, 90, 90, 5])
    samples = 10000
    counter = Counter()
    for i in range(samples):
        counter[random_choice(cumulative, maximum=1)] += 1
    for e in sorted(counter):
        print(e, percent(counter[e] / samples, 2))


if __name__ == "__main__":
    main()
