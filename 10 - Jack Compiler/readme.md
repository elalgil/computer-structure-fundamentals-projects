# Project 10: Jack Compiler I - Syntax Analysis

In this project, I built the **Syntax Analyzer** (Parser) for the Jack programming language. This is the first stage of the full compiler (Front-End), responsible for reading source code and understanding its grammatical structure without yet generating executable code.

## Overview
The goal of this project was to transform raw text (Jack source code) into a structured format (XML) that represents the program's logic hierarchy. This process verifies that the code conforms to the Jack language grammar.

**The Pipeline:**
`Source Code (.jack)` -> **`Tokenizer`** -> **`Compilation Engine`** -> `Parse Tree (.xml)`

## Key Components

### 1. The Tokenizer (`JackTokenizer`)
The lexical analysis phase. This module scans the input stream and groups characters into meaningful "tokens".
* **Functionality:** Ignores comments (`//`, `/** */`) and whitespace.
* **Classification:** Identifies and tags each token as one of the five Jack categories:
    * `KEYWORD` (e.g., `class`, `let`, `while`)
    * `SYMBOL` (e.g., `{`, `}`, `;`, `=`)
    * `INT_CONST` (0-32767)
    * `STRING_CONST` ("Hello World")
    * `IDENTIFIER` (variable and function names)

### 2. The Compilation Engine (`CompilationEngine`)
The syntax analysis phase. This module uses **Recursive Descent Parsing** to build the structure of the program.
* **Logic:** For every non-terminal in the Jack grammar (like `compileClass`, `compileSubroutine`, `compileExpression`), there is a corresponding method in the engine.
* **Lookahead:** The engine reads tokens sequentially and decides which grammatical rule to apply based on the current token (LL(1) Grammar logic).
* **Structure Handling:** It correctly handles nested structures, such as expressions within terms or `while` loops inside `if` statements.

## Output Format (XML)
Instead of generating machine code (which happens in Project 11), this stage outputs XML to visualize the **Parse Tree**. This serves as a debugging tool to verify the parser's logic.

**Example Input (`Main.jack`):**
```jack
class Main {
    function void main() {
        return;
    }
}
