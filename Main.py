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


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    cc = 0
    sy_table = SymbolTable()
    shift_list = ["A<<", "D<<", "M<<", "A>>", "D>>", "M>>"]
    parser = Parser(input_file)
    all_lines = parser.lines #now all of the lines are ready, and the lines we dont need are deleted
    where_to_add = 16

    for i in range(parser.numoflines):
        parser.line = all_lines[i]
        if '//' in parser.line:
            clearingline = parser.line.split("//")
            line1 = clearingline[0]
            parser.line = line1.replace(" ", "")
        actualcom = parser.symbol()

        if parser.command_type() == "L_COMMAND":
                sy_table.add_entry(actualcom, cc)
        else:
            cc += 1
        parser.advance()


    for i in range(parser.numoflines):
        inst = ""
        parser.line = all_lines[i]
        parser.line = parser.line.strip()
        if '//' in parser.line:
            clearingline = parser.line.split("//")
            parser.line = clearingline[0]
        parser.line = parser.line.replace(" ", "")
        comtype = parser.command_type()
        the_command = parser.symbol()
        the_command = the_command.replace(" ", "")

        if comtype == "A_COMMAND":
            if the_command.isdigit():
                inst += '{0:016b}'.format(int(the_command))
                inst += "\n"
            else:
                if not sy_table.contains(the_command):
                    sy_table.add_entry(the_command, where_to_add)
                    where_to_add += 1
                sym_address = sy_table.get_address(the_command)
                inst += '{0:016b}'.format(sym_address)
                inst += "\n"


        elif comtype == "L_COMMAND":
            continue

        elif comtype == "C_COMMAND":
            the_comp = parser.comp()
            the_dest = parser.dest()
            the_jump = parser.jump()

            if the_comp in shift_list:
                inst += "101"
            else:
                inst += "111"
            inst += str(Code.comp(the_comp)) + str(Code.dest(the_dest)) + str(Code.jump(the_jump)) + "\n"
        output_file.write(inst)
        parser.advance()


    input_file.close()
    output_file.close()







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
