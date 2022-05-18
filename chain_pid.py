import csv

# def add_id(id, chain):
#     if(id not in valuable_ids):
#         valuable_ids.append(id)
#         ids_dict[id] = chain

input_file = "../logs/primi30krecord.csv"
output_file = "../logs/result1.csv"
first_pid = "22182028"


valuable_ids = []
ids_dict = {}
curr_chain = 1
valuable_ids.append(first_pid)
filtered_rows = []
headers = []

with open(input_file, encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    line_count = 0
    added = False
    for row in csv_reader:
        # if line_count == 300:
        #     break
        if line_count == 0:
            # if row["pid"]:
            #     add_id(row["pid"], curr_chain)
            # if row["sid"]:
            #     add_id(row["sid"], curr_chain)
            for key in row:
                headers.append(key)
        line_count += 1
        added = False
        if "pid" in row:
            if (row["pid"] in valuable_ids):
                filtered_rows.append(row)
                valuable_ids.append(row["sid"])
                added = True
        if "sid" in row and not added:
            if (row["sid"] in valuable_ids):
                filtered_rows.append(row)
                if "pid" in row:
                    if row["pid"]:
                        valuable_ids.append(row["pid"])
        
    
print(len(filtered_rows))
print(len(valuable_ids))

with open(output_file, 'w', encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in filtered_rows:
        writer.writerow(row.values())
    f.close()
        


