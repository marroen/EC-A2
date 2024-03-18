def count_ones(bitstring):
    return bitstring.count(1)

def multi_fit_func(bitstrings, fit_func):
    return [fit_func(bitstring) for bitstring in bitstrings]
