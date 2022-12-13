#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the sum of the indices for the pairs that are in the right order.\n")
    print("\t-h\tPrint this help message\n")


def flattenNthArray(arrOrItem):
    if isinstance(arrOrItem, list):
        for item in arrOrItem:
            yield from flattenNthArray(item)
    else:
        yield arrOrItem


def verifyCorrectOrder(arr1, arr2):
    _arr1 = [x for x in arr1]
    _arr2 = [x for x in arr2]
    while len(_arr2) > 0:
        if len(_arr1) == 0:
            return True
        item1 = _arr1.pop(0)
        item2 = _arr2.pop(0)
        if item1 == item2:
            continue
        return item1 < item2
    return False


def main(input_file_name):
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
        flattened1 = list(flattenNthArray(pair[0]))
        flattened2 = list(flattenNthArray(pair[1]))
        print(flattened1)
        print(flattened2)
        correctOrder = verifyCorrectOrder(flattened1, flattened2)
        print(correctOrder)
        if correctOrder:
            indices_sum += idx
        idx += 1
        print("")
    
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