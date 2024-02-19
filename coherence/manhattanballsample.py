import random
from metrics import ManhattanDistance
from collections import Counter
from latticesurfaceformula import points_on_surface_of_lattice
import math

D = ManhattanDistance().distance


def is_outside_range(lst):
    for val in lst:
        if val < 0:
            return True
        if val > 7:
            return True
    return False


def random_point(n):
    return [random.randint(0, 7) for i in range(n)]


def random_neighbour(x):
    n = len(x)
    while True:
        index = random.randint(0, n-1)
        direction = random.choice([-1, 1])
        rv = list(x)
        if x[index] + direction < 0:
            rv[index] = 7
        elif x[index] + direction > 7:
            rv[index] = 0
        else:
            rv[index] += direction
        return tuple(rv)


def accept(temperature, cooling_rate=1000):
    return random.random() < math.exp(-temperature / cooling_rate)


def mutate(center, radius, d, cooling_rate=1000):
    x = list(center)
    temperature = 0
    while d(center, x) != radius:
        new_x = random_neighbour(x)
        if abs(d(center, new_x) - radius) < abs(D(center, x) - radius):
            x = new_x
        else:
            if cooling_rate is not None:
                if accept(temperature, cooling_rate):
                    x = new_x
        temperature += 1
    return tuple(x)


def manhattan_ball_sample(center, radius, exclude=()):
    """Randomly choose a point within a ball of radius *radius* from the point
    at *center* in a manhattan space, excluding the center point. (Not
    expected to be uniform).

    Keyword arguments:
    center -- the center point of the ball as an array of integers
    radius -- the radius of the ball
    exclude -- blacklist of points to not sample, default none
    """
    d = ManhattanDistance().distance
    x = None
    while x is None or x == center or x in exclude\
            or is_outside_range(x):
        n = len(center)
        radii = [i for i in range(1, radius + 1)]
        weight = [points_on_surface_of_lattice(n, r)
                  for r in range(1, radius + 1)]
        cumulative = [sum(weight[0:i+1]) for i in range(len(weight))]
        total = cumulative[-1]
        pointer = random.randint(0, total-1)
        i = 0
        while pointer >= cumulative[i]:
            i += 1
        selected_radius = radii[i]
        x = mutate(center, selected_radius, d, cooling_rate=100)
        assert d(x, center) <= radius
        assert d(x, center) == selected_radius
    for xi in x:
        assert xi >= 0
    return x


def exhaustive_manhattan_ball_sample(center, radius, exclude=()):
    global D
    n = len(center)
    x = None
    while x is None or x == center or x in exclude\
            or D(x, center) > radius or is_outside_range(x):
        x = tuple([random.randint(-radius, radius) for i in range(n)])
    for y in exclude:
        assert x != y
    return x


def main():
    center = 0, 0, 0
    radius = 10
    exclude = ((0, 0, 1), )
    num_samples = 25400
    counter = Counter()
    for i in range(num_samples):
        x = exhaustive_manhattan_ball_sample(center, radius, exclude)
        counter[x] += 1
    print(len(counter))
    for x in sorted(counter):
        print(x, counter[x], "\t", len(counter)*counter[x]/num_samples, sep="\t")


if __name__ == "__main__":
    main()
