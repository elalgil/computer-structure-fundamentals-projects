# Computer Structure Fundamentals: From NAND to Tetris

**A full-stack implementation of a general-purpose computer system, built from the ground up.**

This repository documents my journey of constructing a complete computer system—from the most elementary logic gate to a high-level object-oriented game and a functioning Operating System. 

The project follows the "First Principles" approach, demystifying the "black box" of computing by implementing every single layer of abstraction personally.

🔗 **Course:** [Nand2Tetris (The Elements of Computing Systems)](https://www.nand2tetris.org/)

---

## 💡 Rationale & Architecture: The "First Principles" Approach

The core philosophy of this project is **Abstraction**. Modern computers are built in layers, where each layer relies on the one below it while hiding its complexity. 

I built this system in **two main phases**, creating a bridge between hardware and software:

### Phase 1: The Hardware Platform (Logic & Architecture)
Starting with nothing but a primitive **NAND** gate, I designed the hardware using **HDL (Hardware Description Language)**.
1.  **Logic Gates:** Combined NAND gates to create AND, OR, XOR, and Multiplexers.
2.  **Arithmetic:** Built a Half-Adder, Full-Adder, and a 16-bit **ALU** (Arithmetic Logic Unit).
3.  **Memory:** Constructed sequential logic chips (Bit, Register, RAM8... RAM16K) and a Program Counter (PC).
4.  **CPU:** Integrated the ALU and Registers into a Central Processing Unit capable of executing machine instructions (Fetch-Decode-Execute cycle).

### Phase 2: The Software Hierarchy (Toolchain & OS)
Once the hardware was simulated, I built the software tools required to run programs on it. These tools were developed in **Python**.
1.  **Assembler:** Translates symbolic Hack Assembly into binary machine code.
2.  **VM Translator:** A backend that maps a Stack-Machine architecture (Intermediate Representation) onto the register-based hardware.
3.  **Compiler:** A full-scale compiler (Front-end & Back-end) for the high-level **Jack** language.
4.  **Operating System:** A standard library (Math, Memory, Screen, String) implementing core services efficiently in software.

---

## 🛠️ Tech Stack & Tools Used

This project required a versatile use of different programming paradigms and languages:

| Component | Technology / Language | Usage |
| :--- | :--- | :--- |
| **Hardware** | **HDL** (Hardware Description Language) | Designing Chip Logic, ALU, CPU, and RAM. |
| **System Tools** | **Python** | Writing the **Assembler**, **VM Translator**, and **Compiler**. |
| **Parsing** | **Regex** & **Context-Free Grammar** | Used in the Compiler's Tokenizer and Parser (LL1). |
| **Low-Level** | **Hack Assembly** | Writing optimized code for I/O and arithmetic. |
| **High-Level** | **Jack** (Java-like) | Developing the **Operating System** and the **Game Application**. |

---

## 🚀 Key Skills Acquired

Through this project, I gained hands-on experience in core Computer Science and Engineering concepts:

### 1. Computer Architecture & Hardware Design
* **Logic Design:** Understanding combinatorial vs. sequential logic.
* **CPU Architecture:** Designing a Von Neumann architecture with instruction decoding and control bits.
* **Memory Hierarchy:** Building RAM units and understanding the Program Counter's role.

### 2. Compiler Construction & Language Design
* **Lexical Analysis:** Using **Regular Expressions (Regex)** to tokenize source code.
* **Parsing:** Implementing a **Recursive Descent Parser** to generate XML Parse Trees.
* **Code Generation:** Translating high-level OOP constructs (objects, methods, arrays) into low-level stack operations.
* **Symbol Tables:** Managing variable scope (static, field, local, argument) and memory allocation.

### 3. Algorithmic Optimization
* **Math Implementation:** Implementing multiplication ($O(\log n)$) and division algorithms in software constraints.
* **Graph Algorithms:** Implementing **BFS (Breadth-First Search)** for pathfinding in the game project.
* **Memory Management:** Writing a **Heap Allocator** (malloc/free) using a Free-List data structure.

### 4. System Programming
* **Virtualization:** Implementing a Stack Machine VM that abstracts the underlying hardware.
* **Drivers:** Writing low-level drivers for **Screen** (Memory Mapped I/O, Bit-masking) and **Keyboard**.

---

## 📂 Project Structure & Hierarchy

```text
computer-structure-fundamentals-projects/
├── I. Hardware Platform (HDL)
│   ├── 01-Boolean-Logic/          # Logic Gates (Not, And, Or, Xor, Mux)
│   ├── 02-Boolean-Arithmetic/     # Half/Full Adder, Inc16, ALU
│   ├── 03-Sequential-Logic/       # Flip-Flops, Registers, RAM8-RAM16K, PC
│   ├── 04-Machine-Language/       # Assembly code (Mult, I/O drivers)
│   └── 05-Computer-Architecture/  # CPU, Memory, and the complete Computer chip
│
├── II. System Software (Python)
│   ├── 06-Assembler/              # Logic to translate .asm to .hack binary
│   ├── 07-VM-Translator-I/        # Stack arithmetic & memory segments
│   ├── 08-VM-Translator-II/       # Control flow (branching) & Function call stack
│   ├── 10-Compiler-Syntax/        # Tokenizer & Parser (outputs XML structure)
│   └── 11-Compiler-Code-Gen/      # Full compilation to VM code (Symbol Tables)
│
└── III. High-Level Applications (Jack Language)
    ├── 09-The-Maze-Game/          # A complex game featuring AI (BFS) and custom graphics
    └── 12-Operating-System/       # The Standard Library (Math, Screen, String, Memory, etc.)
```

## Aוuther
Developed by Elal Gilboa as part of the Nand2Tetris certification.
│   ├── 01-Boolean-Logic/          # Logic Gates (Not, And, Or, Xor, Mux)
│   ├── 02-
