#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the 3 Elves carrying the most Calories.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    top_carriers_count = 3
    current_most_calories_list = [0] * top_carriers_count
    current_elf_carry_weight = 0
    for line in lines:
        if line.isspace():
            for i in range(top_carriers_count):
                weight = current_most_calories_list[i]
                if current_elf_carry_weight > weight:
                    current_most_calories_list = current_most_calories_list[:i] + [current_elf_carry_weight] + current_most_calories_list[i:top_carriers_count - 1]
                    break
            
            current_elf_carry_weight = 0
            print("Current most calories list is {}".format(current_most_calories_list))
            continue
        weight = int(line)
        current_elf_carry_weight += weight
    
    print("Here are the top {} Elves in terms of Calories carried:")
    for i in range(len(current_most_calories_list)):
        print("Elf #{}: {}".format(i+1, current_most_calories_list[i]))
    print("These Elves in total are carrying {} calories".format(sum(current_most_calories_list)))

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