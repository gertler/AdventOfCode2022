#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Finds the item type that appears in both compartments of each Elf's rucksack and sums their priorities.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    priority_sum = 0

    for line in lines:        
        rucksack_size = len(line.strip())
        cmpt1, cmpt2 = (line[:rucksack_size//2], line[rucksack_size//2:])
        shared_item = set(cmpt1).intersection(set(cmpt2))
        shared_item = list(shared_item)[0]
        if shared_item.islower():
            priority_sum += ord(shared_item) - 96
        else:
            priority_sum += ord(shared_item) - 38
    
    print("The sum of priorities for the shared compartment items is {} ".format(priority_sum))

    input_file.close()

if __name__ == "__main__":
    # Check args:
    if len(sys.argv) != 2:
        usage()
        exit(1)
    if sys.argv[1] == "-h":
        usage()
        exit(0)
    if not os.path.isfile(sys.argv[1]):
        usage()
        exit(1)
    main(sys.argv[1])