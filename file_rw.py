import csv
import os, errno

def write_group_chains_on_files(grouped_chains, directory):
    for cn in grouped_chains:
        chains = grouped_chains[cn]
        write_group_chain(chains, directory, cn)

def write_group_chain(chains, directory, cn):
    cn_dir = directory + "/" + cn + "/"
    try:
        os.makedirs(cn_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    file_prefix = cn_dir + cn + "chain"
    write_chains_on_file(chains, file_prefix)

def write_feature_file(headers, features):
    filename = "feature_file.csv"
    with open(filename, 'w', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in features:
            writer.writerow(row.values())
        f.close()

def write_chain_on_file(chain, filename):
    headers = chain[0].keys()
    with open(filename, 'w', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in chain:
            writer.writerow(row.values())
        f.close()

def write_chains_on_file_from_to(chains, file_prefix, start, end):
    file_index = start
    for chain in chains[start:end]:
        filename = file_prefix + str(file_index) + ".csv"
        file_index += 1
        write_chain_on_file(chain, filename)

def write_chains_on_file(chains, file_prefix):
    file_index = 1
    print(f"Writing {len(chains)} on file")
    for chain in chains:
        filename = file_prefix + str(file_index) + ".csv"
        file_index += 1
        write_chain_on_file(chain, filename)

def add_id(id, chain_index, valuable_ids):
    if (id not in valuable_ids) and id:
        valuable_ids[id] = chain_index

def init_new_chain(id1, id2, chains_size, valuable_ids):
    chains_size += 1
    if id1:
        add_id(id1, chains_size, valuable_ids)
    if id2:
        add_id(id2, chains_size, valuable_ids)
    return chains_size


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
                chains_size = init_new_chain(row["pid"], row["sid"], chains_size, valuable_ids)
                chains.append([])
            line_count += 1
            # if pid is present, save the sid and add the row to the relative chain
            chain_index = valuable_ids.get(row["pid"], -1)
            if chain_index >= 0:
                chains[chain_index].append(row)
                add_id(row["sid"], chain_index, valuable_ids)
                continue
            # if sid is present, save the pid and add the row the relative chain
            chain_index = valuable_ids.get(row["sid"], -1)
            if chain_index >= 0:
                chains[chain_index].append(row)
                add_id(row["pid"], chain_index, valuable_ids)
                continue
            # if this code is reached, this row belongs to a new chain
            chains_size = init_new_chain(row["pid"], row["sid"], chains_size, valuable_ids)
            chains.append([])
            chains[chains_size].append(row)
        f.close()
    print(f"Chains found: {len(chains)}")
    print(f"Unique ids found: {len(valuable_ids)}")
    return chains
            


