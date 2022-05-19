
from file_rw import write_feature_file


def create_feature_file(chains):
    headers = {}
    headers["Chain number"] = ""
    feature_file = []
    for chain in chains:
        occurences = {}
        features = {}
        for row in chain:
            class_name = row["cn"][:3]
            occ = occurences.get(class_name, 0) + 1
            occurences[class_name] = occ
            headers[class_name] = ""
        tot = len(chain)
        for cn in occurences:
            features[cn] = occurences[cn] / tot
        feature_file.append(features)
    normalized_feature_file = []
    index = 0
    for row in feature_file:
        normalized_row = {}
        index += 1
        for cn in headers:
            if cn == "Chain number":
                normalized_row[cn] = "chain" + str(index)
                continue
            occ = row.get(cn, 0)
            normalized_row[cn] = occ
        normalized_feature_file.append(normalized_row)
    write_feature_file(headers, normalized_feature_file)
    # return {headers, feature_file}
        