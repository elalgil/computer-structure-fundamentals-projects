"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line's end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        self.input_lines = input_file.read().splitlines()
        self.num_lines = len(self.input_lines)
        self.cur_line = -1
        self.vm_commands: dict[str, str] = {"add": "C_ARITHMETIC",
                                            "sub": "C_ARITHMETIC",
                                            "and": "C_ARITHMETIC",
                                            "eq": "C_ARITHMETIC",
                                            "gt": "C_ARITHMETIC",
                                            "lt": "C_ARITHMETIC",
                                            "neg": "C_ARITHMETIC",
                                            "or": "C_ARITHMETIC",
                                            "not": "C_ARITHMETIC",
                                            "pop": "C_POP",
                                            "push": "C_PUSH",
                                            "label": "C_LABEL",
                                            "if-goto": "C_IF",
                                            "goto": "C_LABEL",
                                            "function": "C_FUNCTION",
                                            "return": "C_RETURN",
                                            "call": "C_CALL",
                                            "shiftleft": "C_ARITHMETIC",
                                            "shiftright": "C_ARITHMETIC"}

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.cur_line < self.num_lines

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        self.cur_line += 1
        while self.has_more_commands() and not self.valid_line(
                self.input_lines[self.cur_line]):
            self.cur_line += 1
        if self.has_more_commands():
            self.input_lines[self.cur_line] = self.clean_line(
                self.input_lines[self.cur_line])

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        return self.vm_commands[self.input_lines[self.cur_line].split(" ")[0]]

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        if self.command_type() == "C_ARITHMETIC":
            return self.input_lines[self.cur_line].split(" ")[0]
        return self.input_lines[self.cur_line].split(" ")[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        return int(self.input_lines[self.cur_line].split(" ")[2])

    def valid_line(self, line: str) -> bool:
        line = line.strip()
        if len(line) == 0 or line.startswith('//'):
            return False
        return True

    def clean_line(self, line: str) -> str:
        return ' '.join(line.split("//")[0].split())
