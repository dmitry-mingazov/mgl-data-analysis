# from clustering import create_feature_file
import os
from file_rw import read_chains_from_file, write_chains_on_file, write_chains_on_file_from_to, write_group_chain
from clustering import *
from filters import *
from stats import *
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

def get_arg_input(name, type):
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

filter_actions = {
    1: (filter_chains_bigger_than, [("threshold", "int")], False),
    2: (filter_chains_smaller_than, [("threshold", "int")], False),
    3: (filter_chains_by_group, [("group", "string")], True)
}

order_actions = {
    1: (order_chains_by_column, [("column", "string")], False)
}

delete_actions = {
    1: (delete_duplicate_rows, [], False)
}

group_actions = {
    1: (group_by_first_class, [], False),
    2: (group_by_class_name, [], False),
}

def print_group_actions():
    print("1) Group by first class")
    print("2) Group by predominant class")

def print_delete_actions():
    print("1) Delete duplicate rows inside chains")

def print_order_actions():
    print("1) Order chains by @column")

def print_filter_actions():
    print("1) Filter chains bigger than @threshold")
    print("2) Filter chains smaller than @threshold")

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

    for name, type in args_meta:
        args.append(get_arg_input(name, type))
    return fn(*args)

def main():
    input_file = "../logs/100k_raw.csv"
    output_dir = "../logs/chains/smallerThan3/"
    reports_dir = "../reports/"
    delimiter = ","
    cn = "ProFRMConsProtocollo"


    chains = read_chains_from_file(input_file, delimiter)
    # # print_chain_stats(chains)
    # # filtered_chains = filter_chains_bigger_than(delete_duplicate_rows(chains), 3)
    # fc = delete_duplicate_rows(chains)
    # # fc = filter_chains_bigger_than(fc, 3)
    # fc = filter_chains_smaller_than(fc, 4)
    # fc = order_chains_by_column(fc, "p")
    # write_chains_on_file(fc, output_dir+"chain")
    # return

    # occurences = stats_last_row(fc, "a")
    # print_occurences_stats(occurences, len(fc))

    fc = chains
    gc = {}
    while True:
        # os.system("cls")
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
            print("Work in progress")
        elif choice == "g":
            gc = run_action(fc, gc, print_group_actions, group_actions)
            print("Do you want to discard groups with less chains than @threshold? (If not, type 0)")
            threshold = get_arg_input("threshold", "int")
            if threshold != 0:
                gc = filter_grouped_chains_bigger_than(gc, threshold)
        elif choice == "s":
            print("Work in progress")
        elif choice == "r":
            fc = chains
            gc = {}
        elif choice == "0":
            break

    return
    fc2 = chains
    print_chain_stats(fc2)
    gc = group_by_first_class(fc2)
    # gc = group_by_class_name(fc2)

    fgc = delete_duplicate_chains_by_cn_ordered(gc)

    # print_group_cids(gc[cn])
    print_grouped_chain_stats(fgc)
    # write_group_chain(gc[cn], output_dir, cn)
    # print_chain_stats(fc)
    # write_chains_on_file_from_to(filtered_chains, output_dir, 795, 847)
    # grouped_chains = filter_grouped_chains_smaller_than(group_by_first_class(filtered_chains), 3)
    # create_feature_file(fc2)
    # print_grouped_chain_stats(grouped_chains)
    # grouped_chains = filter_grouped_chains_smaller_than(group_by_class_name(filtered_chains), 8)
    # print(f"Groups: {len(grouped_chains)}")
    # print_grouped_chain_stats(grouped_chains)
    # write_group_chain(grouped_chains["RsuFRMGestioneUtenze"], output_dir, "RsuFRMGestioneUtenze")
    # print_chain_stats(filtered_chains)

if __name__ == "__main__":
    main()
