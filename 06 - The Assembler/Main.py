"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def first_pass(symbol_table: SymbolTable, parser: Parser) -> None:
    """This func receive a parser and a symbol table and insert into the table
    all the labels in the file"""
    line_counter: int = -1
    while parser.has_more_commands():
        parser.advance()
        if not parser.has_more_commands():
            break
        c_type: str = parser.command_type()
        if c_type == "L_COMMAND":
            symbol: str = parser.symbol()
            if not symbol_table.contains(symbol):
                symbol_table.add_entry(symbol, line_counter + 1)
        else:
            line_counter += 1
    parser.reset_line_counter()


def to_16bit(binary_str: str) -> str:
    """func extend the binary code string into 16 bits length"""
    return binary_str.zfill(16)


def second_pass(symbol_table: SymbolTable, parser: Parser,
                output_file: typing.TextIO):
    """This func codes into binary code the instruction in file and also add
    variables into the symbol table. Func write into output file the resulted
    instructions"""
    var_counter: int = 16
    C_BITS_SIZE: int = 6
    C_COMMAND_START: str = "111"
    while parser.has_more_commands():
        parser.advance()
        if not parser.has_more_commands():
            break
        c_type: str = parser.command_type()
        if c_type == "C_COMMAND":
            dest: str = parser.dest()
            comp: str = parser.comp()
            jump: str = parser.jump()
            c_dest: str = Code.dest(dest)
            c_comp: str = Code.comp(comp)
            c_jump: str = Code.jump(jump)
            a_bit: str = '1' if 'M' in comp else '0'
            if len(c_comp) > C_BITS_SIZE:
                assembled: str = c_comp + c_dest + c_jump  # extended c command << >>
            else:
                assembled: str = C_COMMAND_START + a_bit + c_comp + c_dest + c_jump
            output_file.write(assembled + '\n')

        elif c_type == "A_COMMAND":
            symbol: str = parser.symbol()
            if symbol.isdigit():
                #  the symbol is a number @Num
                bin_code: str = bin(int(symbol))[2:]
                bin_command: str = to_16bit(bin_code)
                output_file.write(bin_command + '\n')
            else:
                if symbol_table.contains(symbol):
                    address: int = symbol_table.get_address(symbol)
                    bin_code: str = bin(int(address))[2:]
                    bin_command: str = to_16bit(bin_code)
                    output_file.write(bin_command + '\n')
                else:
                    symbol_table.add_entry(symbol, var_counter)
                    bin_code: str = bin(int(var_counter))[2:]
                    bin_command: str = to_16bit(bin_code)
                    output_file.write(bin_command + '\n')
                    var_counter += 1


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    parser: Parser = Parser(input_file)
    symbol_table: SymbolTable = SymbolTable()
    first_pass(symbol_table, parser)
    second_pass(symbol_table, parser, output_file)


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
