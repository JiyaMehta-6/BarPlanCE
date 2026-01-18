import timeit
import csv
import math 
# import panda

def generate_combinations(data, start, path):

    global all_possible_combi_list
    #global all_possible_combi_list
    # Calculate the sum of the current path
    current_sum = sum(path)
    
    # If the current sum exceeds 12, stop further combinations in this sequence
    if current_sum > 1200:
        return

    # Print the current combination (if it's not empty)
    if path:
        all_possible_combi_list.append(path)
        # print(list(path))
    
    # Iterate through the data starting from the current index
    for i in range(start, len(data)):
        # Include the current element and recurse
        generate_combinations(data, i + 1, path + [data[i]])
    

def get_list():
    cut_list = [1,2,3,4]
    # cut_list = [1,2,3,4,5,6,7,8,9]
    # cut_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    return(cut_list)


def get_csv_list():

    filename = "req.csv"

    # Read the CSV
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        req_list = list(reader)

    # Flatten into list of individual required pieces
    req_dtl_list = []
    try:
        for row in req_list:
            row[0] = math.ceil(float(row[0]))
            length = int(row[0])
            qty = int(row[1])
            req_dtl_list.extend([length] * qty)

    except ValueError as e:
        raise ValueError("Invalid data in CSV file. Ensure all values are numeric")

    # Sort in descending order for better greedy packing
    req_dtl_list.sort()
    all_possible_combi_list = req_dtl_list
    print(all_possible_combi_list)
    return (req_dtl_list)

# =====================================================================================

# Standard bar length (in meters)
bar_length = 1200

all_possible_combi_list = []
no_duplicate_list = []

# cut_len_req_list = get_list()
cut_len_req_list = get_csv_list()


def get_all_possible_combi():

    global all_possible_combi_list

    # print(cut_len_req_list)
    # print(generate_combinations(cut_len_req_list, 0, []))
    generate_combinations(cut_len_req_list, 0, [])
    # print(all_possible_combi_list)

    # remove duplicate combi
    no_duplicate_list= []
    for combi in all_possible_combi_list:
        if combi not in no_duplicate_list:
            no_duplicate_list.append(combi)

    all_possible_combi_list=[]
    all_possible_combi_list = no_duplicate_list
    print(all_possible_combi_list)
    del no_duplicate_list

    print(all_possible_combi_list)

if __name__ == '__main__':

    execution_time1 = timeit.timeit(get_all_possible_combi, number=1)

    print(f"Execution time : {execution_time1} s")
    

# Bar usage logic
# Bar usage logic
cuts_sch = []
cuts_bar = []
used_len = 0

for i in range(len(all_possible_combi_list)):
    if sum(sum(cuts)for cuts in cuts_bar) + sum(all_possible_combi_list[i]) <= bar_length:
        cuts_bar.append(all_possible_combi_list[i])
    else:
        cuts_sch.append(cuts_bar)
        cuts_bar = [all_possible_combi_list[i]]  # Start new bar with current cut

# Add the last bar if it has any cuts
if cuts_bar:
    cuts_sch.append(cuts_bar)

# Print results
for j, bar in enumerate(cuts_sch, 1):
    used_length = sum(bar)
    waste = bar_length - used_length

print("bars used = ", len(cuts_bar) )
print("schedule : ", cuts_sch)
print("wastage = ", waste)