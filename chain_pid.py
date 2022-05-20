# from clustering import create_feature_file
from file_rw import read_chains_from_file, write_group_chain
from filters import *

def print_chain_stats(chains):
    print(f"Size of filtered chains: {len(chains)}")
def print_grouped_chain_stats(grouped_chains):
    for cn in grouped_chains:
        print(f"{cn}: {len(grouped_chains[cn])} chains")

def main():
    input_file = "../logs/primi30krecord.csv"
    output_dir = "../logs/chains/"
    chains = read_chains_from_file(input_file)
    # filtered_chains = filter_chains_bigger_than(delete_duplicate_rows(chains), 3)
    filtered_chains = filter_chains_bigger_than(chains, 3)
    grouped_chains = filter_grouped_chains_smaller_than(group_by_first_class(filtered_chains), 3)
    # create_feature_file(filtered_chains)
    print_grouped_chain_stats(grouped_chains)
    # grouped_chains = filter_grouped_chains_smaller_than(group_by_class_name(filtered_chains), 8)
    # print(f"Groups: {len(grouped_chains)}")
    # print_grouped_chain_stats(grouped_chains)
    # write_group_chain(grouped_chains["RsuFRMGestioneUtenze"], output_dir, "RsuFRMGestioneUtenze")
    # print_chain_stats(filtered_chains)

if __name__ == "__main__":
    main()
