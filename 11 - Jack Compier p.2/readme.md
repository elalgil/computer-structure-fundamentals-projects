# Project 11: Jack Compiler II - Code Generation

In this final project of the software track, I built a full-scale **Optimizing Compiler** for the Jack programming language. Unlike the Syntax Analyzer (Project 10) which outputted XML, this compiler generates executable **Virtual Machine (VM)** code that runs on the Hack platform.

## Overview
This project completes the bridge between high-level code and the hardware. It translates object-oriented Jack code into the intermediate VM language, handling memory allocation, variable scoping, and expression evaluation.

**The Pipeline:**
`Source (.jack)` -> **`Tokenizer (Regex)`** -> **`Parser & Symbol Table`** -> **`VM Writer`** -> `Executable (.vm)`

## Core Architecture

### 1. Robust Tokenizer (Regex-Based)
The `JackTokenizer` module performs lexical analysis. Instead of simple string splitting, I utilized **Regular Expressions (Regex)** to create a robust scanner.
* **Regex Usage:** I utilized Python's `re` library to define precise patterns for language constructs. This allows the tokenizer to:
    * Identify identifiers, keywords, and integer constants instantly.
    * Correctly handle string literals (including spaces/symbols inside quotes).
    * Strip out complex comments (`//` single line and `/** */` multi-line blocks) while preserving line numbering for error reporting.

### 2. Symbol Table & Scoping
To support the language's semantics, I implemented a `SymbolTable` that manages variable lifecycles across nested scopes.
* **Nested Scopes:** The table distinguishes between **Class-Level** scope (static, field) and **Subroutine-Level** scope (argument, local).
* **Memory Mapping:** It assigns a running index and a memory segment (`local`, `argument`, `this`, `static`) to each variable type, allowing the compiler to translate `x = x + 1` into precise memory operations (e.g., `push local 0`, `push constant 1`, `add`).

### 3. Compilation Engine (Code Generation)
This is the core logic that traverses the parse tree (Recursive Descent) and orchestrates the translation.
* **Expression Evaluation:** Converts infix expressions (e.g., `a + b * c`) into Postfix VM commands (stack-based arithmetic).
* **Control Flow:** Handles high-level constructs like `while` and `if` by generating unique labels and `goto`/`if-goto` logic.
* **Object Handling:** Compiles method calls (passing `this` as the first argument) and constructor memory allocation (`Memory.alloc`).

### 4. VM Writer
The `VMWriter` module serves as an abstraction layer. Instead of hardcoding string concatenations in the engine, this module exposes an API (e.g., `write_push`, `write_arithmetic`) that ensures clean, error-free VM syntax generation.

## Input / Output Example

**Input (High Level):**
```jack
function int solve(int a, int b) {
    var int sum;
    let sum = a + b;
    return sum;
}
```
ת
```VM Language
function Main.solve 1   // 1 local variable (sum)
push argument 0         // push a
push argument 1         // push b
add                     // compute a + b
pop local 0             // sum = result
push local 0            // push sum
return                  // return value
```
