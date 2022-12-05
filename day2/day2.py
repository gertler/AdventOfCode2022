#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Discover the total score if the Rock, Paper, Scissors strategy guide is totally accurate\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    final_score = 0

    def score(opp, you):
        # Rock, Paper, Scissors
        opp_choices = ['A', 'B', 'C']
        you_choices = ['X', 'Y', 'Z']

        indices = (opp_choices.index(opp), you_choices.index(you))

        selection_score = indices[1] + 1
        outcome_score = 0
        if indices[0] == indices[1]:
            outcome_score = 3
        elif indices[0] == 0 and indices[1] == 2:
            outcome_score = 0
        elif indices[0] == 2 and indices[1] == 0:
            outcome_score = 6
        else:
            outcome_score = 0 if indices[0] > indices[1] else 6
        
        return selection_score + outcome_score

    for line in lines:
        opp, you = line.split()
        final_score += score(opp, you)
    
    print("The total score following the strategy guide (assuming no trickery) is {}".format(final_score))

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