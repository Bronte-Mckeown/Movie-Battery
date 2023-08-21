# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:02:15 2023

@author: bront
"""

import random

clip_min = 8
probe_coverage_duration_min = 2 # how often, roughly, do you want to interupt
probe_interval = 20  # seconds
min_participant_break = 80  # seconds
num_samples_per_interval = 10

total_duration = clip_min * 60  # 8 minutes in seconds
probe_coverage_duration_secs = probe_coverage_duration_min * 60  # 2 minutes in seconds
num_probes = clip_min / probe_coverage_duration_min

print ("total clip duration in seconds:", total_duration, "\n")
print (f"""If you want to sample each participant roughly every {probe_coverage_duration_min} minutes / 
{probe_coverage_duration_secs} seconds, each participant can provide {num_probes} probes \n""")

num_participants = probe_coverage_duration_secs // probe_interval
num_participants_full_sample = num_participants * num_samples_per_interval

print (f"""If you want to sample each participant roughly every {probe_coverage_duration_min} minutes,
/ {probe_coverage_duration_secs} seconds and you want to collect a probe across 
participants every {probe_interval} seconds, you need {num_participants} participants and
therefore, {num_participants} different orders. \n""")

print (f"""Therefore, if you want {num_samples_per_interval} observations every {probe_interval} seconds,
you need {num_participants_full_sample} participants. \n""")

# this function checks whether there are more than or equal to three consequtive
# numbers the same (to stop predictability of probe for a participant)
def check_consecutive_same(lst):
    for i in range(len(lst) - 2):
        if lst[i] == lst[i+1] == lst[i+2]:
            return False
    return True

# this function checks that the probes are adequately spaced (e.g., at least 80 seconds a part)
def check_spacing(numbers, min_participant_break, probe_interval):
    for i in range(len(numbers) - 1):
        if abs(numbers[i] - numbers[i+1]) < min_participant_break/probe_interval:
            return False
    return True

def initialize_flexible_dict(num_keys):
    order_dict = {}
    for i in range(1, num_keys + 1):
        key = str(i)
        order_dict[key] = []
    return order_dict

# set condition to false first before loop
condition = False

# while condition is false, keep going until conditions met
while condition == False:
    # set up empty dictionary with as many keys as is equal to numb of orders needed
    order_dict = initialize_flexible_dict(num_participants)
    
    for segment in range(4):
        available_numbers = list(range(1, num_participants+1))
    
        for key in order_dict:
            assigned_number = random.sample(available_numbers, 1)[0]
            available_numbers.remove(assigned_number)
            order_dict[key].append(assigned_number)  # Use append() to add to existing list
    
    condition = all(check_consecutive_same(order_dict[key]) for key in order_dict)
    
    # create reverse orders here

    if condition:
        # Adding values to specific items in each list
        for key in order_dict:
            order_dict[key][1] += num_participants
            order_dict[key][2] += num_participants*2
            order_dict[key][3] += num_participants*3
        
        # Evaluate for spacing less than 3 apart after adding values
        condition = all(check_spacing(order_dict[key],min_participant_break, probe_interval ) for key in order_dict)

print ("in consecutive 'order' space:", order_dict, "\n")

for key in order_dict:
    # print (order_dict[key][1])
    order_dict[key][1] -= num_participants
    order_dict[key][2] -= num_participants*2
    order_dict[key][3] -= num_participants*3

print ("in separate 'order' space:", order_dict, "\n")


# # Create a mapping of values to their corresponding replacements
# value_mapping = {1: 20, 2: 40, 3: 60, 4: 80, 5: 100, 6: 120}

# Calculate the number of keys in the value_mapping dictionary
num_keys_value_mapping = num_participants
# Create a mapping of values to their corresponding replacements
value_mapping = {}
for i in range(1, num_keys_value_mapping + 1):
    value_mapping[i] = probe_interval + (i - 1) * probe_interval

# Iterate through the dictionary
for key in order_dict:
    for i in range(len(order_dict[key])):
        if order_dict[key][i] in value_mapping:
            order_dict[key][i] = value_mapping[order_dict[key][i]] + i * probe_coverage_duration_secs

print ("in seconds:\n", order_dict)
        
        
# you can then get it to repeatedly randomize the keys of the orderered dict
# on each iteration keep a counter, e..g., iteration 1, keys of new dict
# are 1-6 (PS 1-6), then they are (7-12), etc, each time, one of they keys, 
# will have one of the orders
# then, add in to the mainscript.py, just ask for subject number, 
# reminder to never skip a number on the participant list (if a no show, still use that number for the next person, don't skip that number)
# then, make it only accept integers and give an error message
# automatically select probe order based on participant number, which will take info from the big ass dictionary you make
# maybe read that in as a csv
# alternatively, excel, randomize, 1-6. then, next to it, will be like, input
# 12 orders = bigger chunk of participants but 6 chunk contrls equal distribution
    








