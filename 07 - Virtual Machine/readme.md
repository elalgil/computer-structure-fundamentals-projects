# Project 7: Virtual Machine I - Stack Arithmetic

In this project, I built the first part of the **VM Translator**. This tool serves as the backend of the compiler, translating high-level Virtual Machine (VM) intermediate code into Hack Assembly language that can be executed on the hardware platform.

## Overview
The Hack Virtual Machine is modeled as a **Stack Machine**. In this project, I implemented the core mechanism of this machine:
1.  **Stack Arithmetic**: Performing logical and arithmetic operations using the stack.
2.  **Memory Access**: managing data transfer between the stack and various virtual memory segments (local, argument, this, that, etc.).

## Software Architecture
The implementation uses a modular Python design:

* **`Parser.py`**: Handles the reading of `.vm` input files. It cleans whitespace/comments and breaks down each VM command into its components (command type, segment, index).
* **`CodeWriter.py`**: The core translation engine. It generates the specific Hack Assembly code sequences required to implement:
    * Arithmetic commands (`add`, `sub`, `neg`, `eq`, `gt`, `lt`, `and`, `or`, `not`).
    * Memory access commands (`push`, `pop`) for all 8 memory segments.
* **`Main.py`**: The driver program. It iterates through the input files, initializes the Parser and CodeWriter, and manages the output generation.

## Test Suites & Validation
The project includes specific test directories used to validate the translator's logic against the course's reference implementation. My translator was tested on:

### 1. Stack Arithmetic (`StackArithmetic/`)
Focuses on the ALU operations of the VM.
* **Tests:** Validates that `push constant` works and that the stack correctly processes arithmetic (`add`, `sub`) and boolean (`eq`, `gt`, `lt`) operations.
* **Key Challenge:** Implementing comparison logic (`eq`, `gt`, `lt`) in Assembly using conditional jumps.

### 2. Memory Access (`MemoryAccess/`)
Focuses on the mapping of virtual segments to the physical RAM.
* **BasicTest:** Tests `push`/`pop` operations with `local`, `argument`, `this`, `that`, `temp`, and the implementation of `static` variables.
* **PointerTest:** Verifies the handling of the `pointer` segment (mapping to `THIS`/`THAT` pointers).
* **StaticTest:** Ensures that static variables are globally unique across the file namespace.

## Usage
To translate a VM file or a directory of VM files:

```bash
# Translates file.vm to file.asm
python Main.py path/to/file.vm

# OR using the wrapper script
./VMtranslator path/to/file.vm
