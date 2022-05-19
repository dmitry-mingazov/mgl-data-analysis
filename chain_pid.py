from file_rw import read_chains_from_file
from filters import filter_chains_bigger_than, filter_chains_smaller_than, group_by_class_name

def print_chain_stats(chains):
    print(f"Size of filtered chains: {len(chains)}")
def print_grouped_chain_stats(grouped_chains):
    for cn in grouped_chains:
        print(f"{cn}: {len(grouped_chains[cn])} chains")

def main():
    input_file = "../logs/primi30krecord.csv"
    # output_file = "../logs/chains/rsu_chain"
    chains = read_chains_from_file(input_file)
    filtered_chains = filter_chains_bigger_than(chains, 3)
    grouped_chains = group_by_class_name(filtered_chains)
    print_grouped_chain_stats(grouped_chains)
    # print_chain_stats(filtered_chains)

if __name__ == "__main__":
    main()
