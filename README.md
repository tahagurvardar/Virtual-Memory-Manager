# Virtual Memory Manager

A Python GUI-based Operating Systems project that simulates virtual memory management using page replacement algorithms.

## Features

- FIFO (First In First Out)
- LRU (Least Recently Used)
- Optimal Page Replacement
- Page Fault calculation
- Page Hit calculation
- Fault ratio calculation
- Graphical comparison chart
- Tkinter GUI
- Step-by-step simulation

---

## Technologies Used

- Python
- Tkinter

---

## Algorithms

### FIFO
Removes the oldest page from memory.

### LRU
Removes the least recently used page.

### Optimal
Removes the page that will not be used for the longest future time.

---

## Example Input

Page Reference String:

```text
1 2 3 4 1 2 5 1 2 3 4 5
```

Frames:

```text
3
```

---

## Screenshots

### Main Window

![Main Window](screenshots/main_window.png)

### Simulation

![Simulation](screenshots/simulation.png)

---

## How to Run

Clone repository:

```bash
git clone https://github.com/USERNAME/Virtual-Memory-Manager.git
```

Go into project:

```bash
cd Virtual-Memory-Manager
```

Run:

```bash
python virtual_memory_manager.py
```

---

## Project Purpose

This project was developed for an Operating Systems course to demonstrate virtual memory management concepts and page replacement algorithms.