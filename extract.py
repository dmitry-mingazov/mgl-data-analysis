import csv
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from email import parser

DEFAULT_file = "../logs/10k_raw.csv"
DEFAULT_time_offset = 20000
DEFAULT_group_limit = 10
DEFAULT_verbose = False

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--time", default=DEFAULT_time_offset, type=int)
parser.add_argument("-g", "--group", default=DEFAULT_group_limit, type=int)
parser.add_argument("-f", "--file", default=DEFAULT_file)
parser.add_argument("-v", "--verbose", action="store_true")
args = vars(parser.parse_args())

file = args["file"]
group_limit = args["group"]
time_offset = args["time"]
if args["verbose"]:
    verbose = True 
else:
    verbose = DEFAULT_verbose

groups = 0
group_count = 0

with open(file, encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    prev_time = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names: {" - ".join(row)}')
        line_count += 1

        curr_time = int(row["t"])
        if abs(curr_time - prev_time) > time_offset:
            if group_count > group_limit:
                group_count = 0
                groups += 1
                if verbose:
                    print("###################")
        group_count += 1
        prev_time = curr_time
        if verbose:
            print(row["d"])
        # if line_count > 100:
            # break
    print(f'Groups: {groups}')
    print(f'Counted {line_count} lines')