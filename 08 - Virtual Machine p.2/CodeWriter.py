"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self._output_stream: typing.TextIO = output_stream
        self._file_name = ""
        self._current_label_arithmetic = 0
        self._function_name = ""
        self._cur_function_calls = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self._file_name = filename

    def arithmetic_calc_two_args(self) -> str:
        output = "@SP\nAM=M-1\nD=M\nA=A-1\n"
        return output

    def arithmetic_calc_one_arg(self) -> str:
        output = "@SP\nA=M-1\n"
        return output

    def add_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_two_args())
        self._output_stream.write("M=M+D\n")

    def sub_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_two_args())
        self._output_stream.write("M=M-D\n")

    def and_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_two_args())
        self._output_stream.write("M=M&D\n")

    def or_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_two_args())
        self._output_stream.write("M=M|D\n")

    def neg_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_one_arg())
        self._output_stream.write("M=-M\n")

    def not_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_one_arg())
        self._output_stream.write("M=!M\n")

    def shiftleft_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_one_arg())
        self._output_stream.write("M=M<<\n")

    def shiftright_asm(self) -> None:
        self._output_stream.write(self.arithmetic_calc_one_arg())
        self._output_stream.write("M=M>>\n")

    def arithmetic_comparison_commands(self, jmp_type: str) -> str:
        """
        "@SP\n"
        "A=M-1\n"
        "D=M\n"
        "@POSEY" + str() + "\n"
        "D;JGE\n"
        "(NEGY" + str() + ")\n"
        "@SP\n"
        "A=M-1\n"
        "A=A-1\n"
        "D=M\n"
        "@SAMESIGN" + str() + "\n"
        "D;JLT\n"
        "// x>= 0 and y<0 - always true for gt (jump_type JLE), always false for lt (jump_type JGE) \n"
        "@SP\n"
        "A=M-1\n"
        "D=M\n"
        "@PUSHTRUE" + str() + "\n"
        "D;" + jump_type + "\n"
        "@PUSHFALSE" + str() + "\n"
        "0;JMP\n"

        "(POSEY" + str() + ")\n"
        "@SP\n"
        "A=M-1\n"
        "A=A-1\n"
        "D=M\n"
        "@SAMESIGN" + str() + "\n"
        "D;JGE\n"
        "// y>= 0 and x<0 - always false for gt (jump_type JLE), always true for lt (jump_type JGE)\n"
        "@SP\n"
        "A=M-1\n"
        "A=A-1\n"
        "D=M\n"
        "@PUSHFALSE" + str() + "\n"
        "D;" + jump_type + "\n"
        "@PUSHTRUE" + str() + "\n"
        "0;JMP\n"

        "(SAMESIGN" + str() + ")\n"
        "@SP\n"
        "A=M-1\n"
        "D=M\n"
        "A=A-1\n"
        "D=M-D\n"
        "@PUSHFALSE" + str() + "\n"
        "D;" + jump_type + "\n"
        "(PUSHTRUE" + str() + ")\n"
        "@SP\n"
        "D=M-1\n"
        "A=D-1\n"
        "M=-1\n"
        "@CONTINUE" + str() + "\n"
        "0;JMP\n"
        "(PUSHFALSE" + str() +")\n"
        "@SP\n"
        "D=M-1\n"
        "A=D-1\n"
        "M=0\n"
        "(CONTINUE" + str() + ")\n"
        "@SP\n"
        "M=M-1\n"
        """
        self._current_label_arithmetic += 1
        command: str = ""
        command += "@SP\n"
        command += "A=M-1\n"
        command += "D=M\n"
        command += "@POSEY" + str(self._current_label_arithmetic) + "\n"
        command += "D;JGE\n"
        command += "(NEGY" + str(self._current_label_arithmetic) + ")\n"
        command += "@SP\n"
        command += "A=M-1\n"
        command += "A=A-1\n"
        command += "D=M\n"
        command += "@SAMESIGN" + str(self._current_label_arithmetic) + "\n"
        command += "D;JLT\n"
        command += "// x>= 0 and y<0 - always true for gt (jump_type JLE), always false for lt (jump_type JGE) \n"
        command += "@SP\n"
        command += "A=M-1\n"
        command += "D=M\n"
        command += "@PUSHTRUE" + str(self._current_label_arithmetic) + "\n"
        command += "D;" + jmp_type + "\n"
        command += "@PUSHFALSE" + str(self._current_label_arithmetic) + "\n"
        command += "0;JMP\n"

        command += "(POSEY" + str(self._current_label_arithmetic) + ")\n"
        command += "@SP\n"
        command += "A=M-1\n"
        command += "A=A-1\n"
        command += "D=M\n"
        command += "@SAMESIGN" + str(self._current_label_arithmetic) + "\n"
        command += "D;JGE\n"
        command += "// y>= 0 and x<0 - always false for gt (jump_type JLE), always true for lt (jump_type JGE)\n"
        command += "@SP\n"
        command += "A=M-1\n"
        command += "A=A-1\n"
        command += "D=M\n"
        command += "@PUSHFALSE" + str(self._current_label_arithmetic) + "\n"
        command += "D;" + jmp_type + "\n"
        command += "@PUSHTRUE" + str(self._current_label_arithmetic) + "\n"
        command += "0;JMP\n"

        command += "(SAMESIGN" + str(self._current_label_arithmetic) + ")\n"
        command += "@SP\n"
        command += "A=M-1\n"
        command += "D=M\n"
        command += "A=A-1\n"
        command += "D=M-D\n"
        command += "@PUSHFALSE" + str(self._current_label_arithmetic) + "\n"
        command += "D;" + jmp_type + "\n"
        command += "(PUSHTRUE" + str(self._current_label_arithmetic) + ")\n"
        command += "@SP\n"
        command += "D=M-1\n"
        command += "A=D-1\n"
        command += "M=-1\n"
        command += "@CONTINUE" + str(self._current_label_arithmetic) + "\n"
        command += "0;JMP\n"
        command += "(PUSHFALSE" + str(self._current_label_arithmetic) + ")\n"
        command += "@SP\n"
        command += "D=M-1\n"
        command += "A=D-1\n"
        command += "M=0\n"
        command += "(CONTINUE" + str(self._current_label_arithmetic) + ")\n"
        command += "@SP\n"
        command += "M=M-1\n"
        output = "@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "D=M-D\n" + "@PUSHFALSE" + str(
            self._current_label_arithmetic) + "\n" + "D;" + jmp_type + "\n" + "(PUSHTRUE" + str(
            self._current_label_arithmetic) + ")\n" + "@SP\n" + "D=M-1\n" + "A=D-1\n" + "M=-1\n" + "@CONTINUE" + str(
            self._current_label_arithmetic) + "\n" + "0;JMP\n" + "(PUSHFALSE" + str(
            self._current_label_arithmetic) + ")\n" + "@SP\n" + "D=M-1\n" + "A=D-1\n" + "M=0\n" + "(CONTINUE" + str(
            self._current_label_arithmetic) + ")\n" + "@SP\n" + "M=M-1\n"

        return command

    def gt_asm(self) -> None:
        self._output_stream.write(self.arithmetic_comparison_commands("JLE"))

    def lt_asm(self) -> None:
        self._output_stream.write(self.arithmetic_comparison_commands("JGE"))

    def eq_asm(self) -> None:
        self._output_stream.write(self.arithmetic_comparison_commands("JNE"))


    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        arithmetic_commands: dict[str, typing.Callable[[], None]] = {
            "add": self.add_asm, "sub": self.sub_asm, "and": self.and_asm,
            "or": self.or_asm, "neg": self.neg_asm, "not": self.not_asm,
            "shiftleft": self.shiftleft_asm, "shiftright": self.shiftright_asm,
            "gt": self.gt_asm, "lt": self.lt_asm, "eq": self.eq_asm}

        self._output_stream.write("// " + command + "\n")
        arithmetic_commands[command]()

    def push_command(self, segment: str, index: int) -> str:
        output = ""
        labels: dict[str, str] = {"local": "LCL", "this": "THIS",
                                  "that": "THAT", "argument": "ARG"}
        if segment in ["local", "this", "that", "argument"]:
            output += "@" + str(index) + "\n"
            output += "D=A\n"
            output += "@" + labels[segment] + "\n"
            output += "A=D+M\n"
        elif segment == "constant":
            output += "@" + str(index) + "\n"
        elif segment == "static":
            output += "@" + self._file_name + "." + str(index) + "\n"
        elif segment == "temp":
            output += "@" + str(index + 5) + "\n"
        else:  ## segment == pointer
            output += "@" + str(index + 3) + "\n"

        if segment == "constant":
            output += "D=A\n"
        else:
            output += "D=M\n"

        output += "@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        return output

    def pop_command(self, segment: str, index: int) -> str:
        ## set that R13 will contain the popped value
        output = "@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nM=D\n"

        ## set so that R14 register will contain the address of the pop value
        labels: dict[str, str] = {"local": "LCL", "this": "THIS",
                                  "that": "THAT", "argument": "ARG"}
        if segment in ["local", "this", "that", "argument"]:
            output += "@" + str(index) + "\n"
            output += "D=A\n"
            output += "@" + labels[segment] + "\n"
            output += "A=D+M\n"
        elif segment == "static":
            output += "@" + self._file_name + "." + str(index) + "\n"
        elif segment == "temp":
            output += "@" + str(index + 5) + "\n"
        else:  ## segment == pointer
            output += "@" + str(index + 3) + "\n"
        output += "D=A\n@R14\nM=D\n"

        ## R13 -> D
        output += "@R13\nD=M\n"

        ## R14 -> A
        output += "@R14\nA=M\n"

        ## place the popped value
        output += "M=D\n"

        return output

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        self._output_stream.write(
            "// " + command + " " + segment + " " + str(index) + "\n")

        if command == "C_PUSH":
            self._output_stream.write(self.push_command(segment, index))
        else:
            self._output_stream.write(self.pop_command(segment, index))

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_stream.write("// label " + label + "\n")
        command: str = "(" + self._file_name + "." + self._function_name + "$" + label + ")\n"
        self._output_stream.write(command)

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_stream.write("// goto " + label + "\n")
        final_command: str = ""
        final_command += "@" + self._file_name + "." + self._function_name + "$" + label + "\n"
        final_command += "0;JMP\n"
        self._output_stream.write(final_command)

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_stream.write("// if-goto " + label + "\n")
        final_command: str = ""
        final_command += "@SP\n"
        final_command += "AM=M-1\n"
        final_command += "D=M\n"
        final_command += "@" + self._file_name + "." + self._function_name + "$" + label + "\n"
        final_command += "D;JNE\n"
        self._output_stream.write(final_command)

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self._function_name = function_name
        self._cur_function_calls = 0
        self._output_stream.write(
            "// function " + function_name + " " + str(n_vars) + "\n")
        self._output_stream.write("(" + function_name + ")\n")
        for i in range(n_vars):
            self.write_push_pop("C_PUSH", "constant", 0)

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:

        self._output_stream.write(
            "// call " + function_name + " " + str(n_args) + "\n")
        # push return_address   // generates a label and pushes it to the stack
        self._cur_function_calls += 1
        return_address_label: str = self._file_name + "." + self._function_name + "$ret" + str(
            self._cur_function_calls)
        ret_push_command: str = "@" + return_address_label + "\n"
        ret_push_command += "D=A\n"
        ret_push_command += "@SP\n"
        ret_push_command += "A=M\n"
        ret_push_command += "M=D\n"
        ret_push_command += "@SP\n"
        ret_push_command += "M=M+1\n"

        self._output_stream.write(ret_push_command)
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        command: str = ""
        for seg in ["LCL", "ARG", "THIS", "THAT"]:
            command += "    @" + seg + '\n'
            command += ("    D=M\n"
                              "    @SP\n"
                              "    A=M\n"  # push SEG value into stack
                              "    M=D\n"
                              "    @SP\n"
                              "    M=M+1\n")  # sp++

        # ARG = SP-5-n_args     // repositions ARG
        command += "@" + str(5 + n_args) + "\n"
        command += "D=A\n"
        command += "@SP\n"
        command += "D=M-D\n"
        command += "@ARG\n"
        command += "M=D\n"
        # LCL = SP              // repositions LCL
        command += "@SP\n"
        command += "D=M\n"
        command += "@LCL\n"
        command += "M=D\n"
        # goto function_name    // transfers control to the callee
        command += "@" + function_name + "\n"
        command += "0;JMP\n"
        self._output_stream.write(command)
        # (return_address)      // injects the return address label into the code
        self.write_label("ret" + str(self._cur_function_calls))

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:

        self._output_stream.write(
            "// return from " + self._function_name + "\n")

        final_command: str = ""
        # frame = LCL                   // frame is a temporary variable stored in R13
        final_command += "@LCL\n"
        final_command += "D=M\n"
        final_command += "@R13\n"
        final_command += "M=D\n"
        # return_address = *(frame-5)   // puts the return address in a temp var in R14
        final_command += "@5\n"
        final_command += "A=D-A\n"
        final_command += "D=M\n"
        final_command += "@R14\n"
        final_command += "M=D\n"
        # *ARG = pop()                  // repositions the return value for the caller
        final_command += "@SP\n"
        final_command += "AM=M-1\n"
        final_command += "D=M\n"
        final_command += "@ARG\n"
        final_command += "A=M\n"
        final_command += "M=D\n"
        # SP = ARG + 1                  // repositions SP for the caller
        final_command += "@ARG\n"
        final_command += "D=M+1\n"
        final_command += "@SP\n"
        final_command += "M=D\n"
        # THAT = *(frame-1)             // restores THAT for the caller
        final_command += "@R13\n"
        final_command += "A=M-1\n"
        final_command += "D=M\n"
        final_command += "@THAT\n"
        final_command += "M=D\n"
        # THIS = *(frame-2)             // restores THIS for the caller
        final_command += "@2\n"
        final_command += "D=A\n"
        final_command += "@R13\n"
        final_command += "A=M\n"
        final_command += "A=A-D\n"
        final_command += "D=M\n"
        final_command += "@THIS\n"
        final_command += "M=D\n"
        # ARG = *(frame-3)              // restores ARG for the caller
        final_command += "@3\n"
        final_command += "D=A\n"
        final_command += "@R13\n"
        final_command += "A=M\n"
        final_command += "A=A-D\n"
        final_command += "D=M\n"
        final_command += "@ARG\n"
        final_command += "M=D\n"
        # LCL = *(frame-4)              // restores LCL for the caller
        final_command += "@4\n"
        final_command += "D=A\n"
        final_command += "@R13\n"
        final_command += "A=M\n"
        final_command += "A=A-D\n"
        final_command += "D=M\n"
        final_command += "@LCL\n"
        final_command += "M=D\n"
        # goto return_address           // go to the return address
        final_command += "@R14\n"
        final_command += "A=M\n"
        final_command += "0;JMP\n"

        self._output_stream.write(final_command)
