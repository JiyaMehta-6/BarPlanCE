
import csv
import math 
import pandas as pd


def generate_combinations(data, start, path):
    
    global all_possible_combi_list

    # Calculate the sum of the current path
    current_sum = sum(path)
    
    # If the current sum exceeds 12, stop further combinations in this sequence
    if current_sum > 1200:
        return

    # Print the current combination (if it's not empty)
    if path:
        all_possible_combi_list.append(tuple(path))
        # print(tuple(path))
    
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
    return (req_dtl_list)

# =====================================================================================

# Standard bar length (in meters)
bar_length = 1200

# cut_len_req_list = get_list()
cut_len_req_list = get_csv_list()

all_possible_combi_list = []

def get_all_possible_combi():

    global all_possible_combi_list

    #print(cut_len_req_list)
    #print(generate_combinations(cut_len_req_list, 0, []))
    generate_combinations(cut_len_req_list, 0, [])

    # remove duplicate combi
    no_duplicate_list= []
    for combi in all_possible_combi_list:
        if combi not in no_duplicate_list:
            no_duplicate_list.append(combi)

    all_possible_combi_list=[]
    all_possible_combi_list = no_duplicate_list
    del no_duplicate_list
    # print(all_possible_combi_list)


if __name__ == '__main__':

    get_all_possible_combi()
    
    all_possible_combi_df = pd.DataFrame(all_possible_combi_list)
    # print(all_possible_combi_list)
    # print(all_possible_combi_df)

    # Add a new column with the sum of each row
    all_possible_combi_df['Sum'] = all_possible_combi_df.sum(axis=1)

    # Convert the DataFrame to integers while keeping NaN values
    all_possible_combi_df_int = all_possible_combi_df.apply(lambda x: x.astype('Int64'))  # Use 'Int64' to allow NaN values
    all_possible_combi_df = all_possible_combi_df_int.copy()

    all_possible_combi_sort_df = all_possible_combi_df.sort_values(by='Sum',ascending=False)
    # print(all_possible_combi_sort_df)   

    # -------------------------------------------------------------------------------------------------

    cut_len_req_list_i = cut_len_req_list.copy()
    # print(cut_len_req_list) value contained
    all_possible_combi_sort_df_i = all_possible_combi_sort_df.copy()
    cut_schedule = []
    recomendation_index = 0

    # print(all_possible_combi_sort_df_i)
    # print(cut_len_req_list_i)

    while len(cut_len_req_list_i):
        # print(recomendation_index)
                
        cut_recomonded = all_possible_combi_sort_df_i.iloc[recomendation_index][:-1]
        cut_recomonded = cut_recomonded.dropna()
        # print(cut_recomonded)
        # print(cut_len_req_list_i)

        match_found = False
        for cut_i in cut_recomonded:
            if cut_i in cut_len_req_list_i:
                match_found = True
            else:
                match_found = False
                break

        if match_found:
            # print( 'Bar present')
            recomendation_index = 0
            cut_schedule.append(cut_recomonded.tolist())
            for item in cut_recomonded:
                if item in cut_len_req_list_i:
                    cut_len_req_list_i.remove(item)
        else:
            recomendation_index = recomendation_index +1
            # print( 'Bar abseny')

        #print(cut_len_req_list)
        # print(cut_len_req_list_i)

    with open('Bar Cut Result.txt', 'w') as file:
        # file.write('Requirement of bars : '+ str(cut_len_req_list ))
        file.write('Requirement of bars : \n')

        str_out = ' ' * 6
        for cut_len_req in cut_len_req_list:
            if (len(str_out) + len(str(cut_len_req)))<80:
                if len(str_out)>6:
                    str_out = str_out + ', '
                str_out = str_out + f'{cut_len_req}'
            else:
                file.write(str_out + '\n')
                str_out = ' ' * 6 + f'{cut_len_req}'
        file.write(str_out + '\n')

        file.write('\nRecommended schedule :\n')
        for j in range(len(cut_schedule)):
            # print("Bar ", j+1 ," : " , cuts_sch[j] , "Consumed : " , sum(cuts_sch[j]) , "Wastage : " , bar_length-sum(cuts_sch[j]))
            # print(f"Bar {(j+1):>3} : {str(cut_schedule[j]):<30} Consumed : {sum(cut_schedule[j]):>4}   Wastage : {bar_length-sum(cut_schedule[j]):>4}")       
            file.write(f"Bar {(j+1):>3} : {str(cut_schedule[j]):<30} Consumed : {sum(cut_schedule[j]):>4}   Wastage : {bar_length-sum(cut_schedule[j]):>4}\n")




        



