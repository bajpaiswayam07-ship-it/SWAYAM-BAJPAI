<div align="center">

# ⚡ StructLab : Stack & Circular Queue Interactive Suite

**Production-Grade Interactive Visualizer, Educational Simulator & CLI Engine for Data Structures**

[![Developer](https://img.shields.io/badge/Developer-SWAYAM_BAJPAI-00f2fe?style=for-the-badge&logo=visual-studio-code&logoColor=black)](#-lead-architect--developer)
[![Platform](https://img.shields.io/badge/Platform-Windows_CMD_%7C_Web_Browser-00f5a0?style=for-the-badge&logo=windows&logoColor=black)](#-quick-start--execution)
[![Architecture](https://img.shields.io/badge/Engine-Zero--Dependency_Native-9d4edd?style=for-the-badge)](#-dual-runtime-architecture)
[![Complexity](https://img.shields.io/badge/Time_Complexity-O(1)_Constant-f59e0b?style=for-the-badge)](#-algorithmic-complexity-analysis)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

<br/>

> **"Bridging theoretical computer science and interactive systems programming with dual-engine visual execution in Terminal and Modern Web."**

</div>

---

## 📑 Table of Contents

- [Executive Summary](#-executive-summary)
- [Lead Architect & Developer](#-lead-architect--developer)
- [Dual-Runtime Architecture](#-dual-runtime-architecture)
- [Core Data Structures Engineering](#-core-data-structures-engineering)
  - [1. Stack Engine (LIFO)](#1-stack-engine-lifo---last-in-first-out)
  - [2. Circular Queue Ring Buffer (FIFO)](#2-circular-queue-ring-buffer-fifo---modulo-arithmetic)
- [Algorithmic Complexity Analysis](#-algorithmic-complexity-analysis)
- [Real-World Applied Systems Modules](#-real-world-applied-systems-modules)
  - [Compiler Syntax Bracket Parser](#1-compiler-syntax-bracket-parser)
  - [OS CPU Round-Robin Task Scheduler](#2-operating-system-cpu-round-robin-scheduler)
- [Interactive CLI Terminal Engine (CMD)](#-interactive-cli-terminal-engine-cmd)
- [Interactive Web Visualizer Engine](#-interactive-web-visualizer-engine)
- [Quick Start & Execution](#-quick-start--execution)
- [Keyboard Control Mapping](#-keyboard-control-mapping)
- [Directory & File Organization](#-directory--file-organization)
- [License & Open Source Notice](#-license)

---

## 🔬 Executive Summary

**StructLab** is a dual-interface Computer Science laboratory designed to eliminate the abstraction barrier when learning linear and ring-buffer data structures. 

Built with a **zero-dependency philosophy**, StructLab provides:
1. **A Native Windows Command Prompt (CMD) Terminal Engine** featuring dynamic ANSI ASCII rendering, memory address tracking (`0x7FFE00`), audio synthesizer feedback via PC frequency beepers, and a 3-stage animated `Pop()` execution pipeline.
2. **A High-Fidelity Cyberpunk Web Visualizer** with radial SVG geometry, real-time Modulo formula heads-up displays (HUD), multi-language implementation code (C++, Java, Python, JS), and interactive compiler/scheduler sandboxes.

---

## 👨‍💻 Lead Architect & Developer

<div align="center">

### **SWAYAM BAJPAI**
*Systems Programmer & Lead Software Architect*

```text
===========================================================================
███████╗██╗    ██╗ █████╗ ██╗   ██╗ █████╗ ███╗   ███╗
██╔════╝██║    ██║██╔══██╗╚██╗ ██╔╝██╔══██╗████╗ ████║
███████╗██║ █╗ ██║███████║ ╚████╔╝ ███████║██╔████╔██║
╚════██║██║███╗██║██╔══██║  ╚██╔╝  ██╔══██║██║╚██╔╝██║
███████║╚███╔███╔╝██║  ██║   ██║   ██║  ██║██║ ╚═╝ ██║
╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝
            B   A   J   P   A   I
===========================================================================
```

</div>

---

## ⚙️ Dual-Runtime Architecture

```
                                  +---------------------------------------+
                                  |         STRUCTLAB CORE SUITE          |
                                  +---------------------------------------+
                                                      |
                         +----------------------------+----------------------------+
                         |                                                         |
                         v                                                         v
        +-----------------------------------+                     +-----------------------------------+
        |       TERMINAL CLI ENGINE         |                     |        WEB CLIENT ENGINE          |
        |   (Windows CMD / PowerShell)      |                     |   (HTML5, Vanilla CSS3 & ES6)     |
        +-----------------------------------+                     +-----------------------------------+
        | • run.bat launcher                |                     | • Radial SVG Ring Visualizer      |
        | • ANSI Color ASCII Containers     |                     | • 3D Drop/Bounce Spring Physics   |
        | • Hardware Audio Beep Synthesizer |                     | • Web Audio API FM Synthesizer    |
        | • 3-Stage Pop() Pipeline          |                     | • Code Syntax Highlighting Engine |
        | • Memory Pointer Emulation        |                     | • Real-World Simulator Sandbox    |
        +-----------------------------------+                     +-----------------------------------+
```

---

## 🧩 Core Data Structures Engineering

### 1. Stack Engine (LIFO - Last In, First Out)

A contiguous array-backed stack where operations occur exclusively at the highest allocated index, designated as `TOP`.

```text
       +-------------------------------------+
  TOP  | [OPEN TOP - Push & Pop occur here]  |
       +-------------------------------------+
  [2]  | 42         <-- TOP (Current) [0x7FFE08] |
       +-------------------------------------+
  [1]  | 20                           [0x7FFE04] |
       +-------------------------------------+
  [0]  | 10                           [0x7FFE00] |
       +=====================================+
       |       STACK BASE (Index: 0)         |
       +=====================================+
```

#### Core Boundary Mechanics:
- **Stack Initialization:** `top = -1`, `capacity = N`.
- **Push(x) Invariant:** 
  $$\text{if } (\text{top} == \text{capacity} - 1) \implies \text{Overflow Exception}$$
  $$\text{else } \text{top} \leftarrow \text{top} + 1,\; \text{arr}[\text{top}] \leftarrow x$$
- **Pop() Invariant:**
  $$\text{if } (\text{top} == -1) \implies \text{Underflow Exception}$$
  $$\text{else } \text{val} \leftarrow \text{arr}[\text{top}],\; \text{top} \leftarrow \text{top} - 1,\; \text{return val}$$
- **Peek() Invariant:** Returns $\text{arr}[\text{top}]$ without mutating the pointer.

---

### 2. Circular Queue Ring Buffer (FIFO - Modulo Arithmetic)

Standard linear array queues suffer from **false overflow**: dequeuing elements leaves unutilized memory at the front of the array ($0$ to $\text{front} - 1$). Shifting elements costs $O(N)$ time.

**Circular Queue resolves this in $O(1)$ constant time** by utilizing clock arithmetic modulo $N$:

```text
                      [0]  <-- Front Wraparound
                   /       \
               [5]           [1]
                |    RING     |
               [4]  BUFFER   [2]
                   \       /
                      [3]  <-- Rear Wraparound
```

#### Modulo Pointer Formulas:
$$\text{Next Rear Index} = (\text{rear} + 1) \pmod{\text{capacity}}$$
$$\text{Next Front Index} = (\text{front} + 1) \pmod{\text{capacity}}$$

#### Critical Boundary Conditions:
- **Empty State:** $\text{count} == 0 \iff (\text{front} == -1 \land \text{rear} == -1)$
- **Full State (Overflow):** $\text{count} == \text{capacity} \iff (\text{rear} + 1) \pmod{\text{capacity}} == \text{front}$

---

## 📊 Algorithmic Complexity Analysis

| Operation | Standard Linear Queue | Stack (StructLab) | Circular Queue (StructLab) | Memory Efficiency |
| :--- | :---: | :---: | :---: | :---: |
| **Push / Enqueue** | $O(1)$ | $\mathbf{O(1)}$ *(Optimal)* | $\mathbf{O(1)}$ *(Optimal)* | Zero reallocation |
| **Pop / Dequeue** | $O(N)$ with shift | $\mathbf{O(1)}$ *(Optimal)* | $\mathbf{O(1)}$ *(Optimal)* | $100\%$ Slot reuse |
| **Peek / Top** | $O(1)$ | $\mathbf{O(1)}$ | $\mathbf{O(1)}$ | Direct indexed access |
| **Search** | $O(N)$ | $O(N)$ | $O(N)$ | Linear traversal |
| **Auxiliary Space** | $O(N)$ | $\mathbf{O(N)}$ *(Fixed Array)*| $\mathbf{O(N)}$ *(Ring Buffer)* | No memory fragmentation |

---

## 🛠️ Real-World Applied Systems Modules

### 1. Compiler Syntax Bracket Parser
- **Industry Analogy:** GCC, Clang, and V8 JavaScript parser token validation.
- **Workflow:**
  1. Scan string characters sequentially.
  2. Push opening bracket tokens `(`, `{`, `[` onto the Stack.
  3. On closing token `)`, `}`, `]`, verify whether `stack.pop()` yields the corresponding inverted pair.
  4. Returns `VALID / BALANCED` if and only if $\text{stack.isEmpty}()$ at EOF.

### 2. Operating System CPU Round-Robin Scheduler
- **Industry Analogy:** Linux CFS / Preemptive Thread Scheduler Ready Queue.
- **Workflow:**
  1. Processes ($P_1, P_2, \dots$) enter the Circular Queue with discrete CPU burst times.
  2. CPU core executes the process at `FRONT` for a fixed **Time Quantum ($Q = 2$)**.
  3. If remaining burst $> 0$, the process is preempted and re-enqueued at `REAR`.
  4. If remaining burst $= 0$, process terminates and leaves the queue.

---

## 💻 Interactive CLI Terminal Engine (CMD)

The Command Prompt edition (`run.bat`) features an interactive terminal application:

```text
===========================================================================
 STRUCTLAB : STACK & CIRCULAR QUEUE | DEVELOPER: SWAYAM BAJPAI
===========================================================================

  --- STACK VISUAL REPRESENTATION (LIFO) ---
  Capacity: 3 / 6  [Status: ACTIVE (top = 2)]

       +-------------------------------------+
  TOP  | [OPEN TOP - Push & Pop occur here]  |
       +-------------------------------------+
  [5]  | --- Empty Slot ---        [0x7FFE14] |
       +-------------------------------------+
  [4]  | --- Empty Slot ---        [0x7FFE10] |
       +-------------------------------------+
  [3]  | --- Empty Slot ---        [0x7FFE0C] |
       +-------------------------------------+
  [2]  | 42         <-- TOP (Current) [0x7FFE08] |
       +-------------------------------------+
  [1]  | 20                           [0x7FFE04] |
       +-------------------------------------+
  [0]  | 10                           [0x7FFE00] |
       +=====================================+
       |       STACK BASE (Index: 0)         |
       +=====================================+

  OPERATIONS:
  [1] Push(x)         [4] Fill Random
  [2] Pop()           [5] Clear Stack
  [3] Peek() / Top    [6] Change Capacity
  [7] ⚡ Developer Intro (SWAYAM BAJPAI)
  [0] Back to Main Menu
```

### Highlights of the Rebuilt `Pop()` System:
- **Intelligent Underflow Recovery:** If the user executes `Pop()` on an empty stack, instead of an abrupt failure, it explains the mathematical condition (`top == -1`) and offers an instant one-key prompt to push a value or fill sample elements.
- **3-Stage Visual Pipeline:**
  1. *Read Target:* Inspects item value and simulated hexadecimal address at `arr[top]`.
  2. *Decrement Pointer:* Smoothly moves `top` from $[k] \to [k-1]$.
  3. *Memory Deallocation:* Clears slot, plays synthesized pop audio, and pauses for inspection.

---

## 🌐 Interactive Web Visualizer Engine

Built with clean HTML5, CSS3 Glassmorphism, and Vanilla ES6:
- **Dynamic 3D Stack Tube:** Drop physics and bounce keyframes on push; upward particle ascent on pop.
- **Radial SVG Ring:** Computes angular slot positioning $(\theta_i = \frac{2\pi \cdot i}{N} - \frac{\pi}{2})$ with animated emerald (`FRONT`) and magenta (`REAR`) pointer markers.
- **Modulo HUD:** Real-time formula readout showing whether the next enqueue/dequeue triggers wrap-around.
- **Web Audio API Synthesizer:** Real-time frequency sweep generation without external audio dependencies.
- **Developer Cyber Badge:** Header badge for **SWAYAM BAJPAI** with hacker frequency chords on click (or shortcut `H`).

---

## 🚀 Quick Start & Execution

### Option A: Command Prompt (CMD) Execution *(Recommended)*
1. Open this directory in Command Prompt or File Explorer.
2. Run [`run.bat`](file:///c:/Users/Swayam/OneDrive/Desktop/Stack%20and%20Circular%20Queue/run.bat):
   ```cmd
   run.bat
   ```
3. Alternatively, launch directly via PowerShell:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\main.ps1
   ```

### Option B: Web Application Execution
1. Double-click [`index.html`](file:///c:/Users/Swayam/OneDrive/Desktop/Stack%20and%20Circular%20Queue/index.html) in Windows File Explorer.
2. Runs immediately in any browser (Google Chrome, Microsoft Edge, Brave, Mozilla Firefox).

---

## ⌨️ Keyboard Control Mapping

| Shortcut Key | Web Visualizer Action | Terminal CLI Action |
| :---: | :--- | :--- |
| <kbd>Enter</kbd> | Executes `Push()` or `Enqueue()` | Confirms selected menu option / Input |
| <kbd>Delete</kbd> / <kbd>Backspace</kbd> | Executes `Pop()` or `Dequeue()` | Standard character backspace |
| <kbd>1</kbd> | Switches to **Stack Visualizer** | Selects Option `[1]` |
| <kbd>2</kbd> | Switches to **Circular Queue Visualizer** | Selects Option `[2]` |
| <kbd>3</kbd> | Switches to **Real-World Applications** | Selects Option `[3]` |
| <kbd>4</kbd> | Switches to **Code Explorer** | Selects Option `[4]` |
| <kbd>5</kbd> | Switches to **Mastery Quiz** | Selects Option `[5]` |
| <kbd>H</kbd> | Triggers **SWAYAM BAJPAI Cyber Audio FX** | N/A (Select Option `[7]` in Main Menu) |

---

## 📁 Directory & File Organization

```
c:\Users\Swayam\OneDrive\Desktop\Stack and Circular Queue\
│
├── run.bat                 # One-click Windows CMD startup batch script
├── main.ps1                # Interactive Terminal CLI Suite (ANSI + Audio Engine)
├── index.html              # Modern Web Application client
├── stack_and_queue.cpp     # Standalone C++ menu-driven implementation
├── README.md               # Professional project documentation
│
├── css/
│   └── style.css           # Glassmorphism, Neon dark theme & micro-animations
│
└── js/
    ├── audio.js            # Web Audio API zero-latency sound synthesizer
    ├── codeSnippets.js     # Production C++, Java, Python & JS implementations
    ├── stack.js            # Stack data structure visualizer & parentheses engine
    ├── circularQueue.js    # Radial SVG Circular Queue & CPU scheduler simulator
    └── app.js              # Master application controller, quiz & keyboard events
```

---

## 📜 License

This project is open-source and released under the **MIT License**.

```text
Copyright (c) 2026 SWAYAM BAJPAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

<div align="center">

---

**Crafted with precision by [SWAYAM BAJPAI](#-lead-architect--developer)**  
*Empowering Developers and Students with Intuitive Data Structure Visualizations*

</div>
