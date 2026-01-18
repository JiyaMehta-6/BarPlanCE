import csv
import math

# Standard bar length (in meters)
bar_length = 1200

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
print(req_dtl_list)

# Bar usage logic
bars = []  # List of remaining lengths in each bar

cuts_sch = []
cuts_bar = []
used_len = 0

for i in range(len(req_dtl_list)):
    used_len = sum(cuts_bar)

    if (used_len + req_dtl_list[i]) <= bar_length :
        cuts_bar.append(req_dtl_list[i])
    else:
        cuts_sch.append(cuts_bar)
        cuts_bar = []
        cuts_bar.append(req_dtl_list[i])

    if i+1 == len(req_dtl_list):
        cuts_sch.append(cuts_bar)

print(cuts_sch)

for j in range(len(cuts_sch)):
    # print("Bar ", j+1 ," : " , cuts_sch[j] , "Consumed : " , sum(cuts_sch[j]) , "Wastage : " , bar_length-sum(cuts_sch[j]))
    print(f"Bar {(j+1):>3} : {str(cuts_sch[j]):<30} Consumed : {sum(cuts_sch[j]):>8}   Wastage : {bar_length-sum(cuts_sch[j]):>5}")


# # Results
# print(f"Total bars used: {len(bars)}")
# print(f"Remaining waste in each bar: {bars}")
# print(f"Total waste: {sum(bars)}")

