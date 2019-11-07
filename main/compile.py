#!/usr/bin/env python3

import sys
from turing import *
import math

#################
#   CONSTANTS   #
#################

class NotApplicableType(Exception):

    def __init___(self):

        Exception.__init__(self)

    def __str__(self):

        message = "The export file type you specified is not supported. The current supported types are:\n" + '\n  - '.join(SUPPORTED_EXPORT_TYPES)

        return message

#################
#   FUNCTIONS   #
#################

def get_symbols(states):

    symbols = set()

    for _, state_map in decode_states(states).items():

        for param, function in state_map.items():

            symbols.add(param)

            symbols.add(function[0])

    return symbols.difference({"*"})

#################
#    COMPILE    #
#################

def compile(file_name, export_type="ASM", *argv):

    if not export_type in SUPPORTED_EXPORT_TYPES: raise NotApplicableType

    return SUPPORTED_EXPORT_TYPES[export_type](file_name, argv)

def compile_asm(file_name, *argv):

    lines = file_name.split('\n')

    symbols = get_symbols(lines)

    reg_size = 32

    bits_per_symbol = math.ceil(math.log2(len(symbols)))

    num_per_register = math.floor(reg_size/bits_per_symbol)

    symbol_map = {}

    n = 0

    format_map = '{0:0'+str(bits_per_symbol)+'b}'

    for symbol in symbols:

        symbol_map[symbol] = format_map.format(n)

        n += 1

    print(symbol_map, num_per_register)

    return


SUPPORTED_EXPORT_TYPES = {"ASM": compile_asm}

if __name__=="__main__":

    palindrome_code = """
0 0 _ r 1o
0 1 _ r 1i
0 _ _ * accept     ; Empty input

; State 1o, 1i: find the rightmost symbol
1o _ _ l 2o
1o * * r 1o

1i _ _ l 2i
1i * * r 1i

; State 2o, 2i: check if the rightmost symbol matches the most recently read left-hand symbol
2o 0 _ l 3
2o _ _ * accept
2o * * * reject

2i 1 _ l 3
2i _ _ * accept
2i * * * reject

; State 3, 4: return to left end of remaining input
3 _ _ * accept
3 * * l 4
4 * * l 4
4 _ _ r 0  ; Back to the beginning

accept * : r accept2
accept2 * ) * halt-accept

reject _ : r reject2
reject * _ l reject
reject2 * ( * halt-reject"""

    print(sys.argv[1])

    print(compile(palindrome_code))
