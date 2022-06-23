import csv
from Chain import ChainFactory

def __add_id(id, chain_index, valuable_ids):
    if (id not in valuable_ids) and id:
        valuable_ids[id] = chain_index

def __init_new_chain(id1, id2, chains_size, valuable_ids):
    chains_size += 1
    if id1:
        __add_id(id1, chains_size, valuable_ids)
    if id2:
        __add_id(id2, chains_size, valuable_ids)
    return chains_size

def __merge_chains(chains, chain_index_1, chain_index_2, valuable_ids):
    merged_chain = chains[chain_index_1]
    for row in chains[chain_index_2]:
        merged_chain.append(row)
    chains[chain_index_2] = []
    for id in valuable_ids:
        if valuable_ids[id] == chain_index_2:
            valuable_ids[id] = chain_index_1

def __split_chains_by_cid(chains):
    filtered_chains = []
    for chain in chains:
        cids = {}
        for row in chain:
            cid = row["cid"]
            cid_chain = cids.get(cid, [])
            cid_chain.append(row)
            cids[cid] = cid_chain
        for cid_chain in cids.values():
            filtered_chains.append(cid_chain)
    return filtered_chains

def read_chains_from_file(filename, delimiter):
    chains_size = -1
    chains = []
    valuable_ids = {}

    with open(filename, encoding="utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter=delimiter)
        line_count = 0
        for row in csv_reader:
            # init the first chain
            if line_count == 0:
                chains_size = __init_new_chain(row["pid"], row["sid"], chains_size, valuable_ids)
                chains.append([])
            line_count += 1

            chain_index_pid = valuable_ids.get(row["pid"], -1)
            chain_index_sid = valuable_ids.get(row["sid"], -1)
            if chain_index_pid < 0 or chain_index_sid < 0:
                if chain_index_pid < 0 and chain_index_sid < 0:
                    chains_size = __init_new_chain(row["pid"], row["sid"], chains_size, valuable_ids)
                    chains.append([])
                    chains[chains_size].append(row)
                elif chain_index_pid >= 0:
                    chains[chain_index_pid].append(row)
                    __add_id(row["sid"], chain_index_pid, valuable_ids)
                else:
                    chains[chain_index_sid].append(row)
                    __add_id(row["pid"], chain_index_sid, valuable_ids)
            else:
                if chain_index_pid == chain_index_sid:
                    chains[chain_index_pid].append(row)
                else:
                    chains[chain_index_pid].append(row)
                    __merge_chains(chains, chain_index_pid, chain_index_sid, valuable_ids)
        f.close()

    # remove empty chains
    chains = list(filter(lambda c: len(c) > 0, chains))
    # split chains with multiple cids inside
    chains = __split_chains_by_cid(chains)
    chains = ChainFactory.create_chains(chains)

    print(f"Chains found: {len(chains)}")
    print(f"Unique ids found: {len(valuable_ids)}")
    return chains

