import re
def filter_chains(chains, filter_fn):
    return list(filter(filter_fn, chains))

def filter_rows_inside_chains(chains, filter_fn):
    return list(map(lambda c: filter(c, filter_fn), chains))

def filter_chains_smaller_than(chains, threshold):
    return filter_chains(chains, lambda c: len(c) < threshold)

def filter_chains_bigger_than(chains, threshold):
    return filter_chains(chains, lambda c: len(c) > threshold)

# def filter_chains_by_len(chains, threshold, is_less_then):
#     filtered_chains = []
#     for chain in chains:
#         len_lesser_threshold = len(chain) < threshold
#         if len_lesser_threshold == is_less_then:
#             filtered_chains.append(chain)
#     return filtered_chains

def filter_chains_by_group(grouped_chains, group):
    chains = grouped_chains.get(group, [])
    return chains

def order_chains_by_column(chains, column):
    filtered_chains = []
    for chain in chains:
        ordered = sorted(chain, key=lambda row: row[column])
        filtered_chains.append(ordered)
    return filtered_chains

def delete_duplicate_chains_by_cn_ordered(chains):
    dupes_counter = 0
    chains_by_size = {}
    for chain in chains:
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
    print(f"Chains removed: {dupes_counter}")
    return filtered_chains

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

def filter_grouped_chains_bigger_than(grouped_chains, threshold):
    filtered_grouped_chains = {}
    for cn in grouped_chains:
        group = grouped_chains[cn]
        if len(group) >= threshold:
            filtered_grouped_chains[cn] = group
    return filtered_grouped_chains

def split_chains_by_cid(chains):
    filtered_chains = []
    for chain in chains:
        cids = {}
        for row in chain:
            cid = row["cid"]
            cid_chain = cids.get(cid, [])
            cid_chain.append(row)
            cids[cid] = cid_chain
        for cid_chain in cids:
            filtered_chains.append(cid_chain)
    return filtered_chains

def has_chain_multiple_cids(chain):
    if not len(chain): 
        return False
    first_cid = chain[0]["cid"]
    for row in chain:
        if first_cid != row["cid"]:
            return True
    return False

def filter_chains_with_multiple_cids(chains):
    return filter_chains(chains, has_chain_multiple_cids)

def filter_chains_by_cn_blacklist(chains):
    # TODO take blacklist as parameter
    blacklist = ["act", "an1", "ap1", "app", "bsf", "but",
                 "che", "ctl", "dk", "doc", "dp", "ds", "dr",
                 "dsg", "ele", "exp", "fel", "krn", "mes", "mnu",
                 "msg", "nav", "rep", "rpt", "sch", "wap", "wkf",
                 ]
    blacklist_dict = {}
    for key in blacklist:
        blacklist_dict[key] = False
    filtered_chains = []
    for chain in chains:
        filtered_chain = []
        for row in chain:
            cn = row["cn"][:3].lower()
            if blacklist_dict.get(cn, True):
                filtered_chain.append(row)
        filtered_chains.append(filtered_chain)
    return filtered_chains

def filter_chains_by_act_whitelist(chains):
    # TODO take whitelist as parameter
    whitelist = ["COMPONENT_CLOSED"]
    whitelist_dict = {}
    for key in whitelist:
        whitelist_dict[key] = True
    filtered_chains = []
    for chain in chains:
        filtered_chain = []
        for row in chain:
            act = row["act"]
            if whitelist_dict.get(act, False):
                filtered_chain.append(row)
        filtered_chains.append(filtered_chain)
    return filtered_chains

def filter_chains_by_FRM_in_cn(chains):
    regex = r"^.{3}FRM.*"
    return filter_chains_by_regex_in_cn(chains, regex)

def filter_chains_by_regex_in_cn(chains, regex):
    filtered_chains = []
    for chain in chains:
        filtered_chain = []
        for row in chain:
            cn = row["cn"]
            if re.match(regex, cn):
                filtered_chain.append(row)
        filtered_chains.append(filtered_chain)
    return filtered_chains
