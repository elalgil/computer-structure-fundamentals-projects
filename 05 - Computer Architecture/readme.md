# Project 5: Computer Architecture

In this project, I constructed the complete **Hack Hardware Platform**. This is the culmination of the hardware track of the course, where individual chips built in previous projects (ALU, RAM, PC) are integrated into a fully functioning computer capable of running machine language programs.

## Overview
The goal was to build the top-level architecture of the computer. This involved designing the memory hierarchy, the central processing unit (CPU), and connecting them via the system bus to execute instructions fetched from the ROM.

## Implemented Chips

### 1. CPU.hdl (Central Processing Unit)
The CPU is the "brain" of the computer. It executes instructions described by the Hack Machine Language.
* **Key Responsibilities:**
    * **Instruction Decoding:** Distinguishes between A-Instructions (addressing) and C-Instructions (computation).
    * **ALU Control:** Routes the correct operands (from the A-register, D-register, or Memory) to the ALU based on the instruction bits.
    * **Control Logic:** Manages write permissions for the Memory and Registers (A/D).
    * **Program Flow:** Updates the Program Counter (PC) to either increment to the next instruction or jump to a specific address based on ALU output flags (`zr`, `ng`).

### 2. Memory.hdl
A unified memory module that acts as the computer's address space. It handles input/output via **Memory-Mapped I/O**.
* **Address Mapping:**
    * `0 - 16383`: **RAM16K** (Data storage).
    * `16384 - 24575`: **Screen** (Video memory map).
    * `24576`: **
