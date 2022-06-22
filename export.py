import csv
import os, errno
import env

from Action import ActionFactory, ActionGroup

import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

def __create_dir(directory):
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
    __create_dir(cn_dir)
    dir = cn_dir + "chain"
    write_chains_on_file(grouped_chains[cn], dir, "chain")

def write_chain_on_file(chain, filename):
    headers = chain[0].keys()
    with open(filename, 'w', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in chain:
            writer.writerow(row.values())
        f.close()

def write_chains_on_file(chains, directory, file_prefix):
    file_index = 1
    print(f"Writing {len(chains)} chains on file")
    __create_dir(directory)
    for chain in chains:
        filename = directory + file_prefix + str(file_index) + ".csv"
        file_index += 1
        write_chain_on_file(chain, filename)

def write_chains_on_file_from_to(chains, directory, file_prefix, start, end):
    print(f"Writing {end-start} chains on file")
    file_index = start
    __create_dir(directory)
    for chain in chains[start:end]:
        filename = directory + file_prefix + str(file_index) + ".csv"
        file_index += 1
        write_chain_on_file(chain, filename)

def save_chains_as_xes(chains, directory, file_prefix):
    index = 0
    for chain in filter_not_empty_chains(chains):
        index += 1
        event_log = convert_chain_to_event_log(chain, index)
        __create_dir(directory)
        filename = directory + file_prefix + str(index) + ".xes"
        xes_exporter.apply(event_log, filename)

def save_chains_as_csv_log(chains, filename):
    merged_chains = []
    for index, chain in enumerate(chains):
        fc = add_id_case_to_chain(chain, index+1)
        merged_chains += fc
    write_chain_on_file(merged_chains, filename)
    

def add_id_case_to_chain(chain, id_case):
    filtered_chain = []
    for row in chain:
        row["id_case"] = id_case
        filtered_chain.append(row)
    return filtered_chain

def filter_not_empty_chains(chains):
    return list(filter(lambda c: len(c) > 0,chains))

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

def create_feature_file(chains):
    headers = {}
    headers["Chain number"] = ""
    feature_file = []
    for chain in chains:
        occurences = {}
        features = {}
        for row in chain:
            class_name = row["cn"][:3]
            occ = occurences.get(class_name, 0) + 1
            occurences[class_name] = occ
            headers[class_name] = ""
        tot = len(chain)
        for cn in occurences:
            features[cn] = occurences[cn] / tot
        feature_file.append(features)
    normalized_feature_file = []
    index = 0
    for row in feature_file:
        normalized_row = {}
        index += 1
        for cn in headers:
            if cn == "Chain number":
                normalized_row[cn] = "chain" + str(index)
                continue
            occ = row.get(cn, 0)
            normalized_row[cn] = occ
        normalized_feature_file.append(normalized_row)
    __write_feature_file(headers, normalized_feature_file)
    # return {headers, feature_file}
        
def __write_feature_file(headers, features):
    filename = "feature_file.csv"
    with open(filename, 'w', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in features:
            writer.writerow(row.values())
        f.close()

def get_export_action_group():
    _id = "exp"
    desc = "Export"
    input_char = "e"
    _actions = __get_export_chain_actions()
    _gactions = __get_export_grouped_chain_actions()
    actions = ActionFactory.create_actions_from_list(_id, _actions, _gactions)
    action_group = ActionGroup(_id, actions, desc, input_char)
    action_group.set_edit_chains(False)
    return action_group

def __get_export_chain_actions():
    return [
        (
            write_chains_on_file,
            [
                ("directory", "string", env.OUTPUT_DIR),
                ("file_prefix", "string", env.FILE_PREFIX)
            ],
            "Export chains as csv (@file_prefix + index), inside @directory"
        ),
        (
            write_chains_on_file_from_to, 
            [
                ("directory", "string", env.OUTPUT_DIR),
                ("file_prefix", "string", env.FILE_PREFIX),
                ("start", "int"),
                ("end", "int")
            ],
            "Export chains as csv (@file_prefix + index) from @start to @end inside @directory"
        ),
        (
            save_chains_as_xes,
            [
                ("directory", "string", env.OUTPUT_DIR),
                ("file_prefix", "string", env.FILE_PREFIX),
            ],
            "Export chains as xes (@file_prefix + index), inside @directory"
        ),
        (

            save_chains_as_csv_log,
            [("filename", "string")],
            "Export chains as csv log to @filename"
        ),
        (
            create_feature_file,
            [],
            "Create feature file"
        )
    ]

def __get_export_grouped_chain_actions():
    return [
        (
            write_group_chain,
            [
                ("directory", "string", env.OUTPUT_DIR),
                ("group", "string")
            ],
            "Export chains of @group inside @directory"
        )
    ]

