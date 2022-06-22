from Action import ActionGroup, ActionFactory
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

def get_group_action_group():
    _id = "grp"
    desc = "Group"
    input_char = "g"
    _actions = __get_group_chain_actions()
    actions =  ActionFactory.create_actions_from_list(_id, _actions, [])
    return ActionGroup(_id, actions, desc, input_char)

def __get_group_chain_actions():
    return [
        (
            group_by_first_class,
            [],
            "Group by first class"
        ),
        (
            group_by_class_name,
            [],
            "Group by predominant class"
        ),
        (
            group_by_cid,
            [],
            "Group by cid"
        ),
    ]
