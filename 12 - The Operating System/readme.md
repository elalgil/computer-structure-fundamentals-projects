# Project 12: The Jack Operating System

In this final project, I implemented the **Jack Operating System (OS)**. This is a collection of standard library classes that provide essential services to Jack programs, bridging the gap between high-level code and the underlying hardware platform.

## Overview
The OS is written in the Jack language itself but is compiled separately and linked with user programs. It manages memory allocation, handles Input/Output (I/O) devices, implements mathematical operations, and controls program execution.

## System Architecture & Class Modules

### 1. Memory Management (`Memory.jack`, `Array.jack`)
The core of the system, managing the computer's RAM.
* **`Memory.alloc(size)`**: Implements a dynamic memory allocator using a **Free List** algorithm (First-fit or Best-fit) to find available blocks in the heap.
* **`Memory.deAlloc(object)`**: Recycles memory blocks back to the free list, handling de-fragmentation where possible.
* **`Memory.peek(address)` / `Memory.poke(address, value)`**: Provides direct hardware memory access, essential for driver implementation.
* **`Array` Class**: A wrapper around `Memory.alloc` that allows creating dynamic arrays.

### 2. Mathematical Library (`Math.jack`)
Since the Hack ALU only supports addition and subtraction, this class implements complex arithmetic in software.
* **`multiply(x, y)`**: Implements efficient bit-wise multiplication (Shift-and-Add algorithm) ($O(\log n)$).
* **`divide(x, y)`**: Implements long division using recursion.
* **`sqrt(x)`**: Computes integer square roots using a binary-search-like approach tailored for 16-bit numbers.
* **`min`, `max`, `abs`**: Basic utility functions.

### 3. Graphics & Screen Driver (`Screen.jack`)
Handles direct interaction with the memory-mapped screen segment (Video RAM).
* **`drawPixel(x, y)`**: Calculates the exact memory address and bit-mask to toggle a single pixel.
* **`drawLine(x1, y1, x2, y2)`**: Implements **Bresenham's Line Algorithm** for efficient line drawing using only integer arithmetic.
* **`drawRectangle(x1, y1, x2, y2)`**: An optimized routine that fills rows of 16 pixels at a time (word-aligned) for speed.
* **`drawCircle(x, y, r)`**: Draws filled circles using an efficient calculation to determine row widths (Pythagorean theorem optimization).

### 4. Text Output (`Output.jack`)
Manages the textual display using a bitmap font map.
* **Cursor Management**: Tracks `cursor_x` and `cursor_y` to determine where the next character should appear.
* **`printChar(c)`**: Renders a character bitmap to the screen RAM.
* **`printString(s)`, `printInt(i)`**: Utility functions to format and display data types.

### 5. Keyboard Input (`Keyboard.jack`)
Handles interaction with the memory-mapped keyboard register.
* **`keyPressed()`**: Returns the raw scan code of the key currently pressed.
* **`readChar()`**: Waits for a key press, echoes it to the screen, and handles backspace logic.
* **`readLine(message)`, `readInt(message)`**: buffers user input until a newline is detected.

### 6. String Manipulation (`String.jack`)
Implements the string data type and conversion logic.
* **`setInt(number)`**: Converts an integer to its string representation (ASCII) using recursion.
* **`intValue()`**: Parses the string content into an integer value.
* **Dynamic Sizing**: Manages the underlying character array length.

### 7. System Control (`Sys.jack`)
The entry point and supervisor of the OS.
* **`init()`**: The first function executed by the hardware. It initializes all other OS modules (Memory, Math, Screen, etc.) in the correct order and then calls `Main.main()`.
* **`halt()`**: Stops execution by entering an infinite loop.
* **`wait(duration)`**: Pauses execution for a set amount of time (approximate milliseconds).
* **`error(errorCode)`**: Reports runtime errors (like array index out of bounds) by printing a code and halting.

## ⚡ Algorithmic Efficiency

Since the Hack hardware platform is extremely primitive (lacking native multiplication, division, or floating-point units), the Operating System must implement these operations in software. To ensure reasonable performance, I implemented standard efficient algorithms rather than naive approaches.

### Mathematical Optimizations (`Math.jack`)
* **Multiplication (Shift-and-Add):** Instead of naive repeated addition (which is $O(n)$), I implemented the **Shift-and-Add algorithm**. This allows multiplying two 16-bit numbers in exactly 16 iterations ($O(\log n)$ complexity), manipulating bits directly.
* **Division (Recursive Long Division):** I implemented a recursive long division algorithm ($O(\log n)$) that builds the quotient bit by bit, avoiding the slow process of repeated subtraction.
* **Square Root (Binary Search):** Finding the integer square root is done using a binary search-like approach on the bits. The algorithm determines the root in exactly $n/2$ (8) iterations for 16-bit numbers, checking `(y + 2^j)^2 <= x` at each step.

### Graphics Optimizations (`Screen.jack`)
* **Line Drawing (Bresenham’s Algorithm):** Drawing a line requires determining which pixels to approximate on a grid. I implemented **Bresenham's Line Algorithm**, which relies solely on integer addition and subtraction (avoiding expensive division or floating-point calculations) to determine the "error" term and choose the next pixel.
* **Circle Drawing:** To draw filled circles efficiently, the algorithm uses the Pythagorean theorem ($dy^2 + dx^2 = r^2$) to calculate the horizontal width of the circle at each row, drawing it as a series of horizontal lines (using `drawLine`) rather than calculating every pixel individually.

## Test Suite & Verification
The implementation was rigorously tested using the official Nand2Tetris test suite. Each module is tested in isolation:

1.  **`ArrayTest`**: Verifies dynamic allocation and disposal of arrays.
2.  **`MathTest`**: Checks correctness of multiplication, division, and sqrt on edge cases (negative numbers, overflow, zero).
3.  **`MemoryTest`**: Stress-tests the heap allocator to ensure no memory leaks occur and that the free list is maintained correctly.
4.  **`ScreenTest`**: Visual test to verify that lines, rectangles, and circles are drawn correctly without artifacts.
5.  **`StringTest`**: Validates `setInt` and `intValue` conversions.
6.  **`OutputTest`**: Visual test for text alignment, backspacing, and line wrapping.
7.  **`SysTest`**: checks the `wait` function accuracy.

## Usage
To use this OS, the `.vm` files generated from these classes must be present in the same directory as the user's compiled program. The VM Emulator automatically loads these libraries when running the program.

---
*Part of the Nand to Tetris course.*
