# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:03:04 2023

@author: bront
"""

import random
import csv
import os

def check_consecutive_same(lst):
    for i in range(len(lst) - 2):
        if lst[i] == lst[i+1] == lst[i+2]:
            return False
    return True

# def check_spacing(numbers, min_participant_break, probe_interval):
#     spacings = set()  # To keep track of encountered spacings
    
#     for i in range(len(numbers) - 1):
#         spacing = abs(numbers[i] - numbers[i+1])
        
#         if spacing < (min_participant_break / probe_interval) or spacing in spacings:
#             return False
        
#         spacings.add(spacing)
    
#     return True

def check_spacing(numbers, min_participant_break, probe_interval):
    spacings = set()
    encountered_spacings = []  # List to store encountered spacings
    
    for i in range(len(numbers) - 1):
        spacing = abs(numbers[i] - numbers[i+1])
        
        if spacing < (min_participant_break / probe_interval) or spacing in spacings:
            return False, []  # Return an empty list along with False
        
        spacings.add(spacing)
        encountered_spacings.append(spacing)  # Save the encountered spacing
    
    return True, encountered_spacings  # Return True and the list of encountered spacings


def initialize_flexible_dict(num_keys):
    order_dict = {}
    for i in range(1, num_keys + 1):
        key = str(i)
        order_dict[key] = []
    return order_dict

def generate_order_dict(num_participants, num_samples_per_interval, min_participant_break, probe_interval):
    condition = False
    spacing_dict = {}  # Initialize spacing dictionary

    while condition == False:
        order_dict = initialize_flexible_dict(num_participants)
        spacing_dict.clear()  # Clear spacing_dict for each attempt
    
        for segment in range(num_probes):
            available_numbers = list(range(1, num_participants + 1))
    
            for key in order_dict:
                assigned_number = random.sample(available_numbers, 1)[0]
                available_numbers.remove(assigned_number)
                order_dict[key].append(assigned_number)
        
        condition = all(check_consecutive_same(order_dict[key]) for key in order_dict)
        
        if condition:
            spacing_dict = {}  # Clear spacing_dict to ensure it only stores spacings for successful order
            
            for key in order_dict:
                for i in range(1, len(order_dict[key])):
                    order_dict[key][i] += num_participants * i
        
            condition = all(check_spacing(order_dict[key], min_participant_break, probe_interval)[0] for key in order_dict)
            
            if condition:
                for key in order_dict:
                    _, spacings = check_spacing(order_dict[key], min_participant_break, probe_interval)
                    spacing_dict[key] = spacings  # Store the spacings in spacing_dict
    
    for key in order_dict:
        for i in range(1, len(order_dict[key])):
            order_dict[key][i] -= num_participants * i

    return order_dict, spacing_dict  # Return both order_dict and spacing_dict
    
    #     if condition:
    #         spacing_dict = {}
    #         for key in order_dict:
    #             for i in range(1, len(order_dict[key])):
    #                 order_dict[key][i] += num_participants * i
        
    #         condition = all(check_spacing(order_dict[key], min_participant_break, probe_interval) for key in order_dict)

    # for key in order_dict:
    #     for i in range(1, len(order_dict[key])):
    #         order_dict[key][i] -= num_participants * i

    # return order_dict

def create_value_mapping(num_participants, probe_interval):
    num_keys_value_mapping = num_participants
    value_mapping = {}
    for i in range(1, num_keys_value_mapping + 1):
        value_mapping[i] = probe_interval + (i - 1) * probe_interval

    return value_mapping


# Experiment parameters
num_clips = 3
clip_min = 8
probe_coverage_duration_min = 2 # how often, roughly, do you want to interupt
probe_interval = 20  # seconds
min_participant_break = 80  # seconds
num_samples_per_interval = 10

# Calculations
total_duration = clip_min * 60  # 8 minutes in seconds
probe_coverage_duration_secs = probe_coverage_duration_min * 60  # 2 minutes in seconds
num_probes = int(clip_min / probe_coverage_duration_min)
num_participants = int(probe_coverage_duration_secs / probe_interval)
num_participants_full_sample = num_participants * num_samples_per_interval

# print out
print ("total clip duration in seconds:", total_duration, "\n")
print (f"""If you want to sample each participant roughly every {probe_coverage_duration_min} minutes / 
{probe_coverage_duration_secs} seconds, each participant can provide {num_probes} probes \n""")
print (f"""If you want to sample each participant roughly every {probe_coverage_duration_min} minutes,
/ {probe_coverage_duration_secs} seconds and you want to collect a probe across 
participants every {probe_interval} seconds, you need {num_participants} participants and
therefore, {num_participants} different orders. \n""")
print (f"""Therefore, if you want {num_samples_per_interval} observations every {probe_interval} seconds,
you need {num_participants_full_sample} participants. \n""")

# Create value_mapping
value_mapping = create_value_mapping(num_participants, probe_interval)

order_dict, dur_dict = generate_order_dict(num_participants, num_samples_per_interval, min_participant_break, probe_interval)
    
print("Order dictionary:\n", order_dict, "\n")
print("Duration dictionary:\n", dur_dict, "\n")

# Apply value_mapping to each order_dict
for key in order_dict:
    print ("key:", key)
    for i in range(len(order_dict[key])):
        print ("i:", i)
        if order_dict[key][i] in value_mapping:
            print (order_dict[key][i])
            order_dict[key][i] = value_mapping[order_dict[key][i]] + i * probe_coverage_duration_secs
            
print("Order dictionary in seconds:\n", order_dict, "\n")

for key in dur_dict:
    for i in range(len(dur_dict[key])):
        dur_dict[key][i] = dur_dict[key][i]*probe_interval
        
print("Duration dictionary in seconds:\n", dur_dict, "\n")

# set absolute path
script_directory = "C:\\Users\\bront\\Documents\\CanadaPostdoc\\audio\\Movie-Battery\\Tasks\\taskScripts\\resources\\Movie_Task\\csv"

# Construct the full path for the CSV file
csv_file_path = os.path.join(script_directory, "probe_orders.csv")

# Convert order_dict to a list of lists for CSV
csv_data = []
for key in order_dict:
    csv_data.append(order_dict[key])

# Create column names for the CSV
column_names = [f"Probe {i+1}" for i in range(num_probes)]

# Save the data to the CSV file
with open(csv_file_path, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the column names
    csv_writer.writerow(column_names)
    
    # Write the data rows
    csv_writer.writerows(csv_data)

print(f"Data saved to {csv_file_path}")


# Get the list of clip numbers (assuming clips are numbered 1, 2, and 3)
clip_numbers = list(range(1, num_clips + 1))

# Get a list of keys (orders) from order_dict
order_keys = list(order_dict.keys())

while True:
    # Create the new dictionary to store selected orders for each clip and participant
    selected_orders_dict = {}
    
    # Create a list of available orders for each clip
    available_orders = {clip_num: list(order_keys) for clip_num in clip_numbers}
    
    # Iterate over num_participants
    for participant_num in range(1, num_participants + 1):
        selected_orders_dict[participant_num] = {}
        
        # Select an order for each clip
        for clip_num in clip_numbers:
            # Select a random order from available_orders for the current clip
            selected_order = random.choice(available_orders[clip_num])
            
            # Remove the selected order from the available options
            available_orders[clip_num].remove(selected_order)
            
            # Add the selected order to the participant's entry in the dictionary
            selected_orders_dict[participant_num][clip_num] = selected_order
        
        # Check for duplicates within the current participant's selected orders
        selected_orders_set = set()
        has_duplicates = False
        for selected_order in selected_orders_dict[participant_num].values():
            if selected_order in selected_orders_set:
                has_duplicates = True
                break
            else:
                selected_orders_set.add(selected_order)
        
        # If duplicates are found, restart the loop to generate new orders
        if has_duplicates:
            break
    else:
        # If no duplicates are found for any participant, exit the loop
        break

print("Selected orders dictionary:\n")
print(selected_orders_dict)

# now I just want to loop over num_samples_per_interval
# randomly shuffle the values of selected_orders_dict
# modify keys according to iteration, so second iteration = keys + num_participants * 2

# Create a dictionary to store shuffled and modified dictionaries
shuffled_dicts = {}

# Loop over num_samples_per_interval
for iteration in range(1, num_samples_per_interval + 1):
    # Shuffle the values in selected_orders_dict
    shuffled_dict = {}
    shuffled_values = list(selected_orders_dict.values())
    random.shuffle(shuffled_values)
    
    # Reassign shuffled values to each participant while keeping keys intact
    shuffled_dict = {participant_num: shuffled_values[i] for i, participant_num in enumerate(selected_orders_dict)}
    print (shuffled_dict)
    
    # Modify keys based on the iteration
    if iteration > 1:
        new_shuffled_dict = {}
        for participant_num, participant_data in shuffled_dict.items():
            new_participant_num = participant_num + num_participants * (iteration - 1)
            new_shuffled_dict[new_participant_num] = participant_data
        shuffled_dict = new_shuffled_dict
    
    shuffled_dicts[iteration] = shuffled_dict
    
# TO DO:
    # probably make it about duration between probes being the same, rather than
    # 3 consecutive orders being the same
    
    # save probe durations of final selection out too
    
    # zero index the order numbers that will be inputted into GUI (so need 0-5, not 1-6)
    
    # save shuffled_dicts as a csv file, where key = participant number column
    # next three columns are populated by inner key's values
    
    # once all that is done, can consider whether you want to automate
    # so only ID needs to be entered, then probes selected from file instead








