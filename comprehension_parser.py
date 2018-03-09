import re

import sys
from config import *

class Parser:
    def __init__(self, tokens):
        self.position = 0
        self.tokens = tokens

    #Returns triple containing command, input commands, and test commands
    def comprehension(self):
        self.tokens[self.position] == OPEN or self.error("'{}' expected".format(OPEN))
        self.position += 1

        for_part = []
        if_part = []

        expression_part = self.expression()
        if self.tokens[self.position] == FOR:
            self.position += 1
            for_part = self.for_section()
        if self.tokens[self.position] == IF:
            self.position += 1
            if_part = self.if_section()
        
        if self.position >= len(self.tokens) or self.tokens[self.position] != CLOSE:
            self.error("'{}' expected".format(CLOSE))
        self.position += 1
        return (expression_part, for_part, if_part)

    #Return command
    def expression(self):
        expression = []

        while self.position < len(self.tokens):
            if self.tokens[self.position] in [FOR, IF, CLOSE, COMMA]:
                break
            else:
                expression.append(self.tokens[self.position])
                self.position += 1

        return expression

    #Return list of name, input command tuples
    def for_section(self):
        section = []

        while self.position < len(self.tokens):
            if self.tokens[self.position] == COMMA:
                self.position += 1
                continue
            elif self.tokens[self.position] in [IF, CLOSE]:
                break
            else:
                section.append(self.for_statement())

        return section

    #Returns tuple of variable name and input command
    def for_statement(self):
        variable = self.tokens[self.position]
        re.match("\\A{}\\Z".format(IDENTIFIER), variable) or self.error("Illegal variable name '{}'".format(variable))
        self.position += 1

        self.tokens[self.position] == IN or self.error("'{}' expected".format(IN))
        self.position += 1

        variable_input = self.expression()

        return (variable, variable_input)

    #Returns list of test commands
    def if_section(self):
        section = []

        while self.position < len(self.tokens):
            if self.tokens[self.position] == COMMA:
                self.position += 1
                continue
            elif self.tokens[self.position] == CLOSE:
                break
            else:
                section.append(self.expression())

        return section

    def error(self, message):
        spaces = sum(map(len, self.tokens[:self.position])) + self.position
        print("\033[31;1merror: \033[39;21m" + message)
        print(" ".join(self.tokens))
        print(spaces * " " + "\033[32;1m^\033[39;21m")
        sys.exit(1)
