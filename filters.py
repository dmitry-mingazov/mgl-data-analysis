
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

def get_chain_cn(chain):
    occurences = {}
    max = -1
    max_class_name = ""
    for row in chain:
        class_name = row["cn"][:3]
        occ = occurences.get(class_name, 0) + 1
        occurences[class_name] = occ 
        if occ > max:
            max = occ
            max_class_name = class_name
    return max_class_name

def group_by_class_name(chains):
    grouped_chains = {}
    for chain in chains:
        cn = get_chain_cn(chain)
        group = grouped_chains.get(cn, [])
        group.append(chain)
        grouped_chains[cn] = group
    return grouped_chains
    # for chain in chains:

