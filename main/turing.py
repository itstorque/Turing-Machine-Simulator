#!/usr/bin/env python3

import sys
import time

#################
#   FUNCTIONS   #
#################

class NoInitialStateDefined(Exception):

    def __init__(self):

        Exception.__init__(self)

    def __str__(self):

        return "The initial state 0 was not found in your turing code"

def display(out, pos, hide=True):

        if hide == True: hide = "\r"
        else: hide = "\n"

        print(" "*100, end="\r")

        RED   = "\033[1;31m"
        BLUE  = "\033[1;34m"
        CYAN  = "\033[1;36m"
        GREEN = "\033[0;32m"
        RESET = "\033[0;0m"
        BOLD  = "\033[;1m"
        REVERSE = "\033[;7m"

        sys.stdout.write(RESET)
        print(''.join(out.slice(pos, False)), end="")

        sys.stdout.write(REVERSE+GREEN)
        print(out[pos], end="")

        sys.stdout.write(REVERSE+RESET)
        print(''.join(out.slice(pos, True)), end=hide)

def decode_states(lines):

    states = {}

    for i in lines:

        if i != "" and i[0]!=";":
            try:
                parse = i.split(' ')
                states.setdefault(parse[0], {})
                states[parse[0]][parse[1]] = parse[2:]
            except IndexError:
                raise YourCodeIsBrokenYouN00b

    if '0' not in states:
        raise NoInitialStateDefined

    return states

def decode_state(states, state, input_val):

    if state not in states:
        raise UndefinedState

    if input_val in states[state]:
        return states[state][input_val]

    return states[state]["*"]

#################
#    CLASSES    #
#################

class TuringTape:

    def __init__(self, init):

        self.tape = dict(enumerate(init))

    def __getitem__(self, i):

        if not isinstance(i,slice):

            try: return self.tape[i]
            except: return "_"

        else:

            raise NotImplementedError

    def slice(self, i, after):

        ans = ""

        r = range(min(self.tape), i)

        if after:
            r = range(i+1, max(self.tape)+1)

        for a in r:

            try: ans += self.tape[a]
            except: ans += "_"

        return ans

    def __setitem__(self, i, val):

        self.tape[i] = val

#################
#      MAIN     #
#################

if __name__ == "__main__":

    dt=0

    with open("main/turing.tmap", encoding="utf-8") as f:

        text = f.read()

        dt = float(text.split("speed->")[1].split("\n")[0])

    lines = sys.argv[1].split('\n')

    input = TuringTape('_'.join(sys.argv[2].split(' ')[1:]))

    steps = 0

    cursor_pos = 0

    display(input, cursor_pos)

    states = decode_states(lines)

    print(states)

    state = '0'

    while state[:4] != 'halt':

        steps += 1

        local_input = input[cursor_pos]

        runtime = decode_state(states, state, local_input)

        state = runtime[2]
        if runtime[0]!="*": input[cursor_pos] = runtime[0]

        if runtime[1]=="r":

            cursor_pos += 1

        elif runtime[1] == "l":

            cursor_pos -= 1

        elif runtime[1] == "*":

            pass

        else:

            raise InvalidMove

        display(input, cursor_pos)
        time.sleep(dt)
    display(input, cursor_pos, hide=False)
    print('Halted.')
    print(steps, "Steps")
