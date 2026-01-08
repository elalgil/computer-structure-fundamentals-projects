# Project 9: The Maze Escape (Jack Language)

A complex graphical game developed in the **Jack** programming language (a Java-like language designed for the Hack computer platform). The project demonstrates advanced algorithmic implementation and low-level optimization within a constrained environment.

## 🎮 Game Overview
The player is trapped in a maze and must reach the exit point. However, an intelligent enemy is actively hunting the player using a pathfinding algorithm.

* **Goal:** Navigate through the maze to find the exit without being caught by the enemy.
* **Controls:** Use the arrow keys to move the player.
* **Replayability:** Mazes are randomly selected from a predefined pattern pool to ensure variety.

## 🚀 Technical Highlights & Engineering

This project goes beyond simple game logic by implementing core computer science concepts "from scratch" to overcome the limitations of the Jack language (no standard library, no Garbage Collector, weak typing).

### 1. AI & Pathfinding (BFS Algorithm)
Instead of simple random movement, the enemy tracks the player intelligently.
* **Algorithm:** I implemented **Breadth-First Search (BFS)** to calculate the shortest path from the enemy to the player in real-time.
* **Custom Data Structure:** Since Jack has no `Queue` or `ArrayList`, I implemented a robust **`Queue` class** (`Queue.jack`) using a circular array buffer. This manages the BFS frontier efficiently without causing heap overflows.
* **Optimization:** Path recalculation is throttled to balance between AI intelligence and CPU cycles, ensuring the game runs smoothly on the simulator.

### 2. High-Performance Graphics (Direct Memory Access)
Standard Jack rendering (`Screen.drawPixel`) is too slow for moving sprites.
* **Memory Poking:** I built a custom rendering engine (`MazeRenderer.jack`) that draws entities by writing 16-bit words directly into the Video RAM (starting at memory address 16384).
* **Bit-Masking:** Walls, the player, and the enemy are rendered using bit-masks (arrays of 16-bit integers). This allows rendering a 16x16 pixel sprite in a few CPU cycles instead of 256 individual draw calls.

### 3. Software Architecture
The code follows strict Object-Oriented principles:
* **`Main.jack`**: The entry point that initializes the game instance.
* **`MazeGame.jack`**: The central controller. Manages the game loop, time deltas, collision detection, and orchestrates the AI and Player interactions.
* **`InputHandler.jack`**: Decouples user input from game logic, allowing for responsive control handling and clean code separation.
* **`Random.jack`**: Implements a **Linear Congruential Generator (LCG)** to provide pseudo-randomness for level selection (since Jack lacks a built-in `Math.random`).
* **`Patterns.jack`**: A database of valid maze layouts, ensuring generated levels are always solvable.

## 🛠️ Development Workflow & Tools

### Asset Generation (Bitmap Editor)
To create the custom visual assets (Player sprite, Enemy sprite, and Wall textures), I utilized a custom **Bitmap Editor** tool (`BitmapEditor.html`).
* **Process:** I designed the 16x16 pixel art visually using this web-based tool.
* **Code Generation:** The tool generates the specific integer values (bit-masks) which I then embedded into the `MazeRenderer` class constants. This bridged the gap between visual design and low-level memory manipulation.

## 📂 Project Structure
* `source/` - Contains all `.jack` source files (`Main`, `MazeGame`, `Queue`, `Player`, etc.).
* `tools/` - Contains `BitmapEditor.html` used for asset creation.
* `Main.vm` etc. - Compiled VM code ready for the VM Emulator.

## 🛠️ Challenges Solved
* **Memory Management:** Without a Garbage Collector, I had to manually manage memory allocation and deallocation (`dispose` methods) for the BFS Queue and Arrays to prevent memory leaks during long gameplay sessions.
* **Hardware Constraints:** The Hack platform has a limited instruction set. Implementing complex logic like BFS required careful optimization to maintain a playable frame rate.

## Usage
1.  Compile the directory using the **JackCompiler**.
2.  Load the directory into the **VM Emulator**.
3.  Run the game (Uncheck "Animate" for best performance).
4.  **Controls:** Arrow keys to move.

---
*Developed as part of the Nand to Tetris (Elements of Computing Systems) course.*
