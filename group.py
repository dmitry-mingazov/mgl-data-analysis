
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

def group_by_first_class(chains):
    grouped_chains = {}
    for chain in chains:
        cn = chain[0]["cn"]
        group = grouped_chains.get(cn, [])
        group.append(chain)
        grouped_chains[cn] = group
    return grouped_chains

def group_by_class_name(chains):
    grouped_chains = {}
    for chain in chains:
        cn = get_chain_cn(chain)
        group = grouped_chains.get(cn, [])
        group.append(chain)
        grouped_chains[cn] = group
    return grouped_chains
    # for chain in chains:

def group_by_cid(chains):
    grouped_chains = {}
    # make sure that chains contain only
    # one cid (split_chains_by_cid)
    for chain in chains:
        if not chain:
            continue
        cid = chain[0]["cid"]
        group = grouped_chains.get(cid, [])
        group.append(chain)
        grouped_chains[cid] = group
    return grouped_chains

