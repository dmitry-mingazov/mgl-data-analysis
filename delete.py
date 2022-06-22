from Action import ActionFactory, ActionGroup

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

def get_delete_action_group():
    _id = "dlt"
    input_char = "d"
    desc = "Delete"
    _actions = __get_delete_chain_actions()
    _gactions = __get_delete_grouped_chain_actions()
    actions = ActionFactory.create_actions_from_list(_id, _actions, _gactions)
    return ActionGroup(_id, actions, desc, input_char)


def __get_delete_chain_actions():
    return [
        (
            delete_duplicate_rows,
            [],
            "Delete duplicate rows"
        ),
        (
            delete_duplicate_chains_by_cn_ordered,
            [],
            "Delete duplicate chains by class name ordered"
        ),
    ]

def __get_delete_grouped_chain_actions():
    return []

