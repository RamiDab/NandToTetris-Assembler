"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """
    line = ""
    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.line_list = input_file.read().splitlines()
        self.lines = [line.strip() for line in self.line_list if line.strip() and not line.strip().startswith('//')]
        self.numoflines = len(self.lines)
        self.counter = 0
        for line in self.lines:
            if '//' in line:
                linelist = line.split("//")
                line = linelist[0]
                line = line.replace(" ", "")






    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.counter == (len(self.line_list) -1):
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        if self.has_more_commands():
            self.counter += 1
        return

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        if self.line.startswith('@'):
            return "A_COMMAND"
        elif self.line.startswith('('):
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
        # Your code goes here!
        if self.line.startswith('@'):
            return self.line[1:]
        elif self.line.startswith('('):
            return self.line[1:-1]
        else:
            return self.line

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        splitline1 = self.line.split('=')
        if len(splitline1) == 2:
            return splitline1[0]
        else:
            return "null"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!

        firstsplit = self.line.split(';')
        firstsplit = firstsplit[0].split('=')
        if len(firstsplit) == 2:
            return firstsplit[1]
        return firstsplit[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        splitline = self.line.split(';')
        if len(splitline) == 2:
            return splitline[1]
        else:
            return "null"
