# Project 8: Virtual Machine II - Control Flow & Function Calls

In this project, I completed the **VM Translator**, enabling it to handle complex program flow and function abstraction. This extends the basic stack arithmetic implemented in Project 7 to support branching, looping, and full function call protocols.

## Overview
The goal was to implement the commands that allow high-level languages to control execution flow. This involved translating high-level VM abstractions into low-level Hack Assembly jumps and memory management logic.

## Key Features Implemented

### 1. Program Flow (Branching)
Implemented the logic required for loops and conditional statements (if-else).
* **Commands:** `label`, `goto` (unconditional jump), `if-goto` (conditional jump based on stack value).
* **Mechanism:** Translates VM labels into Assembly labels and uses the stack's top value to determine branching logic.

### 2. Function Calling Protocol
Implemented the complete Function Call Stack mechanism, allowing for nested calls and recursion (e.g., calculating Fibonacci sequences).
* **Commands:** `function`, `call`, `return`.
* **The Stack Frame:** When a function is called, the translator generates assembly code to:
    * Save the caller's state (return address, LCL, ARG, THIS, THAT) onto the stack.
    * Reposition the `LCL` and `ARG` segment pointers for the callee.
    * Transfer control to the function.
* **Return Logic:** When returning, the translator restores the caller's state and memory segments from the stack frame and pushes the return value.

### 3. Bootstrap Code
Added the initialization logic (`Sys.init`) that runs when the computer boots up. This code initializes the stack pointer (`SP`) and calls the main operating system function.

## Module Structure (`CodeWriter.py`)
The `CodeWriter` module was significantly expanded to handle:
* **Label Management:** Generating unique labels for internal jumps (to avoid naming collisions in different functions).
* **Context Switching:** Managing the intricate pointer manipulation required during function calls and returns.

## Validation Suites
The implementation was tested against the course's advanced test suites (located in `ProgramFlow/` and `FunctionCalls/`):
* **BasicLoop / FibonacciSeries:** Validates correct loop execution.
* **SimpleFunction:** Tests basic frame saving/restoring.
* **NestedCall:** verifies that `Sys.init` calls `Sys.main`, which calls `Sys.add12`, maintaining the stack integrity throughout.
* **FibonacciElement:** A full recursive implementation of the Fibonacci algorithm, testing the limits of the stack logic.

## Usage
To translate a full directory (simulating a program linking process):

```bash
# Translates all .vm files in the directory into a single .asm file
python Main.py path/to/directory/
