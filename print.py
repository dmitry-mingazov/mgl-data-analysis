import re
import sys

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

def print_stats_first_row(chains, column):
    occurences = get_occurences(chains, column, 0)
    print_occurences_stats(occurences, len(chains))

def print_stats_last_row(chains, column):
    occurences = get_occurences(chains, column, -1)
    print_occurences_stats(occurences, len(chains))

def get_occurences(chains, column, index):
    occurences = {}
    for chain in chains:
        value = chain[index][column]
        occ = occurences.get(value, 0) + 1
        occurences[value] = occ
    return occurences

def print_chains_linked(chains):
    regex = r"([A-Z]{2}_[a-f0-9]+)"
    sys.stdout = open("linked_chains.txt", "w")
    print_chains_linked_by_regex(chains, regex)
    sys.stdout.close()
    sys.stdout = sys.__stdout__

def print_chains_linked_by_PR(chains):
    print_chains_linked_by_hash_prefix(chains, "PR")

def print_chains_linked_by_hash_prefix(chains, hash_prefix):
    regex = r"("+re.escape(hash_prefix)+"_[a-f0-9]+)"
    print_chains_linked_by_regex(chains, regex)

def print_chains_linked_by_regex(chains, regex):
    prs = {}
    for index, chain in enumerate(chains):
        for row in chain:
            matches = re.finditer(regex, row["d"])
            for _,match in enumerate(matches, start=1):
                pr = match.group()
                matched_chains = prs.get(pr, set())
                matched_chains.add(index)
                prs[pr] = matched_chains
    for pr in prs:
        if len(prs[pr]) == 1:
            continue
        print("------------------------")
        print(f"Chains containing {pr}:")
        for index in prs[pr]:
            print(f"chain{index+1}")
