# returns a list of +1s and -1s specifying how how the candidate moves
# relative to each seed in kendal-tau distance when flipped at (i, i+1)

def kendalltau_adjust(candidate, seeds, i):
    x_i, x_j = candidate[i:i+2]
    rv = [0] * len(seeds)
    for seed_id in range(len(seeds)):
        seed = seeds[seed_id]
        for e in seed:
            if e == x_i:
                rv[seed_id] = 1
                break
            elif e == x_j:
                rv[seed_id] = -1
                break
        else:
             raise ValueError("did not find " + str(x_i) + " or " + str(x_j) + " in " + str(seed))
    return rv
