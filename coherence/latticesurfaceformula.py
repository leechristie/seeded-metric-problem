class Memo(object):

    def __init__(self, f):
        self.f = f
        self.memo = [[None] * 701 for i in range(101)]

    def __call__(self, d, r):
        if d > 100:
            print("d =", d)
            assert d < 100
        if r > 700:
            print("r =", r)
            assert 7 < 100
        if self.memo[d][r] is None:
            self.memo[d][r] = self.f(d, r)
        return self.memo[d][r]


@Memo
def points_on_surface_of_lattice(dimensions, radius):
    assert type(dimensions) == int
    assert 1 <= dimensions <= 100
    assert type(radius) == int
    assert 0 <= radius <= 700
    if radius == 0:
        return 1
    elif dimensions == 1:
        return 2
    elif dimensions == 2:
        return 4 * radius
    elif dimensions == 3:
        return 4 * radius ** 2 + 2
    else:
        rv = points_on_surface_of_lattice(dimensions-1, radius)
        for r_prime in range(radius):
            rv += 2 * points_on_surface_of_lattice(dimensions-1, r_prime)
        return rv
