"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from typing import Callable

from SymbolTable import *
import JackTokenizer
from VMWriter import *

TAB: str = "  "
VAR_CATEGORY: int = 1
VAR_IDX: int = 2
DEF_OR_USE: int = 3
CALLER_TYPE: int = 1
IDENTIFIER: int = 0


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.

    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type)
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier


    Code convention - the caller advance the callee from the outside of the func
    No need for final advance to consume the final token in the callee,
    it will happen from the caller
    """

    def __init__(self, input_stream: JackTokenizer, filename: str,
                 output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.tok_stream: JackTokenizer = input_stream
        self.output: typing.TextIO = output_stream
        self.count_tabs = 0
        self.known_types = ["int", "char", "boolean", "void"]
        self.possible_statements = {
            "let": self.compile_let, "if": self.compile_if,
            "while": self.compile_while, "do": self.compile_do,
            "return": self.compile_return
        }
        self.symbol_t: SymbolTable = SymbolTable()
        self.vm_writer = VMWriter(self.output)
        self.filename: str = filename
        self.if_counter = 0
        self.while_counter = 0

    def advance_tok(self) -> str:
        self.tok_stream.set_prev_tok(self.tok_stream.get_cur_tok())
        self.tok_stream.advance()
        return self.tok_stream.get_cur_tok()

    def write_keyword(self, keyword: str) -> None:
        pass
        # self.output.write(
        #     self.count_tabs * TAB + "<keyword>" + keyword + "</keyword>\n")

    def write_symbol(self, symbol: str) -> None:
        pass
        # self.output.write(
        #     self.count_tabs * TAB + "<symbol>" + symbol + "</symbol>\n")

    def write_const_int(self, integer_constant: str) -> None:
        pass
        # self.output.write(
        #     self.count_tabs * TAB + "<integerConstant>" + integer_constant + "</integerConstant>\n")

    def write_const_string(self, string_constant: str) -> None:
        pass
        # self.output.write(
        #     self.count_tabs * TAB + "<stringConstant>" + self.tok_stream.string_val() + "</stringConstant>\n")

    def write_identifier(self, identifier: str, caller_type: str,
                         is_define: bool = True) -> typing.List[
        typing.Union[str, int]]:
        if caller_type in ["class", "subroutine"] and self.symbol_t.kind_of(
                identifier) is None:
            return [identifier, caller_type]
        else:
            var_category: str = self.symbol_t.kind_of(identifier).upper()
            var_idx: int = self.symbol_t.index_of(identifier)
            if is_define:
                defOrUse = "defined"
            else:
                defOrUse = "used"
            return [identifier, var_category, var_idx, defOrUse]

    def compile_class(self) -> None:
        """Compiles a complete class."""
        tok: str = self.advance_tok()  # Initial advance
        if tok != "class":
            raise ValueError("Expects 'class' token at the beginning of class")
        # write class name
        tok = self.advance_tok()  # consume ClassName
        class_name = tok
        self.write_identifier(class_name, "class")
        tok = self.advance_tok()  # consume symbol '{'
        if tok != '{':
            raise ValueError("class format is invalid")

        #  class variables declaration
        tok = self.advance_tok()
        while tok in ["static", "field"]:
            self.compile_class_var_dec()
            tok = self.advance_tok()  # consume ';' symbol

        while tok in ["constructor", "function", "method"]:
            self.compile_subroutine()
            tok = self.advance_tok()

        # consume symbol '}' - by the end of the while
        if tok != '}':
            raise ValueError("Expected '}' at end of class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        tok: str = self.tok_stream.get_cur_tok()
        ## static/field
        var_kind: str = tok
        tok = self.advance_tok()  # consume var kind
        ## var type - int|boolean|char
        var_type: str = tok
        if tok in self.known_types:
            self.write_keyword(tok)
        else:  ## |className
            self.write_identifier(tok, "class", True)
        tok = self.advance_tok()  # consume var type
        # var_name
        var_name: str = tok
        if var_type in self.known_types:
            self.symbol_t.define(var_name, var_type.upper(), var_kind)
        else:
            self.symbol_t.define(var_name, var_type, var_kind)
        self.write_identifier(tok, "class", True)
        # several params
        tok = self.advance_tok()  # consume var name
        while tok != ";":
            # var_name
            if tok == ',':  # only at the initial entry to the loop this cond will be true
                tok = self.advance_tok()
            var_name = tok
            # add var to symbol table
            if var_type in self.known_types:
                self.symbol_t.define(var_name, var_type.upper(), var_kind)
            else:
                self.symbol_t.define(var_name, var_type, var_kind)
            self.write_identifier(tok, "class", True)
            tok = self.advance_tok()  # consume symbol ','

        # tok = self.advance_tok()  # consume symbol ';'
        if tok != ';':
            raise ValueError("Expected ';' at end of var declaration")

    def handle_constructor(self) -> None:
        # consume keyword constructor
        self.advance_tok()
        ## returnType
        # consume return type - ClassName
        tok = self.advance_tok()
        ## subRoutineName
        subroutine_name = tok  # sub_name == "new"
        self.write_identifier(tok, "subroutine", True)
        self.advance_tok()
        # consume symbol '('
        self.advance_tok()
        self.compile_parameter_list()
        # consume symbol ')'
        self.advance_tok()

        ## subroutineBody
        # consume symbol '{'
        tok = self.advance_tok()
        while tok == "var":
            self.compile_var_dec()
            tok = self.advance_tok()
        self.vm_writer.write_function(self.filename + '.' + subroutine_name,
                                      self.symbol_t.var_count("VAR"))
        # pushing the number of object fields to allocate
        self.vm_writer.write_push("CONST", self.symbol_t.var_count("FIELD"))
        self.vm_writer.write_call("Memory.alloc", 1)
        # alloc return the address of the allocated object - then set THIS to it
        self.vm_writer.write_pop("POINTER", 0)

        self.compile_statements()  # all statements will be compiled except return
        # consume symbol '}'
        # self.compile_return()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        tok: str = self.tok_stream.get_cur_tok()
        method_flag: bool = False
        ## constructor/function/method
        if tok == "constructor":
            self.handle_constructor()
            return
        elif tok == "method":
            method_flag = True
        self.symbol_t.start_subroutine(method_flag)  # reset symbol table
        # consume keyword method or function
        tok = self.advance_tok()
        ## returnType
        # return_void: bool = False
        # if tok == "void":
        #    return_void = True
        if tok in self.known_types:
            self.write_keyword(tok)
        else:  ## |className
            self.write_identifier(tok, "subroutine", True)
        tok = self.advance_tok()
        ## subRoutineName
        subroutine_name = tok
        self.write_identifier(tok, "subroutine", True)
        self.advance_tok()
        # self.write_symbol("(")
        self.advance_tok()
        self.compile_parameter_list()
        # self.write_symbol(")")
        self.advance_tok()

        ## subroutineBody
        # consume symbol '{'
        tok = self.advance_tok()
        while tok == "var":
            self.compile_var_dec()
            tok = self.advance_tok()
        self.vm_writer.write_function(self.filename + '.' + subroutine_name,
                                      self.symbol_t.var_count("VAR"))
        if method_flag:
            # we need to set THIS to be the current object to access fields
            # methods receive as first argument the base address of cur object
            self.vm_writer.write_push("ARG", 0)
            self.vm_writer.write_pop("POINTER", 0)  # this = arg 0

        self.compile_statements()
        # consume symbol '}' from the caller

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()"
        """
        tok: str = self.tok_stream.get_cur_tok()
        first_time = True
        var_type: str = ""
        while tok != ")":
            if not first_time:
                # self.write_symbol(",")
                tok = self.advance_tok()
            else:
                first_time = False
            ## var type - int|boolean|char
            var_type = tok
            if tok in self.known_types:
                self.write_keyword(tok)
            else:  ## |className
                self.write_identifier(tok, "subroutine", True)
            tok = self.advance_tok()
            ## varName
            var_name: str = tok
            # add argument to symbol table:
            self.symbol_t.define(var_name, var_type, "ARG")
            self.write_identifier(tok, "subroutine", True)
            tok = self.advance_tok()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration. """
        tok: str = self.tok_stream.get_cur_tok()
        tok = self.advance_tok()  # consume keyword VAR
        first_time = True
        var_type: str = ""
        while tok != ";":
            if not first_time:
                tok = self.advance_tok()  # consume symbol ','
            else:
                first_time = False
                ## var type - int|boolean|char
                var_type = tok
                if var_type in self.known_types:
                    self.write_keyword(tok)
                else:  ## |className
                    self.write_identifier(tok, "subroutine", True)
                tok = self.advance_tok()  # consume type
            ## varName
            var_name: str = tok
            # add local vars into symbol table:
            self.symbol_t.define(var_name, var_type, "VAR")  # VAR==LOCAL
            self.write_identifier(tok, "subroutine", True)
            tok = self.advance_tok()  # consume symbol ';'

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}". Return statement is not handled by this func
        """
        tok: str = self.tok_stream.get_cur_tok()
        while tok in self.possible_statements:
            if tok == "do":
                self.possible_statements[tok]()
                self.vm_writer.write_pop("TEMP", 0)
                # after do function call to a void func - garbage value must be handled
            else:
                self.possible_statements[tok]()
            tok = self.tok_stream.get_cur_tok()
        # after loop the current token will be the next token - no need to advance

    def compile_do(self) -> None:
        """Compiles a do statement. In VM do command is translated into a jump
        to execute another function"""
        num_exp: int = 0
        self.advance_tok()  # consume keyword 'do'
        # subRoutineCall
        tok_type: str = self.tok_stream.token_type()
        next_tok = self.advance_tok()
        tok = self.tok_stream.get_prev_tok()
        if next_tok == '(':
            # subroutine(expression_list)
            subroutine_name = tok
            self.write_identifier(tok, "subroutine", False)
            # push THIS as first arg (argument 0) BEFORE compiling the real args
            self.vm_writer.write_push("POINTER", 0)
            self.advance_tok()  # consume symbol '('
            num_exp = self.compile_expression_list()
            # no need to advance token
            self.advance_tok()  # consume symbol ')'
            self.vm_writer.write_call(f"{self.filename}.{subroutine_name}",
                                      num_exp + 1)  # also pushed this


        elif next_tok == '.':
            OS_CLASSES = ["Array", "Memory", "Math", "Screen", "Keyboard",
                          "String", "Sys", "Output"]
            # (className | varName).Subroutine(Expression_list)
            class_or_var = tok
            self.write_identifier(tok, "subroutine", False)
            var_type: str = self.symbol_t.type_of(class_or_var)
            var_kind: str = self.symbol_t.kind_of(class_or_var)
            if var_kind is not None and (class_or_var not in OS_CLASSES):
                # this is an Object variable and not a className
                segment: str = self.symbol_t.kind_of(class_or_var)
                idx: int = self.symbol_t.index_of(class_or_var)
                self.vm_writer.write_push(segment, idx)
                num_exp += 1  # pushing this variable
                if var_type is None:
                    raise ValueError(
                        f"Type info missing for variable '{class_or_var}'")
                class_or_var = var_type

            # consume symbol '.'
            tok = self.advance_tok()  # tok is now subroutine name
            func_name = tok
            self.write_identifier(tok, "subroutine", False)
            self.advance_tok()
            self.advance_tok()  # consume symbol '('
            num_exp += self.compile_expression_list()
            # no need to advance token
            self.advance_tok()  # consume symbol ')'
            target_name: str = class_or_var + '.' + func_name
            self.vm_writer.write_call(target_name, num_exp)
        self.advance_tok()  # consume symbol ';'

    def compile_let(self) -> None:
        """Compiles a let statement."""
        tok = self.advance_tok()  # consume keyword 'let'
        # varName
        var_name: str = tok
        parm_lst = self.write_identifier(tok, "subroutine", False)
        tok = self.advance_tok()
        if tok == "[":  # array assignment - varName[exp1] = exp2
            # push array base address
            segment: str = parm_lst[VAR_CATEGORY]
            idx: int = parm_lst[VAR_IDX]
            self.vm_writer.write_push(segment, idx)

            self.advance_tok()  # consume symbol '['
            self.compile_expression()  # expression result is pushed to stack
            # no need to advance token after expression
            if self.tok_stream.get_cur_tok() != ']':
                raise ValueError("Expected ']' after array index expression")
            self.advance_tok()  # consume symbol ']'
            # compute memory address = base + index(exp1)
            self.vm_writer.write_arithmetic("ADD")

            self.advance_tok()  # consume '='
            self.compile_expression()  # no need to advance, value is pushed to stack
            # save exp2 in temp
            self.vm_writer.write_pop("TEMP", 0)  # temp0 = value
            # set THAT to point to memory address
            self.vm_writer.write_pop("POINTER", 1)  # pointer 1 <- address
            # restore value and store into THAT 0
            self.vm_writer.write_push("TEMP", 0)
            self.vm_writer.write_pop("THAT", 0)

            self.advance_tok()  # consume symbol ';'

        else:
            self.advance_tok()  # consume symbol '='
            self.compile_expression()  # the result is now pushed into the stack
            segment: str = parm_lst[VAR_CATEGORY]
            idx: int = parm_lst[VAR_IDX]
            self.vm_writer.write_pop(segment, idx)
            # the expression result in now popped into the variable
            # no need to advance token after expression
            self.advance_tok()  # consume symbol ';'

    def compile_while(self) -> None:
        """Compiles a while statement."""
        idx: int = self.while_counter
        self.while_counter += 1
        tok: str = self.tok_stream.get_cur_tok()
        # consume keyword 'while'
        if tok != 'while':
            raise ValueError("Expected 'while'")
        # consume symbol '('
        tok = self.advance_tok()
        if tok != '(':
            raise ValueError("Expected '(' after 'while'")
        self.vm_writer.write_label(f"WHILE_EXP{idx}")
        self.advance_tok()

        # compile while condition, result pushed to stack
        self.compile_expression()
        # no need to advance token after expression

        # consume symbol ')'
        tok = self.tok_stream.get_cur_tok()
        if tok != ')':
            raise ValueError("Expected ')' after while-condition")
        self.advance_tok()

        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(f"WHILE_END{idx}")

        # consume symbol '{'
        tok = self.tok_stream.get_cur_tok()
        if tok != '{':
            raise ValueError("Expected '{' to open while-body")
        self.advance_tok()

        self.compile_statements()
        # no need to advance token after statements
        # consume symbol '}'
        tok = self.tok_stream.get_cur_tok()
        if tok != '}':
            raise ValueError("Expected '}' to close while-body")
        self.advance_tok()

        self.vm_writer.write_goto(f"WHILE_EXP{idx}")

        # exit loop:
        self.vm_writer.write_label(f"WHILE_END{idx}")

    def compile_return(self) -> None:
        """Compiles a return statement. In VM the returned value must be
        pushed before the return statement"""
        tok: str = self.tok_stream.get_cur_tok()
        # consume keyword 'return'
        tok = self.advance_tok()
        if tok == ";":  # handle void return
            self.vm_writer.write_push("CONST", 0)
            self.vm_writer.write_return()
            self.advance_tok()  # consume ';'
            return

        self.compile_expression()
        # no need to advance token after expression
        if self.tok_stream.get_cur_tok() != ';':
            raise ValueError("Expected ';' after return expression")
        self.vm_writer.write_return()
        self.advance_tok()  # consume ';'

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        idx: int = self.if_counter
        self.if_counter += 1
        # consume keyword 'if'
        tok: str = self.tok_stream.get_cur_tok()
        if tok != 'if':
            raise ValueError("Expected 'if'")

        tok = self.advance_tok()  # consume symbol '('
        if tok != '(':
            raise ValueError("Expected '(' after 'if'")

        self.advance_tok()  # current tok is now the first tok of expression
        self.compile_expression()  # expression result is pushed to stack
        # no need to advance token after expression

        tok = self.tok_stream.get_cur_tok()
        if tok != ')':
            raise ValueError("Expected ')' after if-condition")

        self.advance_tok()  # consume symbol ')'

        # branching commands to check if condition is True/False
        self.vm_writer.write_if(f"IF_TRUE{idx}")
        self.vm_writer.write_goto(f"IF_FALSE{idx}")

        self.vm_writer.write_label(f"IF_TRUE{idx}")
        # consume symbol '{' for True Block
        tok = self.tok_stream.get_cur_tok()
        if tok != '{':
            raise ValueError("Expected '{' to open if-block")
        self.advance_tok()

        self.compile_statements()
        # no need to advance token after statements

        # consume symbol '}' for True Block
        tok = self.tok_stream.get_cur_tok()
        if tok != '}':
            raise ValueError("Expected '}' to close if-block")
        self.advance_tok()
        self.vm_writer.write_goto(f"END_IF{idx}")  # skip else Block

        self.vm_writer.write_label(f"IF_FALSE{idx}")
        if self.tok_stream.get_cur_tok() == "else":
            # consume keyword 'else'
            self.advance_tok()
            # consume symbol '{'
            tok = self.tok_stream.get_cur_tok()
            if tok != '{':
                raise ValueError("Expected '{' to open else-block")
            self.advance_tok()

            self.compile_statements()
            # no need to advance token after statements
            tok = self.tok_stream.get_cur_tok()
            if tok != '}':
                raise ValueError("Expected '}' to close else-block")
            self.advance_tok()  # consume symbol '}'

        self.vm_writer.write_label("END_IF" + str(idx))

    def compile_expression(self) -> None:
        """Compiles an expression. At the end of compilation the expression
        value is pushed into the stack"""
        OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '&lt;', '&gt;',
               '&amp;']
        UNARY_OPS = ['~', '-']
        ops_translator: typing.Dict[str, str] = {
            '+': "ADD", '-': "SUB", '*': "MULT",
            '/': "DIV", '&': "AND", '|': "OR",
            '<': "LT", '>': "GT", '=': "EQ", '&lt;': "LT", '&gt;': "GT",
            '&amp;': "AND"}
        tok: str = self.tok_stream.get_cur_tok()
        self.compile_term()
        # no need to advance token after term
        tok = self.tok_stream.get_cur_tok()
        while tok in OPS:
            op: str = tok
            # consume operator
            self.advance_tok()
            self.compile_term()
            self.vm_writer.write_arithmetic(ops_translator[op])
            tok = self.tok_stream.get_cur_tok()

    # the current token at the end of the method is the next token

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        UNARY_OPS = ['~', '-', '^', '#']
        KEYWORD_CONST = ['true', 'false', 'this', 'null']

        tok: str = self.tok_stream.get_cur_tok()
        tok_type: str = self.tok_stream.token_type()

        # handle integer constant:
        if tok_type == "INT_CONST":
            # consume constant int
            self.vm_writer.write_push("CONST", int(tok))
            self.advance_tok()
            return

        # handle constant string:
        elif tok_type == "STRING_CONST":
            s: str = tok
            length = len(s)
            # creating a new String object using the OS library
            self.vm_writer.write_push("CONST", length)
            self.vm_writer.write_call("String.new", 1)
            # appending each char in string to object
            for ch in s:
                ascii_val: int = ord(ch)
                self.vm_writer.write_push("CONST", ascii_val)
                self.vm_writer.write_call("String.appendChar", 2)

            self.advance_tok()  # consume string
            return

        # handle keyword constants:
        if (tok_type == "KEYWORD") and (tok in KEYWORD_CONST):
            if tok == "true":
                self.vm_writer.write_push("CONST", 1)
                self.vm_writer.write_arithmetic("NEG")  # true == -1
            elif tok == "this":
                # pushing the base address THIS object
                self.vm_writer.write_push("POINTER", 0)
            else:  # false / null == 0
                self.vm_writer.write_push("CONST", 0)
            self.advance_tok()
            return

        # handle (expression) and unary-op temp
        elif tok_type == "SYMBOL":
            if tok == '(':
                # (expression) case
                self.advance_tok()  # consume symbol '('
                self.compile_expression()
                # consume symbol ')'
                if self.tok_stream.get_cur_tok() != ')':
                    raise ValueError(
                        "Expected ')' after parenthesized expression")
                self.advance_tok()  # consume ')'
                return
            elif tok in UNARY_OPS:  # unary_op temp
                unary_op: str = tok
                self.advance_tok()  # consume unary operator
                self.compile_term()
                # recursive call to process the term following the unary op
                unary_op_trans = {'~': "NOT", '-': "NEG"}
                self.vm_writer.write_arithmetic(unary_op_trans[unary_op])
                return
        else:
            # cases: var | var[expr] | sub(exprList) | (class|var).sub(exprList)
            #  we need to differentiate between possibilities:
            self.advance_tok()
            next_tok: str = self.tok_stream.get_cur_tok()
            tok = self.tok_stream.get_prev_tok()
            if next_tok == '[':  # VarName[expression]
                parm_lst = self.write_identifier(tok, "subroutine", False)
                segment: str = parm_lst[VAR_CATEGORY]
                idx: int = parm_lst[VAR_IDX]
                self.vm_writer.write_push(segment, idx)  # array base address

                self.advance_tok()  # consume symbol '['
                self.compile_expression()
                if self.tok_stream.get_cur_tok() != ']':
                    raise ValueError(
                        "Expected ']' after array index expression")
                self.advance_tok()  # consume symbol ']'

                # insert (base + index) to THAT, then push THAT 0
                self.vm_writer.write_arithmetic("ADD")
                self.vm_writer.write_pop("POINTER", 1)
                self.vm_writer.write_push("THAT", 0)
                return

            elif next_tok == '(':  # subroutine(expression_list)
                sub_name: str = tok
                # push current object base address
                self.vm_writer.write_push("POINTER", 0)
                self.write_identifier(tok, "subroutine", False)

                self.advance_tok()  # consume symbol '('
                n_args: int = self.compile_expression_list()
                # no need to advance token
                if self.tok_stream.get_cur_tok() != ')':
                    raise ValueError("Expected ')' after expression list")
                self.advance_tok()  # consume symbol ')'

                self.vm_writer.write_call(self.filename + '.' + sub_name,
                                          n_args + 1)
                # n_args + 1 is pushed because we added THIS current object
                return

            elif next_tok == '.':
                # (className | varName).Subroutine(Expression_list)
                OS_CLASSES = ["Array", "Memory", "Math", "Screen", "Keyboard",
                              "String", "Sys", "Output"]
                var_or_class: str = tok
                n_args: int = 0
                self.write_identifier(tok, "subroutine", False)
                is_object: bool = self.symbol_t.kind_of(
                    var_or_class) is not None
                if is_object and (var_or_class not in OS_CLASSES):
                    # VarName is an object and not a ClassName
                    # Pushing the object itself (base address)
                    segment: str = self.symbol_t.kind_of(var_or_class)
                    idx: int = self.symbol_t.index_of(var_or_class)
                    self.vm_writer.write_push(segment, idx)
                    n_args += 1
                    type_name: str = self.symbol_t.type_of(var_or_class)
                    var_or_class = type_name

                self.advance_tok()  # consume symbol '.'
                sub_name = self.tok_stream.get_cur_tok()
                self.advance_tok()  # consume subroutine name
                self.write_identifier(sub_name, "subroutine", False)

                if self.tok_stream.get_cur_tok() != '(':
                    raise ValueError("Expected '(' after subroutine name")
                self.advance_tok()  # consume '('

                n_args += self.compile_expression_list()
                if self.tok_stream.get_cur_tok() != ')':
                    raise ValueError("Expected ')' after expression list")
                self.advance_tok()  # consume ')
                func_name = f"{var_or_class}.{sub_name}"
                self.vm_writer.write_call(func_name, n_args)
                # no need to advance token
                return

            else:
                # if none of the above was executed then the current token is
                # only VarName and the following token is unrelated
                parm_lst = self.write_identifier(tok, "subroutine", False)
                segment: str = parm_lst[VAR_CATEGORY]
                idx: int = parm_lst[VAR_IDX]
                self.vm_writer.write_push(segment, idx)
                # no need to advance, already advanced because of next token
                return

        # By the end of this function - the current token is ')'
        raise ValueError(f"Unexpected term start token: {tok}")

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions.
        This func compile the expression list and does not compile the '(', ')'
        parentheses. Func return the number of expressions in exp list"""
        tok: str = self.tok_stream.get_cur_tok()
        if tok == ')':
            # expression list is an empty list ()
            return 0  # there are 0 args in the exp list
        counter: int = 0
        while tok != ')':
            self.compile_expression()
            counter += 1
            # no need to advance token after expression
            tok = self.tok_stream.get_cur_tok()
            if tok == ',':
                self.advance_tok()  # consume symbol ','
        return counter
