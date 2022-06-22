import csv
import os, errno

import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

def create_dir(directory):
    try:
        os.mkdir(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def write_group_chains_on_files(grouped_chains, directory):
    for cn in grouped_chains:
        chains = grouped_chains[cn]
        write_group_chain(chains, directory, cn)

def write_group_chain(grouped_chains, directory, cn):
    cn_dir = directory + "/" + cn + "/"
    create_dir(cn_dir)
    dir = cn_dir + "chain"
    write_chains_on_file(grouped_chains[cn], dir, "chain")

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

def write_chains_on_file_from_to(chains, directory, file_prefix, start, end):
    print(f"Writing {end-start} chains on file")
    file_index = start
    create_dir(directory)
    for chain in chains[start:end]:
        filename = directory + file_prefix + str(file_index) + ".csv"
        file_index += 1
        write_chain_on_file(chain, filename)

def write_chains_on_file(chains, directory, file_prefix):
    file_index = 1
    print(f"Writing {len(chains)} chains on file")
    create_dir(directory)
    for chain in chains:
        filename = directory + file_prefix + str(file_index) + ".csv"
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

def merge_chains(chains, chain_index_1, chain_index_2, valuable_ids):
    merged_chain = chains[chain_index_1]
    for row in chains[chain_index_2]:
        merged_chain.append(row)
    chains[chain_index_2] = []
    for id in valuable_ids:
        if valuable_ids[id] == chain_index_2:
            valuable_ids[id] = chain_index_1

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

            chain_index_pid = valuable_ids.get(row["pid"], -1)
            chain_index_sid = valuable_ids.get(row["sid"], -1)
            if chain_index_pid < 0 or chain_index_sid < 0:
                if chain_index_pid < 0 and chain_index_sid < 0:
                    chains_size = init_new_chain(row["pid"], row["sid"], chains_size, valuable_ids)
                    chains.append([])
                    chains[chains_size].append(row)
                elif chain_index_pid >= 0:
                    chains[chain_index_pid].append(row)
                    add_id(row["sid"], chain_index_pid, valuable_ids)
                else:
                    chains[chain_index_sid].append(row)
                    add_id(row["pid"], chain_index_sid, valuable_ids)
            else:
                if chain_index_pid == chain_index_sid:
                    chains[chain_index_pid].append(row)
                else:
                    chains[chain_index_pid].append(row)
                    merge_chains(chains, chain_index_pid, chain_index_sid, valuable_ids)
        f.close()
    not_empty_chains = []
    for chain in chains:
        if len(chain) > 0:
            not_empty_chains.append(chain)
    print(f"Chains found: {len(chains)}")
    print(f"Not empty chains: {len(not_empty_chains)}")
    print(f"Unique ids found: {len(valuable_ids)}")
    return not_empty_chains

def convert_chain_to_event_log(chain, index):
    log = {
        "case:concept:name": [],
        "concept:name": [],
        "time:timestamp": [],
    }
    for row in chain:
        log["case:concept:name"].append(index)
        log["concept:name"].append(row["cn"])
        log["time:timestamp"].append(row["ingestionDate"])
    df = pd.DataFrame.from_dict(log)
    df = dataframe_utils.convert_timestamp_columns_in_df(df)
    return log_converter.apply(df)

def filter_not_empty_chains(chains):
    return list(filter(lambda c: len(c) > 0,chains))

def save_chains_as_xes(chains, directory, file_prefix):
    index = 0
    for chain in filter_not_empty_chains(chains):
        index += 1
        event_log = convert_chain_to_event_log(chain, index)
        create_dir(directory)
        filename = directory + file_prefix + str(index) + ".xes"
        xes_exporter.apply(event_log, filename)

def add_id_case_to_chain(chain, id_case):
    filtered_chain = []
    for row in chain:
        row["id_case"] = id_case
        filtered_chain.append(row)
    return filtered_chain

def save_chains_as_csv_log(chains, filename):
    merged_chains = []
    for index, chain in enumerate(chains):
        fc = add_id_case_to_chain(chain, index+1)
        merged_chains += fc
    write_chain_on_file(merged_chains, filename)
    

