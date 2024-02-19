import random
from itertools import permutations
from kendalltau import kendalltau
import tausurfaceformula
import weightedchoice


def random_adjacent_swap(x, must_increase_kt_distance=False):
    i = random.randint(0, len(x)-2)
    if must_increase_kt_distance:
        while x[i] > x[i+1]:
            i = random.randint(0, len(x)-2)
    x[i], x[i+1] = x[i+1], x[i]
    return x


def random_swap(x):
    x = list(x)
    i = random.randint(0, len(x) - 1)
    j = i
    while j == i:
        j = random.randint(0, len(x) - 1)
    x[i], x[j] = x[j], x[i]
    return x


def all_perm_at_distance(center, radius):
    rv = []
    for x in permutations(center):
        if kendalltau(x, center) == radius:
            rv.append(tuple(x))
    return rv


def all_perm_within_distance(center, radius):
    rv = []
    for x in permutations(center):
        if kendalltau(x, center) <= radius:
            rv.append(tuple(x))
    return rv


from metrics import KendallTauRankDistance
D = KendallTauRankDistance(normalised=False).distance


def random_at_kendalltau_distance(center, radius):
    #print("random_at_kendalltau_distance(" + str(shorten(center)) + ", " + str(radius) + "):")
    y = list(center)
    swaps = 0
    while kendalltau(center, y) < radius:
        temp_y = random_swap(y)
        kt = kendalltau(center, temp_y)
        if kt == radius:
            return tuple(temp_y)
        elif kt < radius:
            y = temp_y
        y = random_adjacent_swap(y, False)
        swaps += 1
    if D(center, y) != radius:
        import sys
        sys.exit()
    assert D(center, y) == radius
    return tuple(y)


def shorten(x):
    if x is None:
        return None
    elif len(x) == 0:
        return []
    elif type(x[0]) in (list, tuple):
        return [shorten(e) for e in x]
    else:
        if len(x) < 11:
            return x
        else:
            return str(x[0:11])[0:-1] + ", ...]"


def random_within_kt_ball(center, radius, exclude=[]):
    exclude = [tuple(e) for e in exclude]
    #print("random_within_kt_ball(" + str(shorten(center)) + ", " + str(radius) + ", " + str(shorten(exclude)) + "):")
    cumulative = tausurfaceformula.kt_cumulative(len(center))
    chosen_radius = 0
    while chosen_radius < 1:
        chosen_radius = weightedchoice.random_choice(cumulative,
                                                     maximum=radius)
    rv = random_at_kendalltau_distance(center, chosen_radius)
    while rv in exclude:
        chosen_radius = 0
        while chosen_radius < 1:
            chosen_radius = weightedchoice.random_choice(cumulative,
                                                         maximum=radius)
        rv = random_at_kendalltau_distance(center, chosen_radius)
    return rv


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
    import tqdm
    length = 100
    center = list(range(length))
    random.shuffle(center)
    radius = 2000
    samples = 10000
    for i in tqdm.tqdm(range(samples)):
        point = random_within_kt_ball(center, radius)



#def main():
#    import tqdm
#    length = 7
#    center = list(range(length))
#    random.shuffle(center)
#    print(center)
#    radius = 4
#    #all_on_rad = all_perm_at_distance(center, radius)
#    all_on_rad = all_perm_within_distance(center, radius)
#    print(len(all_on_rad))
#    samples = 10000
#    counts = dict.fromkeys(list(all_on_rad), 0)
#    print("excluding ", [sorted(all_on_rad)[-1], sorted(all_on_rad)[-3]])
#    for i in tqdm.tqdm(range(samples)):
#        point = random_within_kt_ball(center, radius, exclude=[sorted(all_on_rad)[-1], sorted(all_on_rad)[-3]])
#        assert point in all_on_rad
#        counts[point] += 1
#    for key in sorted(all_on_rad):
#        print(key, leftpad(percent(counts[key] / samples, 2), 7), sep="\t")


if __name__ == "__main__":
    main()
