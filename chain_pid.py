from file_rw import read_chains_from_file
from filters import filter_chains_smaller_than

def print_chain_stats(chains):
    print(f"Size of filtered chains: {len(chains)}")

def main():
    input_file = "../logs/primi30krecord.csv"
    output_file = "../logs/chains/rsu_chain"
    chains = read_chains_from_file(input_file)
    filtered_chains = filter_chains_smaller_than(chains, 2)
    print_chain_stats(filtered_chains)

if __name__ == "__main__":
    main()
