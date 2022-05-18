import csv

input_file = "../logs/primi30krecord.csv"
output_file = "../logs/chains/chain"
# first_pid = "22182028"


valuable_ids = {} 
# ids_dict = {}
curr_chain = 0
# valuable_ids.append(first_pid)
filtered_chains = []
filtered_chains.append([])
headers = []

def add_id(id, chain):
    if(id not in valuable_ids):
        valuable_ids[id] = chain
        # valuable_ids.append(id)
        # ids_dict[id] = chain

def init_new_chain(id1, id2):
    global curr_chain 
    curr_chain += 1
    if id1:
        add_id(id1, curr_chain)
    if id2:
        add_id(id2, curr_chain)
    filtered_chains.append([])

with open(input_file, encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    line_count = 0
    added = False
    for row in csv_reader:
        # if line_count == 300:
        #     break
        if line_count == 0:
            if row["pid"]:
                add_id(row["pid"], curr_chain)
            if row["sid"]:
                add_id(row["sid"], curr_chain)
            for key in row:
                headers.append(key)
        line_count += 1
        added = False
        chain = valuable_ids.get(row["pid"], -1)
        if chain >= 0:
            # chain = ids_dict.get(row["pid"])
            filtered_chains[chain].append(row)
            if row["sid"] not in valuable_ids:
                add_id(row["sid"], chain)
            # valuable_ids.append(row["sid"])
            added = True
        if not added:
            chain = valuable_ids.get(row["sid"], -1)
            if chain >= 0:
                # chain = ids_dict[row["sid"]]
                filtered_chains[chain].append(row)
                if "pid" in row:
                    if row["pid"]:
                        add_id(row["pid"], chain)
                added = True
        if not added:
            init_new_chain(row["pid"], row["sid"])
            filtered_chains[curr_chain].append(row)

        
    
print(f"Chains: {len(filtered_chains)}")
print(f"Valuable ids: {len(valuable_ids)}")

# short_chains = []
# long_chains = 
# filtered_chains_len = len(filtered_chains)
# chain_length = {}

# for chain in filtered_chains:
#     length = len(chain)
#     curr_len = chain_length.get(length, 0)
#     chain_length[length] = curr_len + 1
#     if len(chain) < 10:
#         short_chains.append(chain)
# chain_lengths_ordered = sorted(chain_length.keys())

# for length in chain_lengths_ordered:
#     num_chains = chain_length[length]
#     perc = num_chains / filtered_chains_len * 100
#     print(f"{chain_length[length]} chains of {length} rows ({perc}%)")
# print(f"Short chains: {len(short_chains)}")

# exit(1)

# with open("../logs/chains/short_chain_less2.csv", 'w', encoding="utf-8", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(headers)
#     for short_chain in short_chains:
#         for row in short_chain:
#             writer.writerow(row.values())
#     f.close()


# exit(1)
curr_file_i = 1
for chain in filtered_chains:
    filename = output_file + str(curr_file_i) + ".csv"
    curr_file_i += 1
    with open(filename, 'w', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in chain:
            writer.writerow(row.values())
        f.close()
        


