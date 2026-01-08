# Project 10: Jack Compiler I - Syntax Analysis

In this project, I built the **Syntax Analyzer** (Parser) for the Jack programming language. This is the first stage of the full compiler (Front-End), responsible for reading source code, tokenizing it, and outputting its grammatical structure as XML.

## Overview
The goal was to transform raw text (Jack source code) into a structured **Parse Tree**. This process verifies that the code conforms to the Jack language grammar and serves as the foundation for the code generation phase (Project 11).

**The Pipeline:**
`Source Code (.jack)` -> **`Tokenizer`** -> **`Compilation Engine`** -> `Parse Tree (.xml)`

## Components & Implementation

### 1. The Tokenizer (`JackTokenizer.py`)
This module performs **Lexical Analysis**. It scans the `.jack` input file and breaks it down into atomic units called "tokens".
* **Functionality:** Strips out all comments (`//`, `/** */`) and whitespace.
* **Token Types:** Classifies each token into one of five categories:
    * `KEYWORD` (`class`, `method`, `int`, etc.)
    * `SYMBOL` (`{`, `}`, `=`, `;`, etc.)
    * `INT_CONST` (Integer literals)
    * `STRING_CONST` (String literals)
    * `IDENTIFIER` (Variable/Class names)

### 2. The Compilation Engine (`CompilationEngine.py`)
This module performs **Syntax Analysis** using a **Recursive Descent Parser**.
* **Structure:** For every rule in the Jack Grammar (e.g., `class`, `subroutineDec`, `expression`), there is a corresponding method in the Python class (e.g., `compile_class()`, `compile_subroutine()`).
* **XML Generation:** As the parser traverses the code, it writes the corresponding XML tags to the output file, creating a hierarchical representation of the program logic.

### 3. Build & Execution (`Makefile` & Wrapper)
To comply with the course's strict submission requirements (which run on a Linux environment), the project includes:
* **`Makefile`**: Ensures the execution environment is set up correctly. In this Python implementation, it simply grants execution permissions (`chmod +x`) to the wrapper script.
* **`JackAnalyzer`**: A shell script wrapper that invokes the Python interpreter on `JackAnalyzer.py`, allowing the program to be run directly from the command line as an executable.

## XML Output Example
Here is an example of how the analyzer translates a simple Jack snippet into XML.
**Example Output (`Main.xml`):**

```xml
<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
```

**Input (`Main.jack`):**
```jack
class Main {
    function void main() {
        return;
    }
}
