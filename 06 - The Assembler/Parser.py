"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from typing import *

class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self._input_lines: List[str] = input_file.read().splitlines()
        self._num_lines: int = len(self._input_lines)
        self._cur_line: int = -1

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self._num_lines > self._cur_line

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
        """Reads the next command from the input and makes it the current command.
        Should be called only if it has_more_commands() is true.
        """
        self._cur_line += 1  # advance the cur_line index
        while self.has_more_commands() and not self.valid_command(
                self._input_lines[self._cur_line]):
            self._cur_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        command: str = self.clean_command()
        if command.startswith('@'):
            return "A_COMMAND"
        elif command.startswith('('):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        command: str = self.clean_command()
        c_type: str = self.command_type()
        if c_type == "A_COMMAND":
            return command[1:]  # remove the '@' symbol from A command
        else:
            return command[1:-1]  # remove the '(', ')' symbol from Labels

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        command: str = self.clean_command()
        if '=' not in command:
            return "null"
        else:
            divided: List[str] = command.split('=')
            return divided[0]
            # return the dest part of command on the left side of the '='

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        command: str = self.clean_command()
        if ';' not in command:
            divided: List[str] = command.split('=')
            return divided[1]

        elif '=' not in command:
            divided: List[str] = command.split(';')
            return divided[0]

        else:
            divided1: List[str] = command.split('=')
            divided2: List[str] = divided1[1].split(';')
            return divided2[0]
        # dividing twice the command and removing the dest and jump parts

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        command: str = self.clean_command()
        if ';' not in command:
            return "null"
        else:
            divided: List[str] = command.split(';')
            return divided[1]
        # return the jump part of command on the right side of the ';'

    def reset_line_counter(self):
        """Func reset the line counter to 0"""
        self._cur_line = -1

    def clean_command(self) -> str:
        line = self._input_lines[self._cur_line]
        # remove in-line comments and spaces
        return ''.join(line.split("//")[0].split())
