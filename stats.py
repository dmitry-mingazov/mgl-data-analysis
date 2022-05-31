def stats_first_row(chains, column):
    occurences = {}
    for chain in chains:
        value = chain[0][column]
        occ = occurences.get(value, 0) + 1
        occurences[value] = occ
    return occurences

def stats_last_row(chains, column):
    occurences = {}
    for chain in chains:
        value = chain[-1][column]
        occ = occurences.get(value, 0) + 1
        occurences[value] = occ
    return occurences

