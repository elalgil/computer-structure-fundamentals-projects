"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from typing import Callable

import JackTokenizer

TAB: str = "  "


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

    """

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
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

    def advance_tok(self) -> str:
        self.tok_stream.set_prev_tok(self.tok_stream.get_cur_tok())
        self.tok_stream.advance()
        return self.tok_stream.get_cur_tok()

    def write_keyword(self, keyword: str) -> None:
        self.output.write(
            self.count_tabs * TAB + "<keyword>" + keyword + "</keyword>\n")

    def write_symbol(self, symbol: str) -> None:
        self.output.write(
            self.count_tabs * TAB + "<symbol>" + symbol + "</symbol>\n")

    def write_const_int(self, integer_constant: str) -> None:
        self.output.write(
            self.count_tabs * TAB + "<integerConstant>" + integer_constant + "</integerConstant>\n")

    def write_const_string(self, string_constant: str) -> None:
        self.output.write(
            self.count_tabs * TAB + "<stringConstant>" + self.tok_stream.string_val() + "</stringConstant>\n")

    def write_identifier(self, identifier: str) -> None:
        self.output.write(
            self.count_tabs * TAB + "<identifier>" + identifier + "</identifier>\n")

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.advance_tok()
        tok: str = self.tok_stream.get_cur_tok()
        if tok == "class":
            self.output.write("<class>\n")
            self.count_tabs += 1
            self.write_keyword("class")
            # class name
            tok = self.advance_tok()
            self.write_identifier(tok)
            tok = self.advance_tok()
            if tok != '{':
                raise ValueError("class format is invalid")

            self.write_symbol("{")
            tok = self.advance_tok()
            while tok in ["static", "field"]:
                self.compile_class_var_dec()
                tok = self.advance_tok()
            while tok in ["constructor", "function", "method"]:
                self.compile_subroutine()
                tok = self.advance_tok()
            self.write_symbol("}")
            self.count_tabs -= 1
            self.output.write("</class>\n")
        else:
            raise ValueError("current token is not a class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<classVarDec>\n")
        self.count_tabs += 1
        ## static/field
        self.write_keyword(tok)
        tok = self.advance_tok()
        ## var type - int|boolean|char
        if tok in self.known_types:
            self.write_keyword(tok)
        else:  ## |className
            self.write_identifier(tok)
        tok = self.advance_tok()
        # var_name
        self.write_identifier(tok)
        # several params
        tok = self.advance_tok()
        while tok != ";":
            self.write_symbol(",")
            tok = self.advance_tok()
            # var_name
            self.write_identifier(tok)
            tok = self.advance_tok()
        self.write_symbol(";")
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<subroutineDec>\n")
        self.count_tabs += 1
        ## constructor/function/method
        self.write_keyword(tok)
        tok = self.advance_tok()
        ## returnType
        if tok in self.known_types:
            self.write_keyword(tok)
        else:  ## |className
            self.write_identifier(tok)
        tok = self.advance_tok()
        ## subRoutineName
        self.write_identifier(tok)
        tok = self.advance_tok()
        self.write_symbol("(")
        tok = self.advance_tok()
        self.compile_parameter_list()
        self.write_symbol(")")
        tok = self.advance_tok()

        ## subroutineBody
        self.output.write(self.count_tabs * TAB + "<subroutineBody>\n")
        self.count_tabs += 1
        self.write_symbol("{")
        tok = self.advance_tok()
        while tok == "var":
            self.compile_var_dec()
            tok = self.advance_tok()
        self.compile_statements()
        self.write_symbol("}")
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</subroutineBody>\n")
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<parameterList>\n")
        self.count_tabs += 1
        first_time = True
        while tok != ")":
            if not first_time:
                self.write_symbol(",")
                tok = self.advance_tok()
            else:
                first_time = False
            ## var type - int|boolean|char
            if tok in self.known_types:
                self.write_keyword(tok)
            else:  ## |className
                self.write_identifier(tok)
            tok = self.advance_tok()
            ## varName
            self.write_identifier(tok)
            tok = self.advance_tok()

        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<varDec>\n")
        self.count_tabs += 1
        self.write_keyword("var")
        tok = self.advance_tok()
        first_time = True
        while tok != ";":
            if not first_time:
                self.write_symbol(",")
                tok = self.advance_tok()
            else:
                first_time = False
                ## var type - int|boolean|char
                if tok in self.known_types:
                    self.write_keyword(tok)
                else:  ## |className
                    self.write_identifier(tok)
                tok = self.advance_tok()
            ## varName
            self.write_identifier(tok)
            tok = self.advance_tok()

        self.write_symbol(";")
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<statements>\n")
        self.count_tabs += 1
        while tok in self.possible_statements:
            self.possible_statements[tok]()
            tok = self.tok_stream.get_cur_tok()
        # after loop the current token will be the next token - no need to advance
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<doStatement>\n")
        self.count_tabs += 1
        self.write_keyword("do")
        self.advance_tok()
        # subRoutineCall
        tok_type: str = self.tok_stream.token_type()
        next_tok = self.advance_tok()
        tok = self.tok_stream.get_prev_tok()
        if (tok_type == "IDENTIFIER") and (next_tok == '('):
            # subroutine(expression_list)
            self.write_identifier(tok)
            self.write_symbol(next_tok)  # write '('
            self.advance_tok()
            self.compile_expression_list()
            # no need to advance token
            self.write_symbol(self.tok_stream.get_cur_tok())  # write ')'
            self.advance_tok()
        elif (tok_type == "IDENTIFIER") and (next_tok == '.'):
            # (className | varName).Subroutine(Expression_list)
            self.write_identifier(tok)
            self.write_symbol(next_tok)  # write '.'
            tok = self.advance_tok()  # tok is now subroutine name
            self.write_identifier(tok)
            self.advance_tok()
            self.write_symbol(self.tok_stream.get_cur_tok())  # write '('
            self.advance_tok()
            self.compile_expression_list()
            # no need to advance token
            self.write_symbol(self.tok_stream.get_cur_tok())  # write ')'
            self.advance_tok()

        self.write_symbol(";")
        self.advance_tok()
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<letStatement>\n")
        self.count_tabs += 1
        self.write_keyword("let")
        tok = self.advance_tok()
        # varName
        self.write_identifier(tok)
        tok = self.advance_tok()
        if tok == "[":
            self.write_symbol("[")
            tok = self.advance_tok()
            self.compile_expression()
            # no need to advance token after expression
            self.write_symbol("]")
            self.advance_tok()
        self.write_symbol("=")
        self.advance_tok()
        self.compile_expression()
        # no need to advance token after expression
        self.write_symbol(";")
        self.advance_tok()
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<whileStatement>\n")
        self.count_tabs += 1
        self.write_keyword("while")
        tok = self.advance_tok()
        self.write_symbol("(")
        tok = self.advance_tok()
        self.compile_expression()
        # no need to advance token after expression
        self.write_symbol(")")
        self.advance_tok()
        self.write_symbol("{")
        self.advance_tok()
        self.compile_statements()
        # no need to advance token after statements
        self.write_symbol("}")
        self.advance_tok()
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<returnStatement>\n")
        self.count_tabs += 1
        self.write_keyword("return")
        tok = self.advance_tok()
        if tok != ";":
            self.compile_expression()
        # no need to advance token after expression
        tok = self.tok_stream.get_cur_tok()
        self.write_symbol(";")
        self.advance_tok()
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<ifStatement>\n")
        self.count_tabs += 1
        self.write_keyword("if")
        self.advance_tok()
        self.write_symbol("(")
        self.advance_tok()
        self.compile_expression()
        # no need to advance token after expression
        self.write_symbol(")")
        self.advance_tok()
        self.write_symbol("{")
        self.advance_tok()
        self.compile_statements()
        # no need to advance token after statements
        self.write_symbol("}")
        self.advance_tok()
        if self.tok_stream.get_cur_tok() == "else":
            self.write_keyword("else")
            self.advance_tok()
            self.write_symbol("{")
            self.advance_tok()
            self.compile_statements()
            # no need to advance token after statements
            self.write_symbol("}")
            self.advance_tok()
        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '&lt;', '&gt;',
               '&amp;']
        UNARY_OPS = ['~', '-']
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<expression>\n")
        self.count_tabs += 1
        self.compile_term()
        # no need to advance token after term
        tok = self.tok_stream.get_cur_tok()
        while tok in OPS:
            self.write_symbol(tok)
            self.advance_tok()
            self.compile_term()
            tok = self.tok_stream.get_cur_tok()

        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</expression>\n")

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
        OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '&lt;', '&gt;',
               '&amp;']
        UNARY_OPS = ['~', '-', '^', '#']
        KEYWORD_CONST = ['true', 'false', 'this', 'null']
        self.output.write(self.count_tabs * TAB + "<term>\n")
        self.count_tabs += 1

        tok: str = self.tok_stream.get_cur_tok()
        tok_type: str = self.tok_stream.token_type()
        if tok_type == "INT_CONST":
            self.write_const_int(tok)
            self.advance_tok()
        elif tok_type == "STRING_CONST":
            self.write_const_string(tok)
            self.advance_tok()
        elif (tok_type == "KEYWORD") and (tok in KEYWORD_CONST):
            self.write_keyword(tok)
            self.advance_tok()
        elif tok_type == "SYMBOL":
            if tok == '(':
                # (expression)
                self.write_symbol(self.tok_stream.get_cur_tok())  # write '('
                self.advance_tok()
                self.compile_expression()
                self.write_symbol(self.tok_stream.get_cur_tok())  # write ')'
                self.advance_tok()
            elif tok in UNARY_OPS:
                # unary_op temp
                self.write_symbol(tok)
                self.advance_tok()
                self.compile_term()
                # recursive call to process the term following the unary op
        else:
            #  we need to differentiate between possibilities:
            self.advance_tok()
            next_tok: str = self.tok_stream.get_cur_tok()
            tok = self.tok_stream.get_prev_tok()
            if (tok_type == "IDENTIFIER") and (next_tok == '['):
                #  VarName[expression]
                self.write_identifier(tok)
                self.write_symbol(next_tok)  # write '['
                self.advance_tok()
                self.compile_expression()
                self.write_symbol(self.tok_stream.get_cur_tok())  # write ']'
                self.advance_tok()
            elif (tok_type == "IDENTIFIER") and (next_tok == '('):
                # subroutine(expression_list)
                self.write_identifier(tok)
                self.write_symbol(next_tok)  # write '('
                self.advance_tok()
                self.compile_expression_list()
                # no need to advance token
                self.write_symbol(self.tok_stream.get_cur_tok())  # write ')'
                self.advance_tok()
            elif (tok_type == "IDENTIFIER") and (next_tok == '.'):
                # (className | varName).Subroutine(Expression_list)
                self.write_identifier(tok)
                self.write_symbol(next_tok)  # write '.'
                tok = self.advance_tok()  # tok is now subroutine name
                self.write_identifier(tok)
                self.advance_tok()
                self.write_symbol(self.tok_stream.get_cur_tok())  # write '('
                self.advance_tok()
                self.compile_expression_list()
                # no need to advance token
                self.write_symbol(self.tok_stream.get_cur_tok())  # write ')'
                self.advance_tok()
            else:
                # if none of the above was executed then the current token is
                # only VarName and the following token is unrelated
                self.write_identifier(tok)
                # no need to advance, already advanced because of next token

        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</term>\n")

    # By the end of this function - the current token is ')'
    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions.
        This func compile the expression list and does not compile the '(', ')'
        parentheses"""
        tok: str = self.tok_stream.get_cur_tok()
        self.output.write(self.count_tabs * TAB + "<expressionList>\n")
        self.count_tabs += 1
        if tok == ')':
            # expression list is an empty list ()
            self.count_tabs -= 1
            self.output.write(self.count_tabs * TAB + "</expressionList>\n")
            return

        while tok != ')':
            self.compile_expression()
            # no need to advance token after expression
            tok = self.tok_stream.get_cur_tok()
            if tok == ',':
                self.write_symbol(tok)  # write ',' between expressions
                self.advance_tok()

        self.count_tabs -= 1
        self.output.write(self.count_tabs * TAB + "</expressionList>\n")
