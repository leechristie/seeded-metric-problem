from collections import Iterable
from numbers import Real
from allbitstrings import all_bit_strings


class BenchmarkFunction(object):

    def __call__(self, x):
        raise(NotImplementedError("To be over-ridden by subclass."))

    def global_optima(self):
        raise(NotImplementedError("To be over-ridden by subclass."))

    def optimum_value(self):
        raise(NotImplementedError("To be over-ridden by subclass."))


class Const(BenchmarkFunction):

    def __init__(self, length, constant):
        assert isinstance(length, int)
        assert length >= 0
        self.length = length
        assert isinstance(constant, Real)
        assert constant >= 0
        self.constant = constant

    def __call__(self, x):
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        return self.constant

    def global_optima(self):
        return all_bit_strings(self.length)

    def optimum_value(self):
        return self.constant


class Needle(BenchmarkFunction):

    def __init__(self, length):
        assert isinstance(length, int)
        assert length >= 0
        self.length = length

    def __call__(self, x):
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        for e in x:
            if e == 0:
                return 0
        return 1

    def global_optima(self):
        return [tuple([1] * self.length)]

    def optimum_value(self):
        return 1


class OneMax(BenchmarkFunction):

    def __init__(self, length):
        assert isinstance(length, int)
        assert length >= 0
        self.length = length

    def __call__(self, x):
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        return sum(x)

    def global_optima(self):
        return [tuple([1] * self.length)]

    def optimum_value(self):
        return self.length


class ZeroMax(BenchmarkFunction):

    def __init__(self, length):
        assert isinstance(length, int)
        assert length >= 0
        self.length = length

    def __call__(self, x):
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        return self.length - sum(x)

    def global_optima(self):
        return [tuple([0] * self.length)]

    def optimum_value(self):
        return self.length


class BinVal(BenchmarkFunction):

    def __init__(self, length):
        assert isinstance(length, int)
        assert length >= 0
        self.length = length

    def __call__(self, x):
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        rv = 0
        for i in range(self.length):
            if x[i] == 1:
                rv += 2 ** i
        return rv

    def global_optima(self):
        return [tuple([1] * self.length)]

    def optimum_value(self):
        return 2 ** self.length


class Check_1D(BenchmarkFunction):

    def __init__(self, length):
        assert isinstance(length, int)
        assert length >= 2
        self.length = length

    def __call__(self, x):
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        rv = 0
        for i in range(self.length - 1):
            if x[i] != x[i+1]:
                rv += 1
        return rv

    def global_optima(self):
        return [tuple([1 - i % 2 for i in range(self.length)]), tuple([i % 2 for i in range(self.length)])]

    def optimum_value(self):
        return self.length - 1


class Leading(BenchmarkFunction):

    def __init__(self, length):
        assert isinstance(length, int)
        assert length >= 0
        self.length = length

    def __call__(self, x):
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        num_ones = 0
        for i in range(self.length):
            if x[i] == 1:
                num_ones += 1
            else:
                return num_ones
        return self.length

    def global_optima(self):
        return [tuple([1] * self.length)]

    def optimum_value(self):
        return self.length


class Trap(BenchmarkFunction):

    def __init__(self, length, order):
        assert isinstance(length, int)
        assert length >= 0
        self.length = length
        assert isinstance(order, int)
        assert order >= 1
        self.order = order
        assert length % order == 0

    def __call__(self, x):
        def g(u, k):
            if u < k:
                return k - u - 1
            else:
                return k
        assert isinstance(x, Iterable)
        assert len(x) == self.length
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        rv = 0
        for i in range(self.length // self.order):
            u = 0
            for j in range(self.order):
                u += x[i*self.order + j]
            rv += g(u, self.order)
        return rv

    def global_optima(self):
        return [tuple([1] * self.length)]

    def optimum_value(self):
        return self.length


class Goldberg(BenchmarkFunction):

    def __call__(self, x):
        def g(u, k):
            if u < k:
                return k - u - 1
            else:
                return k
        assert isinstance(x, Iterable)
        assert len(x) == 3
        for e in x:
            assert isinstance(e, int)
            assert e in {0, 1}
        if x == [1, 1, 1]:
            return 30
        elif x == [0, 0, 1]:
            return 14
        elif x == [0, 1, 0]:
            return 22
        elif x == [1, 0, 0]:
            return 26
        elif x == [0, 0, 0]:
            return 28
        else:
            return 0

    def global_optima(self):
        return [(1, 1, 1)]

    def optimum_value(self):
        return 30


def suite_100():
    return {"Const(100, 42)" : Const(100, 42),
            "Needle(100)"    : Needle(100),
            "OneMax(100)"    : OneMax(100),
            "ZeroMax(100)"   : ZeroMax(100),
            "BinVal(100)"    : BinVal(100),
            "Check_1D(100)"  : Check_1D(100),
            "Trap(100, 4)"   : Trap(100, 4),
            "Trap(100, 5)"   : Trap(100, 5),
            "Trap(100, 10)"  : Trap(100, 10),
            "Trap(100, 20)"  : Trap(100, 20)}


if __name__ == "__main__":

    f = Const(9, 42)
    display = "Const(9, 42)"
    x = [1, 1, 1, 1, 0, 1, 1, 0, 0]
    actual = f(x)
    expected = 42
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = Needle(9)
    display = "Needle(9)\t"
    x = [1, 1, 1, 1, 0, 1, 1, 0, 0]
    actual = f(x)
    expected = 0
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = OneMax(8)
    display = "OneMax(8)\t"
    x = [1, 1, 1, 1, 0, 1, 1, 0]
    actual = f(x)
    expected = 6
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = ZeroMax(8)
    display = "ZeroMax(8)\t"
    x = [1, 1, 1, 1, 0, 1, 1, 0]
    actual = f(x)
    expected = 2
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = BinVal(8)
    display = "BinVal(8)\t"
    x = [1, 1, 1, 1, 0, 1, 1, 0]
    actual = f(x)
    expected = 111
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = Check_1D(8)
    display = "Check_1D(8)\t"
    x = [1, 1, 1, 1, 0, 1, 1, 0]
    actual = f(x)
    expected = 3
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = Leading(8)
    display = "Leading(8)\t"
    x = [1, 1, 1, 1, 0, 1, 1, 0]
    actual = f(x)
    expected = 4
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = Trap(8, 4)
    display = "Trap(8, 4)\t"
    x = [1, 1, 1, 1, 0, 1, 1, 0]
    actual = f(x)
    expected = 5
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")

    f = Goldberg()
    display = "Goldberg()\t"
    x = [0, 0, 1]
    actual = f(x)
    expected = 14
    print(display, actual, "okay" if actual == expected else "fail", sep="\t")
