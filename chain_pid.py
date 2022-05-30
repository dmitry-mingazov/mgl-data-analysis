# from clustering import create_feature_file
import os
from file_rw import read_chains_from_file, write_chains_on_file_from_to, write_group_chain
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
def get_action_input(print_fn, fc_len, max_input):
    while True:
        os.system("cls")
        print(f"Current chains: {fc_len}")
        print_fn()
        choice = int(input("Choice: "))
        if choice in range(1, max_input):
            return choice

filter_actions = {
    1: (filter_chains_bigger_than, [("threshold", "int")]),
    2: (filter_chains_smaller_than, [("threshold", "int")])
}

order_actions = {
    1: (order_chains_by_column, [("column", "string")])
}

delete_actions = {
    1: (delete_duplicate_rows, [])
}

def print_delete_actions():
    print("1) Delete duplicate rows inside chains")

def print_order_actions():
    print("1) Order chains by @column")

def print_filter_actions():
    print("1) Filter chains bigger than @threshold")
    print("2) Filter chains smaller than @threshold")

def run_action(chains, print_fn, actions):
    choice = get_action_input(print_fn, len(chains), len(actions)+1)
    action = actions[choice]
    fn = action[0]
    args_meta = action[1]
    args = [chains]
    for name, type in args_meta:
        args.append(get_arg_input(name, type))
    return fn(*args)

def main():
    input_file = "../logs/100k_raw.csv"
    output_dir = "../logs/chains/"
    reports_dir = "../reports/"
    delimiter = ","
    cn = "ProFRMConsProtocollo"


    chains = read_chains_from_file(input_file, delimiter)
    # print_chain_stats(chains)
    # filtered_chains = filter_chains_bigger_than(delete_duplicate_rows(chains), 3)
    # fc = delete_duplicate_rows(chains)
    # fc = filter_chains_bigger_than(fc, 3)
    # fc = order_chains_by_column(fc, "p")
    # occurences = stats_last_row(fc, "a")
    # print_occurences_stats(occurences, len(fc))

    fc = chains
    while True:
        # os.system("cls")
        print("----------------------")
        print(f"Current chains: {len(fc)}")
        print("----------------------")
        print_action_groups()
        choice = input("Choice: ")
        if choice == "f":
            fc = run_action(fc, print_filter_actions, filter_actions)
        elif choice == "d":
            fc = run_action(fc, print_delete_actions, delete_actions)
        elif choice == "o":
            fc = run_action(fc, print_order_actions, order_actions)
        elif choice == "p":
            print("Work in progress")
            # fc = run_action(fc, print_order_actions, order_actions)
        elif choice == "g":
            print("Work in progress")
        elif choice == "s":
            print("Work in progress")
        elif choice == "r":
            fc = chains
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
