#! /usr/bin/env python3
import sys
import os

# Globals
correct_order = False

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the sum of the indices for the pairs that are in the right order.\n")
    print("\t-h\tPrint this help message\n")


def verifyCorrectOrder(arr1, arr2) -> bool:
    global correct_order
    is_arr1 = hasattr(arr1, '__iter__')
    is_arr2 = hasattr(arr2, '__iter__')

    if is_arr1 and is_arr2:
        zipped = list(zip(arr1, arr2))
        zip_len = len(zipped)
        for left, right in zipped:
            is_done = verifyCorrectOrder(left, right)
            if is_done:
                return True
        leftover_len1 = len(arr1[zip_len:])
        leftover_len2 = len(arr2[zip_len:])
        if leftover_len1 != leftover_len2:
            correct_order = leftover_len1 < leftover_len2
            return True
    elif not is_arr1 and not is_arr2:
        if arr1 != arr2:
            correct_order = arr1 < arr2
            return True
    else:
        is_done = False
        if is_arr1:
            is_done = verifyCorrectOrder(arr1, [arr2])
        else:
            is_done = verifyCorrectOrder([arr1], arr2)
        if is_done:
            return True

def main(input_file_name):
    global correct_order
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    indices_sum = 0
    pairs = []
    pairing = False
    for line in lines:
        validated = line.strip()
        if len(validated) == 0:
            pairing = False
        elif pairing:
            unsafe_line = eval(validated)
            pairs[-1].append(unsafe_line)
        else:
            unsafe_line = eval(validated)
            pairs.append([unsafe_line])
            pairing = True
    
    # Test pairs
    idx = 1
    indices_sum = 0
    for pair in pairs:
        # print(pair[0])
        # print(pair[1])
        correct_order = False
        verifyCorrectOrder(pair[0], pair[1])
        # print(correct_order)
        if correct_order:
            indices_sum += idx
        idx += 1
        correct_order = False
        # print("")
    
    print("The sum of the indices for the pairs that are in the right order is {}".format(indices_sum))


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