# Project 2: Boolean Arithmetic

In this project, I implemented the arithmetic logic required for the computer's CPU. Starting from simple adders, I built a full 16-bit Adder and finally a fully functional Arithmetic Logic Unit (ALU).

## Overview
This project bridges the gap between boolean logic (Project 1) and arithmetic operations. The resulting ALU is capable of performing additions, subtractions, and bitwise logical operations, which serves as the computational core of the Hack computer.

## Implemented Chips

### Binary Adders
* **HalfAdder**: Adds two bits and returns a sum and a carry.
* **FullAdder**: Adds three bits (two inputs + carry in) and returns a sum and a carry.
* **Add16**: A 16-bit adder built by cascading FullAdders.
* **Inc16**: A 16-bit incrementer (adds 1 to the input).

### The ALU (Arithmetic Logic Unit)
* **ALU**: The centerpiece of the CPU arithmetic. It computes a function on two 16-bit inputs based on 6 control bits.
    * Supported operations: addition, subtraction, bitwise AND/OR, negation, and constant output (0/1).
    * Output flags: `zr` (zero result) and `ng` (negative result).

### Bit Shifters
* **ShiftLeft**: Shifts the bits of a 16-bit number one position to the left (multiplication by 2).
* **ShiftRight**: Shifts the bits of a 16-bit number one position to the right (division by 2).

## Usage
To test the implementation:
1.  Load the `.hdl` file into the **Hardware Simulator**.
2.  Load the corresponding test script (`.tst` file).
3.  Run the simulation.
4.  Verify that the output matches the comparison file (`.cmp`).

---
*Part of the Nand to Tetris course.*
