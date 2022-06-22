#! /usr/bin/python3.9
import env

from file_rw import read_chains_from_file
from filters import get_filter_action_group
from delete import get_delete_action_group
from print import get_print_action_group
from group import get_group_action_group
from order import get_order_action_group
from export import get_export_action_group

from Cli import Cli

def __get_groups():
    return [
        get_filter_action_group(),
        get_delete_action_group(),
        get_print_action_group(),
        get_group_action_group(),
        get_order_action_group(),
        get_export_action_group()
    ]

if __name__ == "__main__":
    cli = Cli(__get_groups())
    cli.print_info(f"Reading chains inside {env.INPUT_FILE} ...")
    original_chains = read_chains_from_file(env.INPUT_FILE, env.DELIMITER)
    chains = original_chains
    cli.set_chains(chains)
    grouped_chains = {}
    while True:
        cli.wait_for_input()
        group = cli.select_group()
        if not group:
            # 'q' inserted
            break

        action = cli.select_action(group)

        if action.is_grouped() and not grouped_chains:
            cli.print_error("You must create groups before using this function")
            continue

        cli.input_action_args(action)

        if action:
            if action.is_grouped():
                input_chains = grouped_chains
            else:
                input_chains = chains
            res = action.run(input_chains)
            if action.edit_chains:
                if action._id[:3] == "grp":
                    grouped_chains = res
                else:
                    chains = res
            cli.set_chains(chains)
            cli.set_grouped_chains(grouped_chains)

