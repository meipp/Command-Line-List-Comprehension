#!/usr/bin/python3

import sys
import subprocess
import itertools
import re

from comprehension_parser import Parser
from config import *

def command_stdout(command):
    stdout = subprocess.run(command, stdout=subprocess.PIPE).stdout
    for line in stdout.splitlines():
        yield line.decode(SUBPROCESS_CHARSET)

def command_return(command):
    try:
        subprocess.check_output(command)
        return 0
    except subprocess.CalledProcessError as e:
        return e.returncode

#Interpolation Policy
#Replace identifier existing as a variable name: x, {x}
#Escape interpolation: %x, %{x}
def perform_interpolation(command, names, values):
    command = list(command)
    for i in range(len(command)):
        if command[i] in names:
            command[i] = values[names.index(command[i])]
            continue

        interpolate = lambda matching: substitute_interpolation(matching, names, values)
        command[i] = re.sub("({}|{}|%{}|%%|%)".format(IDENTIFIER, "{" + IDENTIFIER + "}", IDENTIFIER), interpolate, command[i])

    return command

#Support function for perform_interpolation
def substitute_interpolation(matching, names, values):
    interpolation = matching.group(1)

    if interpolation == "%%":
        return "%"
    elif interpolation == "%":
        raise RuntimeError()
    elif interpolation.startswith("%{") and interpolation.endswith("}"):
        return interpolation[2:-1]
    elif interpolation.startswith("%"):
        return interpolation[1:]
    elif interpolation.startswith("{") and interpolation.endswith("}"):
        name = interpolation[1:-1]
        if name in names:
            return values[names.index(name)]
        else:
            return interpolation
    elif interpolation in names:
        return values[names.index(interpolation)]
    else:
        return interpolation

def execute_command(command, names, combination, if_):
    for clause in if_:
        #If condition fails, do not yield anything
        clause = perform_interpolation(clause, names, combination)
        if command_return(clause) != 0:
            return

    command = perform_interpolation(command, names, combination)
    yield from command_stdout(command)

def execute_comprehension(expression, for_, if_):
    for_names = [x for (x,y) in for_]
    for_outputs = [command_stdout(y) for (x,y) in for_]

    combinations = itertools.product(*for_outputs)

    for combination in combinations:
        yield from execute_command(expression, for_names, combination, if_)

if __name__ == "__main__":
    #Replace program name with OPEN symbol
    tokens = [OPEN] + sys.argv[1:]

    parser = Parser(tokens)
    comprehension = parser.comprehension()

    for ln in execute_comprehension(*comprehension):
        print(ln)
