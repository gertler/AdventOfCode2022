#! /usr/bin/env python3
import sys
import os
import re
from functools import reduce

# Globals
NUM_ROUNDS = 10_000
N_MOST_ACTIVE = 2

class Monkey:
    def __init__(self, items: list = []):
        self.items = items
        self.test_divisor = 1
        self.decisions = {}
        self.num_inspections = 0
    
    def setOperation(self, op_str):
        def add_op(a, b):
            return a + b
        def multiply_op(a, b):
            return a * b

        x = re.search(r"new = (old|\d+) ([\+\*]) (old|\d+)", op_str)
        tokens = x.groups()
        self.op_tokens = [tkn for tkn in tokens]
        if tokens[1] == "+":
            self.op = add_op
        elif tokens[1] == "*":
            self.op = multiply_op
    
    def setTest(self, test_str):
        def _test(operand):
            return operand % self.test_divisor == 0
        
        x = re.search(r"divisible by (\d+)", test_str)
        self.test_divisor = int(x.groups()[0])
        self.test = _test
    
    def setThrow(self, testBool, throw_str):
        x = re.search(r"throw to monkey (\d+)", throw_str)
        throw_id = int(x.groups()[0])
        self.decisions[testBool] = throw_id
    
    def throw(self, to_monkey: object):
        item = self.items.pop(0)
        to_monkey.items.append(item)
    
    def inspectItems(self, lcm):
        throw_decisions = []
        item_idx = 0
        while item_idx < len(self.items):
            item = self.items[item_idx]
            operand1 = item if self.op_tokens[0] == "old" else int(self.op_tokens[0])
            operand2 = item if self.op_tokens[2] == "old" else int(self.op_tokens[2])
            worry = self.op(operand1, operand2)
            worry %= lcm
            self.items[item_idx] = worry

            testBool = self.test(worry)
            to_monkey_id = self.decisions[testBool]
            throw_decisions.append(to_monkey_id)
            item_idx += 1
        self.num_inspections += len(throw_decisions)
        return throw_decisions


def helpParse(monkey: Monkey, slug, string):
    if slug == "Starting":
        monkey.items = [int(x) for x in string.split(", ")]
    elif slug == "Operation":
        monkey.setOperation(string)
    elif slug == "Test":
        monkey.setTest(string)
    elif slug == "true":
        monkey.setThrow(True, string)
    elif slug == "false":
        monkey.setThrow(False, string)


def idToMonkey(id, monkeys):
    return 

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the level of monkey business after 20 rounds of stuff-slinging.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    monkey_business_level = 0
    monkeys = []
    for line in lines:
        x = re.search(r"^Monkey", line)
        y = re.search(r"^\s+(Starting|Operation|Test|If)\s*(true|false)?.*: (.*)$", line)
        if x:
            monkeys.append(Monkey())
        elif y:
            tokens = y.groups()
            slug = tokens[0] if tokens[1] is None else tokens[1]
            helpParse(monkeys[-1], slug, tokens[2])
    
    # print(monkeys)
    divisors = [m.test_divisor for m in monkeys]
    lcm = reduce(lambda x,y: x*y, divisors, 1)

    round = 1
    while round < NUM_ROUNDS + 1:
        for monkey in monkeys:
            throw_decisions = monkey.inspectItems(lcm)
            [monkey.throw(monkeys[to]) for to in throw_decisions]
        # print("After round {}:".format(round))
        # for i in range(len(monkeys)):
        #     items = map(str, monkeys[i].items)
        #     print("Monkey {}: {}".format(i, ', '.join(items)))
        # print("\n")
        round += 1

    num_inspections = [m.num_inspections for m in monkeys]
    num_inspections = sorted(num_inspections)[::-1]
    print(num_inspections)
    monkey_business_level = reduce(lambda x,y: x*y, num_inspections[:N_MOST_ACTIVE], 1)
    print("The level of monkey business after 10,000 rounds is {}".format(monkey_business_level))

    

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