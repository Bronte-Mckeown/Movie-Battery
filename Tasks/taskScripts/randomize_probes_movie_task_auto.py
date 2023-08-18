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

# Generate full_sample_order_dictionary
full_sample_order_dictionary = {}

for idx, _ in enumerate(range(num_samples_per_interval)):
    order_dict = generate_order_dict(num_participants, num_samples_per_interval, min_participant_break, probe_interval)
    modified_order_dict = {}
    
    for key, values in order_dict.items():
        modified_key = str(int(key) + (idx * num_participants))
        modified_order_dict[modified_key] = values
        
    full_sample_order_dictionary[idx + 1] = modified_order_dict

# Print the generated dictionaries
for idx, order_dict in full_sample_order_dictionary.items():
    print(f"Order dictionary {idx}:\n", order_dict)
    
    # Apply value_mapping to each order_dict
    for key in order_dict:
        for i in range(len(order_dict[key])):
            if order_dict[key][i] in value_mapping:
                order_dict[key][i] = value_mapping[order_dict[key][i]] + i * probe_coverage_duration_secs

    print(f"Order dictionary {idx} in seconds:\n", order_dict)
