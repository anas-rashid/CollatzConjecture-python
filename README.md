# Collatz Conjecture (Python)

An interactive visualizer for the **Collatz Conjecture** built with Python, tkinter, and Matplotlib — styled with the [Catppuccin Mocha](https://github.com/catppuccin/catppuccin) color palette.

## What is the Collatz Conjecture?

Given any positive integer **x**, apply the following rules repeatedly:

- If **x** is **even** → `x = x / 2`
- If **x** is **odd** → `x = 3x + 1`

The conjecture states that no matter which starting value you choose, the sequence will always eventually reach **1**. Simple to state, yet unproven for over 80 years.

## Features

- Plot the Collatz sequence for any integer x ≥ 2
- Four chart types: **Line**, **Scatter**, **Bar**, **Step**
- Hover tooltip explaining the Collatz equation
- View the full sequence values in a scrollable dialog
- Clean graph to start fresh
- Navigation toolbar for zoom, pan, and export
- Dark theme (Catppuccin Mocha)

## Requirements

```
python >= 3.10
matplotlib
tkinter (usually bundled with Python)
```

Install dependencies:

```bash
pip install matplotlib
```

## Usage

```bash
python collatz.py
```

Enter a starting value for **x**, choose a graph type, and click **Plot** (or press Enter).
