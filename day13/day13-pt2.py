#! /usr/bin/env python3
import sys
import os

# Globals
correct_order = False
DIVIDERS = [
[[2]],
[[6]]
]

class Packet:
    def __init__(self, data):
        self.data = data
    
    def __lt__(self, __o: object) -> bool:
        global correct_order
        verifyCorrectOrder(self.data, __o.data)
        ret = correct_order
        correct_order = False
        return ret

    # def __eq__(self, __o: object) -> bool:
    #     pass


def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the decoder key for the distress signal given the input packets.\n")
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

    decoder_key = 1
    packets = []
    for line in lines:
        validated = line.strip()
        if len(validated) == 0:
            continue
        unsafe_line = eval(validated)
        packets.append(Packet(unsafe_line))
    
    # Add divider packets
    packets += [Packet(d) for d in DIVIDERS]

    # Sort packets
    packets.sort()
    dividers_str = list(map(str, DIVIDERS))
    idx = 1
    for packet in packets:
        if str(packet.data) in dividers_str:
            decoder_key *= idx
        print(packet.data)
        idx += 1
    
    print("The decoder key for the distress signal is {}".format(decoder_key))


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