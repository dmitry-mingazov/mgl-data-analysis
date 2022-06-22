from Action import ActionFactory, ActionGroup

def order_chains_by_column(chains, column):
    filtered_chains = []
    for chain in chains:
        ordered = sorted(chain, key=lambda row: row[column])
        filtered_chains.append(ordered)
    return filtered_chains

def get_order_action_group():
    _id = "ord"
    desc = "Order"
    input_char = "o"
    _actions = __get_order_chain_actions()
    actions = ActionFactory.create_actions_from_list(_id, _actions, [])
    return ActionGroup(_id, actions, desc, input_char)

def __get_order_chain_actions():
    return [
        (
            order_chains_by_column,
            [("column", "string")],
            "Order rows inside chains by @column"
        ),
    ]
