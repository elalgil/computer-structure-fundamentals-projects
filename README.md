# Computer Structure Fundamentals: From NAND to Tetris

This repository contains the complete implementation of a general-purpose computer system, built from the ground up. Starting from the most elementary logic gate (**NAND**), I constructed a hardware platform, a full software hierarchy (Assembler, VM, Compiler), and finally an Operating System and an interactive application.

The project follows the "First Principles" approach, demystifying how computers work by implementing every layer of abstraction personally.

**Course Link:** [Nand2Tetris (The Elements of Computing Systems)](https://www.nand2tetris.org/)

## 🏗️ The Architecture: Layer by Layer

The repository is organized to reflect the gradual construction of the computer, moving from low-level hardware to high-level software.

```text
computer-structure-fundamentals-projects/
├── I. Hardware Platform (HDL)
│   ├── 01-Boolean-Logic/          # Logic Gates (And, Or, Xor, Mux)
│   ├── 02-Boolean-Arithmetic/     # ALU & Adders
│   ├── 03-Sequential-Logic/       # RAM & Registers
│   ├── 04-Machine-Language/       # Assembly Programming (Low-Level)
│   └── 05-Computer-Architecture/  # CPU & Memory Integration
│
├── II. System Software (Python)
│   ├── 06-Assembler/              # Translates Assembly to Binary
│   ├── 07-VM-Translator-I/        # Stack Arithmetic Translation
│   ├── 08-VM-Translator-II/       # Control Flow & Function Calls
│   ├── 10-Compiler-Syntax/        # Tokenizer & Parser (XML Output)
│   └── 11-Compiler-Code-Gen/      # Full Compilation to VM Code
│
└── III. High-Level Applications (Jack Language)
    ├── 09-The-Maze-Game/          # Complex OOP Game with AI & Graphics
    └── 12-Operating-System/       # Standard Library (Math, Screen, Memory...)
