
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

def delete_duplicate_chains_by_cn_ordered(grouped_chains):
    dupes_counter = 0
    filtered_grouped_chains = {}
    for cn in grouped_chains:
        chains_by_size = {}
        for chain in grouped_chains[cn]:
            chain_len = len(chain)
            tmp_array = chains_by_size.get(chain_len, [])
            tmp_array.append(chain)
            chains_by_size[chain_len] = tmp_array
        filtered_chains = []
        for index in chains_by_size:
            chains = chains_by_size[index]
            cn_strings = []
            for chain in chains:
                cn_string = ""
                for row in chain:
                    cn_string += row["cn"]
                cn_strings.append(cn_string)
            seen = set()
            i = 0
            for cn_string in cn_strings:
                chain = chains[i]
                i += 1
                if not(cn_string in seen):
                    seen.add(cn_string)
                    filtered_chains.append(chain)
                else:
                    dupes_counter += 1
        filtered_grouped_chains[cn] = filtered_chains
    print(f"Chains removed: {dupes_counter}")
    return filtered_grouped_chains

def delete_duplicate_rows(chains):
    filtered_chains = []
    for chain in chains:
        filtered_rows = []
        prev = chain[0]
        filtered_rows.append(prev)
        for row in chain:
            if row["d"] != prev["d"] or row["sid"] != prev["sid"]:
                filtered_rows.append(row)
                prev = row
        filtered_chains.append(filtered_rows)
    return filtered_chains

def filter_grouped_chains_smaller_than(grouped_chains, threshold):
    filtered_grouped_chains = {}
    for cn in grouped_chains:
        group = grouped_chains[cn]
        if len(group) >= threshold:
            filtered_grouped_chains[cn] = group
    return filtered_grouped_chains

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

