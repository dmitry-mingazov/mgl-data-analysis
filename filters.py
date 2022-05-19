
def filter_chains_smaller_than(chains, threshold):
    return filter_chains_by_len(chains, threshold, True)        

def filter_chains_bigger_than(chains, threshold):
    return filter_chains_by_len(chains, threshold, False)        

def filter_chains_by_len(chains, threshold, is_less_then):
    filtered_chains = []
    for chain in chains:
        len_lesser_threshold = len(chain) < threshold
        if len_lesser_threshold == is_less_then:
            filtered_chains.append(chain)
    return filtered_chains
