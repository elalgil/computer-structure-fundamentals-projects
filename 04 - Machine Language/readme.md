# Project 4: Machine Language

In this project, I transitioned from hardware construction to low-level programming. I wrote programs in the **Hack Assembly Language** to perform arithmetic operations, manipulate arrays using pointers, and handle Input/Output (I/O) tasks by directly accessing memory maps.

## Overview
This project demonstrates the bridge between the hardware platform and software. It involves writing efficient assembly code to implement functionality that the ALU does not support natively (like multiplication) and managing I/O devices (Screen and Keyboard).

## Implemented Programs

### 1. Mult.asm (Multiplication)
* **Goal:** Multiplies the values in `R0` and `R1` and stores the result in `R2`.
* **Implementation:**
    * Since the Hack ALU only supports addition, I implemented multiplication via **repeated addition**.
    * **Optimization:** The code first checks if `R0` or `R1` are zero. If so, it jumps directly to the end to avoid unnecessary loops.
    * **Logic:** A loop adds the value of `R0` to `R2`, repeating `R1` times (decrementing a counter).

### 2. Fill.asm (I/O & Screen Manipulation)
* **Goal:** An infinite loop that listens to the keyboard and modifies the screen display.
* **Implementation:**
    * **Memory Mapping:** The program interacts with the **Screen** (starting at address 16384) and the **Keyboard** (address 24576).
    * **Logic:**
        * The program runs a continuous loop checking the `KBD` register.
        * **If a key is pressed:** It jumps to a "Black" loop, writing `-1` (1111111111111111 in binary) to every register in the screen's memory map.
        * **If no key is pressed:** It jumps to a "White" loop, writing `0` to clear the screen.
    * Uses pointer arithmetic to iterate through all 8,192 registers dedicated to the screen.

### 3. Swap.asm (Array & Pointer Arithmetic)
* **Goal:** Finds the Maximum and Minimum values in an array and swaps their locations.
* **Implementation:**
    * **Indirect Addressing:** The program heavily uses pointer logic (accessing `RAM[RAM[A]]`) since the array's base address is stored in a variable (`R14`) and its length in another (`R15`).
    * **Process:**
        1.  Iterates through the array to find the **minimum** value and saves its index.
        2.  Iterates again to find the **maximum** value and saves its index.
        3.  Swaps the content of the two addresses found.
    * **Edge Case Handling:** Checks if the array length allows for valid operations.

### 4. Max2.asm (Conditional Logic)
* **Goal:** Computes `max(R1, R2)` and stores the result in `R0`.
* **Implementation:** Uses simple branching logic (`JGE`, `JMP`) to compare the two values and route the larger one to the output register.

## Usage
To run these programs:
1.  Open the **CPU Emulator** (included in the Nand2Tetris suite).
2.  Load the desired `.asm` file.
3.  (Optional) Load the corresponding test script (`.tst`).
4.  Run the simulation.

---
*Part of the Nand to Tetris course.*
