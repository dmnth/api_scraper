#! /usr/bin/env python3

import itertools
import os
import sys

def save_iter():
    if os.path.isfile('save_file.txt'):
        with open('save_file.txt', 'r') as save:
            start_point = int(save.read())
    else:
        start_point = 0 

    items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    all_combos = itertools.product(items, repeat=9) 

    #Start at start point and stop at none
    combos = itertools.islice(all_combos, start_point, None)
    for i, comb in enumerate(combos, start=start_point):
        try:
            print(i, comb)
        except KeyboardInterrupt:
            print(f'next time will start from {i}')
            with open('save_file.txt', 'w') as outfile:
                outfile.write(str(i))
            sys.exit()

if __name__ == "__main__":
    save_iter()
