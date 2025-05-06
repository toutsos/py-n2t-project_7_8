# Nand2Tetris Projects 7 & 8: VM Translator

**An implementation of the Virtual Machine (VM) Translator for Nand2Tetris Projects 7 & 8.**

This project implements a VM-to-Hack translator that converts VM commands into Hack assembly code. It handles stack-based virtual machine language commands as described in the Nand2Tetris curriculum.

## Features

- **Project 7 (Basic VM Translator):**

  - **Arithmetic Commands:** `add`, `sub`, `neg`, `eq`, `gt`, `lt`, `and`, `or`, `not`
  - **Memory Access:** `push` and `pop` for segments: `local`, `argument`, `this`, `that`, `constant`, `static`, `temp`, `pointer`

- **Project 8 (Extended VM Translator):**

  - **Program Flow:** `label`, `goto`, `if-goto`
  - **Functions:** `function`, `call`, `return`
  - **Bootstrap Code:** Initializes the VM and calls `Sys.init` if needed.

- **Single & Multi-File Translation:**
  Supports translating a single `.vm` file or an entire directory of `.vm` files.

- **Error Handling:**
  Basic error detection for invalid commands or arguments.

---

## Usage

1️⃣ **Clone the repository:**

```bash
git clone project
cd in project
```

2️⃣ **Run the translator:**

- **For a single file:**

```bash
python VMTranslator.py path/to/File.vm
```

- **For a directory:**

```bash
python VMTranslator.py path/to/Directory/
```

Example:

```bash
python VMTranslator.py StackArithmetic/SimpleAdd.vm
```

---

## Repository Structure

```
├── VMTranslator.py            # Main translator
├── parser.py                  # Parses VM commands
├── code_writer.py             # Translates VM commands to assembly
├── tests/                     # Test scripts and VM files (optional)
├── examples/                  # Example VM files
└── README.md
```

---

## How It Works

1. **Parser:**
   Reads each `.vm` file line by line and breaks down commands into components.

2. **CodeWriter:**
   Converts each VM command into Hack assembly code using the Hack platform conventions.

3. **Bootstrap:**
   When translating a directory, the translator inserts bootstrap code to initialize the stack and start the program.

---

## Example

**VM Code:**

```vm
push constant 7
push constant 8
add
```

**Output Assembly:**

```asm
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
```

---

## License

Specify your license (e.g., MIT).

---

## Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests to improve or extend functionality.
