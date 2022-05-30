
def print_chain_stats(chains):
    print(f"Size of filtered chains: {len(chains)}")

def print_grouped_chain_stats(grouped_chains):
    for cn in grouped_chains:
        print(f"{cn}: {len(grouped_chains[cn])} chains")

def print_occurences_stats(occurences, tot):
    print(f"Chains analyzed: {tot}")
    for value in occurences:
        perc = (occurences[value]/tot)*100
        print(f"{value}: {perc:.3}% ({occurences[value]})")

def print_group_cids(chains):
    occurences = {}
    for chain in chains:
        cid = chain[0]["cid"]
        occ = occurences.get(cid, 0) + 1
        occurences[cid] = occ
    for cid in occurences:
        print(f"{cid}: {occurences[cid]} chains")