# Project 3: Sequential Logic & Memory

In this project, I built the computer's volatile memory (RAM) and the Program Counter (PC). Unlike the previous projects which dealt with combinational logic, this project introduces sequential logic, allowing the system to maintain state over time using a clock signal.

## Overview
Starting from a primitive Data Flip-Flop (DFF), I constructed 1-bit and 16-bit registers, and then scaled them up to build a complete RAM hierarchy. I also implemented a Program Counter (PC) that manages the instruction execution flow.

## Implemented Chips

### Basic Storage Units
* **Bit**: A 1-bit register (stores 1 bit of data). Built using a DFF and a Multiplexer.
* **Register**: A 16-bit register. The atomic storage unit of the CPU.

### RAM (Random Access Memory) hierarchy
I implemented a recursive hierarchy of RAM chips, where each level aggregates the previous one:
* **RAM8**: A memory of 8 registers (16-bit each).
* **RAM64**: Holds 64 registers (composed of 8 RAM8 chips).
* **RAM512**: Holds 512 registers.
* **RAM4K**: Holds 4,096 registers.
* **RAM16K**: Holds 16,384 registers.

### Control Logic
* **PC (Program Counter)**: A 16-bit counter used to address the next instruction in memory.
    * Features: Increment (next instruction), Load (jump to address), and Reset (restart program).

## Key Concepts
* **Sequential Logic**: Logic that depends on input history (state), not just current input.
* **Clocked Chips**: Using the master clock signal to synchronize state updates.
* **Feedback Loops**: Feeding the output of a chip back into its input to preserve data.

## Usage
To test the implementation:
1.  Load the `.hdl` file into the **Hardware Simulator**.
2.  Load the corresponding test script (`.tst` file).
3.  Run the simulation.
4.  Verify that the output matches the comparison file (`.cmp`).

---
*Part of the Nand to Tetris course.*
