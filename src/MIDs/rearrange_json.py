#! /usr/bin/env python3

import json 

# Here we will switch key and value and
# write it to a new json for better hash map
# performance in future

new_file = 'n_mids.json'
out_file = 'mids.json'

# Function takes first element in file,
# get it last element from values and
# checks if any other key contain same 
# element and if so - writes {'element': ['key']}
# to new json file.o

# Transforms from {mid: [countryi_name_list]} to
# {country_name: [mid_list]}


def shambles(data):
    new_dict = {}
    # get country names and pick one
    for key, value in data.items():
        current_country = value[-1]
        new_dict[current_country] = [key]
        for key in data.keys():
            if current_country in data[key]:
                new_dict[current_country].append(key)
    return new_dict

if __name__ == "__main__":

    with open(out_file, 'r') as out:
        data = json.load(out)

    result = shambles(data)

    object = json.dumps(result)
    with open(new_file, 'w') as inp:
        inp.write(object)



