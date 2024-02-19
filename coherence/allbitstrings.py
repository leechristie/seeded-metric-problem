def all_bit_strings(length):
    class GeneratorWithLength(object):
        def __init__(self, generator, length):
            self.generator = generator
            self.length = length

        def __len__(self):
            return self.length

        def __iter__(self):
            return self.generator
    def all_bit_strings_generator(length):
        def decrement(current):
            current = list(current)
            index = 0
            while index < len(current):
                current[index] -= 1
                if current[index] == -1:
                    current[index] = 1
                    index += 1
                else:
                    break
            return current
        assert isinstance(length, int)
        assert length >= 0
        if length == 0:
            return
        x = [1] * length
        yield tuple(x)
        while 1 in x:
            x = decrement(x)
            yield tuple(x)
    return GeneratorWithLength(all_bit_strings_generator(length), 2 ** length)


if __name__ == "__main__":

    print("str : ", all_bit_strings(0))
    print("len : ", len(all_bit_strings(0)))
    print("list : ", list(all_bit_strings(0)))
    print("frozenset : ", frozenset(all_bit_strings(0)))
    print()

    print("str : ", all_bit_strings(1))
    print("len : ", len(all_bit_strings(1)))
    print("list : ", list(all_bit_strings(1)))
    print("frozenset : ", frozenset(all_bit_strings(1)))
    print()

    print("str : ", all_bit_strings(2))
    print("len : ", len(all_bit_strings(2)))
    print("list : ", list(all_bit_strings(2)))
    print("frozenset : ", frozenset(all_bit_strings(2)))
    print()

    print("str : ", all_bit_strings(3))
    print("len : ", len(all_bit_strings(3)))
    print("list : ", list(all_bit_strings(3)))
    print("frozenset : ", frozenset(all_bit_strings(3)))
    print()

    print("str : ", all_bit_strings(10))
    print("len : ", len(all_bit_strings(10)))
    print()

    print("str : ", all_bit_strings(25))
    print("len : ", len(all_bit_strings(25)))
    print()