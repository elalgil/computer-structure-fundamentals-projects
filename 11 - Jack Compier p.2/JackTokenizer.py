"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import re
import typing
from typing import Pattern, AnyStr


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
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

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    KEYWORDS = {'class', 'constructor', 'function', 'method', 'field',
                'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}

    SYMBOLS = set('{}()[].,;+-*/&|<>=~^#')

    # Regular expressions for token matching at the start of a line
    _RE_STRING: Pattern[AnyStr] = re.compile(r'^"[^"\n]*"')
    _RE_INT: Pattern[AnyStr] = re.compile(r'^\d+')
    _RE_IDENT: Pattern[AnyStr] = re.compile(r'^[A-Za-z_]\w*')
    _RE_SYMBOL: Pattern[AnyStr] = re.compile(r'^[{}()\[\].,;+\-*/&|<>=~^#]')

    # The order matters!!!
    _RE_EXPRESSIONS: list[Pattern[AnyStr]] = [_RE_STRING, _RE_SYMBOL, _RE_INT,
                                              _RE_IDENT]

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.
        Args:
            input_stream (typing.TextIO): input stream.
        """
        raw_lines = input_stream.read().splitlines()
        self.cur_line_idx: int = 0
        self.cur_line: typing.Union[str, None] = None
        self.in_block_comment = False
        cleaned = []
        for line in raw_lines:
            cl = self.clean_line(line)
            if cl != "":
                cleaned.append(cl)
        self.input_lines = cleaned
        self.num_lines: int = len(self.input_lines)
        self.cur_token = None
        self.prev: typing.Union[str, None] = None

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        if self.cur_line and self.cur_line.strip():
            return True
            # check remaining lines for any non-empty (after cleaning)
        while self.cur_line_idx < self.num_lines:
            if self.input_lines[self.cur_line_idx].strip():
                return True
            self.cur_line_idx += 1
        return False

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        if not self.has_more_tokens():
            raise ValueError("there are no more tokens")

        while not (self.cur_line and self.cur_line.strip()):
            if self.cur_line_idx >= self.num_lines:
                raise ValueError("there are no more tokens")
            self.cur_line = self.input_lines[self.cur_line_idx]
            self.cur_line_idx += 1

        s = self.cur_line.lstrip()
        startswith_white_space = len(self.cur_line) - len(s)
        if startswith_white_space:
            # remove leading whitespace
            self.cur_line = s

        for pattern in JackTokenizer._RE_EXPRESSIONS:
            match = pattern.match(s)
            if match:
                token = match.group(0)
                self.cur_token = token
                self.cur_line = s[len(token):]
                return

        # the token starts with invalid characters
        raise ValueError(f"Unexpected token start: {repr(s[:20])}")

    def clean_line(self, line: str) -> str:
        """Func clean the current line in the input file and remove all spaces
        and comments. Func may return and empty string if the entire line is
        comments"""
        res_chars = []
        i = 0
        length: int = len(line)
        # in_string = False
        while i < length:
            # If currently inside a block comment, look for end
            if self.in_block_comment:
                end = line.find('*/', i)
                if end == -1:
                    # remove the rest of line is inside block comment
                    return ''.join(res_chars).rstrip()
                else:
                    # skip block comment content until after */
                    i = end + 2
                    self.in_block_comment = False
                    continue
            chars = line[i]
            # Handle quote toggling """..."""
            # TODO and statement is redundant
            if chars == '"' and not self.in_block_comment:
                # start or end of string literal
                res_chars.append(chars)
                i += 1
                # copy until closing quote or end-of-line
                while i < length:
                    if line[i] == '"':
                        res_chars.append('"')
                        i += 1
                        break
                    # include characters inside string (including comment markers)
                    res_chars.append(line[i])
                    i += 1
                continue
            # Check for start of line comment //
            if chars == '/' and i + 1 < length and line[i + 1] == '/':
                # rest of line is a comment -> stop processing
                break
            # Check for start of block comment /*
            if chars == '/' and i + 1 < length and line[i + 1] == '*':
                self.in_block_comment = True
                i += 2
                # Now continue the while loop which will handle the in_block_comment state
                continue
            # keep all the normal character which are not in comment
            res_chars.append(chars)
            i += 1
        return ''.join(res_chars).rstrip()

    def check_const_int(self, line: str) -> bool:
        """func returns true is the token is an INT CONSTANT and false
         otherwise"""
        first_word: str = line.split()[0]
        # TODO removed the loop - redundant
        return first_word.isdigit()
        # for i in range(len(first_word)):
        #     if not (first_word[i].isdigit()):
        #         return False
        # return True

    def check_const_str(self, line: str) -> bool:
        """func returns true is the token is an STRING CONSTANT and false
         otherwise"""
        token: str = line.split()[0]
        if token.startswith('"') and token.endswith('"'):
            # why try except? what's the purpose of the condition here
            try:
                separated: str = token.split('"')[1]
                if '"' not in separated and '\n' not in separated:
                    return True
                else:
                    return False
            except:
                return False
        return False

    def check_identifier(self, line: str) -> bool:
        """func returns true is the token is an identifier and false
         otherwise"""
        token: str = line.split()[0]
        if token[0].isdigit():
            # identifier can't start with a digit
            return False
        for i in range(len(token)):
            if not (token[i].isdigit() or token[i].isalpha() or token[
                i] == '_'):
                # token has characters which are not number/ A-Z, a-z, _
                return False
        return True

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        Keywords: typing.List[str] = ['class', 'constructor', 'function',
                                      'method', 'field', 'static', 'var',
                                      'int', 'char', 'boolean', 'void', 'true',
                                      'false', 'null', 'this', 'let', 'do',
                                      'if', 'else', 'while', 'return']
        Symbols: typing.List[str] = ['{', '}', '(', ')', '[', ']', '.', ',',
                                     ';', '+', '-', '*', '/', '&', '|', '<',
                                     '>', '=', '~', '^', '#']
        tok: str = self.cur_token
        if tok in self.KEYWORDS:
            return "KEYWORD"
        if len(tok) == 1 and tok in self.SYMBOLS:
            return "SYMBOL"
        if self._RE_INT.fullmatch(tok):
            return "INT_CONST"
        if self._RE_STRING.fullmatch(tok):
            return "STRING_CONST"
        if self._RE_IDENT.fullmatch(tok):
            return "IDENTIFIER"
        raise ValueError(
            "The current token does not match any category of language grammar")

    def keyword(self) -> str:
        """Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.cur_token.upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        special_symbols: typing.Dict[str, str] = {"<": "&lt;", ">": "&gt;",
                                                  "&": "&amp;"}
        if self.cur_token in special_symbols:
            return special_symbols[self.cur_token]
        return self.cur_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self.cur_token

    def int_val(self) -> str:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return self.cur_token

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        return self.cur_token[1:-1]

    def get_cur_tok(self):
        """func return current token"""
        special_symbols: typing.Dict[str, str] = {"<": "&lt;", ">": "&gt;",
                                                  "&": "&amp;"}
        if self.cur_token in special_symbols:
            return special_symbols[self.cur_token]
        return self.cur_token

    def get_prev_tok(self):
        """func return prev token"""
        special_symbols: typing.Dict[str, str] = {"<": "&lt;", ">": "&gt;",
                                                  "&": "&amp;"}
        if self.prev in special_symbols:
            return special_symbols[self.prev]
        return self.prev

    def set_prev_tok(self, tok: str) -> None:
        """Func set the prev token to the received token string"""
        self.prev = tok
