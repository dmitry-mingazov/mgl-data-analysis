# from clustering import create_feature_file
from file_rw import read_chains_from_file, write_chains_on_file_from_to, write_group_chain
from filters import *

def print_chain_stats(chains):
    print(f"Size of filtered chains: {len(chains)}")

def print_grouped_chain_stats(grouped_chains):
    for cn in grouped_chains:
        print(f"{cn}: {len(grouped_chains[cn])} chains")

def print_group_cids(chains):
    occurences = {}
    for chain in chains:
        cid = chain[0]["cid"]
        occ = occurences.get(cid, 0) + 1
        occurences[cid] = occ
    for cid in occurences:
        print(f"{cid}: {occurences[cid]} chains")


def main():
    input_file = "../logs/100k_raw.csv"
    output_dir = "../logs/chains/"
    reports_dir = "../reports/"
    delimiter = ","
    cn = "ProFRMAllegati"
    chains = read_chains_from_file(input_file, delimiter)
    # filtered_chains = filter_chains_bigger_than(delete_duplicate_rows(chains), 3)
    fc = filter_chains_bigger_than(chains, 3)
    fc2 = delete_duplicate_rows(fc)
    gc = group_by_first_class(fc2)
    print_group_cids(gc[cn])
    # print_grouped_chain_stats(gc)
    # write_group_chain(gc[cn], output_dir, cn)
    # print_chain_stats(fc)
    # write_chains_on_file_from_to(filtered_chains, output_dir, 795, 847)
    # grouped_chains = filter_grouped_chains_smaller_than(group_by_first_class(filtered_chains), 3)
    # create_feature_file(filtered_chains)
    # print_grouped_chain_stats(grouped_chains)
    # grouped_chains = filter_grouped_chains_smaller_than(group_by_class_name(filtered_chains), 8)
    # print(f"Groups: {len(grouped_chains)}")
    # print_grouped_chain_stats(grouped_chains)
    # write_group_chain(grouped_chains["RsuFRMGestioneUtenze"], output_dir, "RsuFRMGestioneUtenze")
    # print_chain_stats(filtered_chains)

if __name__ == "__main__":
    main()
