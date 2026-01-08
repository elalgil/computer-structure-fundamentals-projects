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
        # A good place to start is to read all the lines of the input:
        self.input_lines = input_file.read().splitlines()
        self._num_lines: int = len(self.input_lines)
        self._cur_line: int = -1

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self._cur_line <= self._num_lines - 1

    def valid_command(self, command: str) -> bool:
        """this func receive a string command and return true if it does not
        contain white spaces or labels and false otherwise"""
        if command is None:
            return False
        stripped = command.strip()
        if stripped == "" or stripped.startswith("//"):
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self._cur_line += 1  # advance the cur_line index
        while self.has_more_commands() and not self.valid_command(
                self.input_lines[self._cur_line]):
            self._cur_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        ARITHMETICS: typing.List[str] = ["add", "sub", "neg", "eq", "gt", "lt",
                                         "and", "or", "not", "shiftleft",
                                         "shiftright"]
        command: str = self.clean_command()
        if command in ARITHMETICS:
            return "C_ARITHMETIC"
        elif command.startswith('push'):
            return "C_PUSH"
        elif command.startswith('pop'):
            return "C_POP"
        elif command.startswith('label'):
            return "C_LABEL"
        elif command.startswith('goto'):
            return "C_GOTO"
        elif command.startswith('if'):
            return "C_IF"
        elif command.startswith('function'):
            return "C_FUNCTION"
        elif command.startswith('return'):
            return "C_RETURN"
        else:
            return "C_CALL"

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        ARITHMETICS: typing.List[str] = ["add", "sub", "neg", "eq", "gt", "lt",
                                         "and", "or", "not", "shiftleft",
                                         "shiftright"]
        command: str = self.clean_command()
        tokens = command.split()
        op = tokens[0]
        if op in ARITHMETICS:
            return op
        else:
            return tokens[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        command: str = self.clean_command()
        parms: typing.List[str] = command.split()
        return int(parms[2])

    def clean_command(self) -> str:
        line = self.input_lines[self._cur_line]
        # remove inline comments
        return ' '.join(line.split("//")[0].split())
