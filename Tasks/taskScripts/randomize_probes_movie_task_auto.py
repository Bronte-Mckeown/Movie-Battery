# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:03:04 2023

@author: bront
"""

import random

def check_consecutive_same(lst):
    for i in range(len(lst) - 2):
        if lst[i] == lst[i+1] == lst[i+2]:
            return False
    return True

def check_spacing(numbers, min_participant_break, probe_interval):
    for i in range(len(numbers) - 1):
        if abs(numbers[i] - numbers[i+1]) < min_participant_break / probe_interval:
            return False
    return True

def initialize_flexible_dict(num_keys):
    order_dict = {}
    for i in range(1, num_keys + 1):
        key = str(i)
        order_dict[key] = []
    return order_dict

def generate_order_dict(num_participants, num_samples_per_interval, min_participant_break, probe_interval):
    condition = False

    while condition == False:
        order_dict = initialize_flexible_dict(num_participants)
    
        for segment in range(num_probes):
            available_numbers = list(range(1, num_participants + 1))
    
            for key in order_dict:
                assigned_number = random.sample(available_numbers, 1)[0]
                available_numbers.remove(assigned_number)
                order_dict[key].append(assigned_number)
        
        condition = all(check_consecutive_same(order_dict[key]) for key in order_dict)
    
        if condition:
            for key in order_dict:
                for i in range(1, len(order_dict[key])):
                    order_dict[key][i] += num_participants * i
        
            condition = all(check_spacing(order_dict[key], min_participant_break, probe_interval) for key in order_dict)

    for key in order_dict:
        for i in range(1, len(order_dict[key])):
            order_dict[key][i] -= num_participants * i

    return order_dict

def create_value_mapping(num_participants, probe_interval, probe_coverage_duration_secs):
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
value_mapping = create_value_mapping(num_participants, probe_interval, probe_coverage_duration_secs)


order_dict = generate_order_dict(num_participants, num_samples_per_interval, min_participant_break, probe_interval)
    
print("Order dictionary:\n", order_dict, "\n")

# Apply value_mapping to each order_dict
for key in order_dict:
    for i in range(len(order_dict[key])):
        if order_dict[key][i] in value_mapping:
            order_dict[key][i] = value_mapping[order_dict[key][i]] + i * probe_coverage_duration_secs

print("Order dictionary in seconds:\n", order_dict, "\n")

# # Create the new dictionary to store selected keys for each participant
# selected_keys_dict = {}

# # Iterate over num_participants using enumerate
# for participant_num, _ in enumerate(range(num_participants), start=1):
#     # Get three random keys without replacement from the order_dict
#     random_keys = random.sample(list(order_dict.keys()), 3)
#     selected_keys_dict[participant_num] = random_keys

# print("Selected keys dictionary:\n")
# print(selected_keys_dict)

# # Create the new dictionary to store selected orders for each clip and participant
# selected_orders_dict = {}

# # Get the list of clip numbers (assuming clips are numbered 1, 2, and 3)
# clip_numbers = list(range(1, num_clips + 1))

# # Get a list of keys (orders) from order_dict
# order_keys = list(order_dict.keys())

# # Create a list of available orders for each clip
# available_orders = {clip_num: list(order_keys) for clip_num in clip_numbers}

# # Iterate over num_participants
# for participant_num in range(1, num_participants + 1):
#     selected_orders_dict[participant_num] = {}
    
#     # Select an order for each clip
#     for clip_num in clip_numbers:
#         # Select a random order from available_orders for the current clip
#         selected_order = random.choice(available_orders[clip_num])
        
#         # Remove the selected order from the available options
#         available_orders[clip_num].remove(selected_order)
        
#         # Add the selected order to the participant's entry in the dictionary
#         selected_orders_dict[participant_num][clip_num] = selected_order

# print("Selected orders dictionary:\n")
# print(selected_orders_dict)

# # Loop over the outer keys (participant numbers) in the selected_orders_dict
# for participant_num, participant_data in selected_orders_dict.items():
#     # Create a set to store the selected orders for the current participant
#     selected_orders_set = set()
    
#     # Loop over the inner keys (clip numbers) and values (selected orders) for the current participant
#     for clip_num, selected_order in participant_data.items():
#         # Check if the selected order has been seen before
#         if selected_order in selected_orders_set:
#             print("Same order selected for different clips")
#             break  # No need to check further, we found a duplicate
#         else:
#             selected_orders_set.add(selected_order)



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

# now I just want to loop over 










