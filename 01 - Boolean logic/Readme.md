# Project 1: Boolean Logic

In this project, I implemented a set of elementary logic gates using the Hardware Description Language (HDL). These gates form the building blocks for the entire computer architecture built in later stages.

## Overview
Starting from a primitive `Nand` gate, I constructed basic logic gates (Not, And, Or, Xor) and more complex multi-bit and multi-way chips (Mux, DMux).

## Implemented Chips
The following chips were implemented in HDL:

### Elementary Logic Gates
* **Not**: Inverts the input bit.
* **And**: Returns 1 if both inputs are 1.
* **Or**: Returns 1 if at least one input is 1.
* **Xor**: Returns 1 if inputs are different (Exclusive Or).
* **Mux** (Multiplexer): Selects between two inputs based on a selection bit.
* **DMux** (Demultiplexer): Channels the input to one of two outputs based on a selection bit.

### 16-Bit Variants
* **Not16**: 16-bit bitwise Not.
* **And16**: 16-bit bitwise And.
* **Or16**: 16-bit bitwise Or.
* **Mux16**: 16-bit Multiplexer.

### Multi-Way Variants
* **Or8Way**: 8-way Or gate.
* **Mux4Way16**: 4-way 16-bit Multiplexer.
* **Mux8Way16**: 8-way 16-bit Multiplexer.
* **DMux4Way**: 4-way Demultiplexer.
* **DMux8Way**: 8-way Demultiplexer.

## Usage
To test the implementation:
1.  Load the `.hdl` file into the **Hardware Simulator**.
2.  Load the corresponding test script (`.tst` file).
3.  Run the simulation.
4.  Verify that the output matches the comparison file (`.cmp`).

---
*Part of the Nand to Tetris course.*
