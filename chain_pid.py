# from clustering import create_feature_file
import os
import env
from file_rw import read_chains_from_file, save_chains_as_xes, write_chains_on_file, write_chains_on_file_from_to, write_group_chain
from clustering import *
from filters import *
from print import *

def print_action_groups():
    print("f - Filter")
    print("d - Delete")
    print("o - Order")
    print("p - Print")
    print("g - Group")
    print("s - Save on file")
    print("-----------------------")
    print("r - Reset chains")
    print("0 - Exit")

def get_arg_input(name, type, default_value=None):
    if default_value:
        value = input(f"Insert @{name} value ({default_value}): ")
        if not value:
            print(value)
            value = default_value
    else:
        value = input(f"Insert @{name} value: ")
    if type == "int":
        return int(value)
    else:
        return value

def print_current_chains(chains, grouped_chains):
    print("----------------------")
    print(f"Current chains: {len(chains)}")
    if grouped_chains:
        print(f"Groups: {len(grouped_chains.keys())}")
    else:
        print("Groups: -- no groups created yet --")
    print("----------------------")

def get_action_input(print_fn, chains, grouped_chains, max_input):
    while True:
        os.system("cls")
        print_current_chains(chains, grouped_chains)
        print_fn()
        choice = int(input("Choice: "))
        if choice in range(1, max_input):
            return choice

save_on_file_actions = {
    1: (write_chains_on_file, [("directory", "string", env.OUTPUT_DIR),("file_prefix", "string", env.FILE_PREFIX)], False),
    2: (write_chains_on_file_from_to, [("directory", "string", env.OUTPUT_DIR),("file_prefix", "string", env.FILE_PREFIX), ("start", "int"), ("end", "int")], False),
    3: (write_group_chain, [("directory", "string", env.OUTPUT_DIR), ("group", "string")], True),
    4: (save_chains_as_xes,  [("directory", "string", env.OUTPUT_DIR), ("file_prefix", "string", env.FILE_PREFIX)], False)
}

filter_actions = {
    1: (filter_chains_bigger_than, [("threshold", "int")], False),
    2: (filter_chains_smaller_than, [("threshold", "int")], False),
    3: (filter_chains_by_group, [("group", "string")], True)
}

order_actions = {
    1: (order_chains_by_column, [("column", "string")], False)
}

delete_actions = {
    1: (delete_duplicate_rows, [], False),
    2: (delete_duplicate_chains_by_cn_ordered, [], False)
}

group_actions = {
    1: (group_by_first_class, [], False),
    2: (group_by_class_name, [], False),
}

print_actions = {
    1: (print_grouped_chain_stats, [], True),
    2: (print_stats_first_row, [("column", "string")], False),
    3: (print_stats_last_row, [("column", "string")], False),
}

def print_save_on_file_actions():
    print("1) Save chains as csv (@file_prefix + index), inside @directory")
    print("2) Save chains as csv @file_prefix + index from @start to @end inside @directory")
    print("3) Save chains as of @group as csv inside @directory")
    print("4) Save chains as xes (@file_prefix + index), inside @directory")

def print_print_actions():
    print("1) Print group grouped chains stats")
    print("2) Print occurences of distinct @column in first rows of chains")
    print("3) Print occurences of distinct @column in last rows of chains")

def print_group_actions():
    print("1) Group by first class")
    print("2) Group by predominant class")

def print_delete_actions():
    print("1) Delete duplicate rows inside chains")
    print("2) Delete duplicate chains (by ordered class name)")

def print_order_actions():
    print("1) Order chains by @column")

def print_filter_actions():
    print("1) Filter chains bigger than @threshold")
    print("2) Filter chains smaller than @threshold")
    print("3) Filter chains inside @group")

def run_action(chains, grouped_chains, print_fn, actions):
    choice = get_action_input(print_fn, chains, grouped_chains, len(actions)+1)
    action = actions[choice]
    fn = action[0]
    args_meta = action[1]
    is_grouped_chains = action[2]
    args = []
    if is_grouped_chains:
        if grouped_chains:
            args.append(grouped_chains)
        else:
            print("You can't use this function: no groups created yet")
            return chains
    else:
        args.append(chains)

    for arg_meta in args_meta:
        name = arg_meta[0]
        type = arg_meta[1]
        if len(arg_meta) > 2:
            default_value = arg_meta[2]
            arg = get_arg_input(name, type, default_value)
        else:
            arg = get_arg_input(name, type)
        args.append(arg)
    return fn(*args)

def main():
    print(f"Reading chains inside {env.INPUT_FILE} ...")
    chains = read_chains_from_file(env.INPUT_FILE, env.DELIMITER)

    fc = chains
    gc = {}
    while True:
        print_current_chains(fc, gc)
        print_action_groups()
        choice = input("Choice: ")
        if choice == "f":
            fc = run_action(fc, gc, print_filter_actions, filter_actions)
        elif choice == "d":
            fc = run_action(fc, gc, print_delete_actions, delete_actions)
        elif choice == "o":
            fc = run_action(fc, gc, print_order_actions, order_actions)
        elif choice == "p":
            run_action(fc, gc, print_print_actions, print_actions)
            print("-----------------------")
            input("Press ENTER to continue...")
        elif choice == "g":
            gc = run_action(fc, gc, print_group_actions, group_actions)
            print("Do you want to discard groups with less chains than @threshold? (If not, type 0)")
            threshold = get_arg_input("threshold", "int")
            if threshold != 0:
                gc = filter_grouped_chains_bigger_than(gc, threshold)
        elif choice == "s":
            run_action(fc, gc, print_save_on_file_actions, save_on_file_actions)
            print("-----------------------")
            input("Press ENTER to continue...")
        elif choice == "r":
            fc = chains
            gc = {}
        elif choice == "0":
            break
    return

if __name__ == "__main__":
    main()
