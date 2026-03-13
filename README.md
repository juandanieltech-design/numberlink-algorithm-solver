NumberLink Algorithm Solver

Implementation and comparative analysis of different algorithmic approaches to solve the **NumberLink / FreeFlow puzzle**.

This project was developed as part of the **Algorithm Analysis course** and explores multiple paradigms for solving a constraint-based pathfinding problem.

## Problem Description

NumberLink is played on an **n × n grid** where pairs of identical numbers must be connected with continuous orthogonal paths. The solution must satisfy the following constraints:

* Paths must move only vertically or horizontally.
* Each pair of numbers must be connected by a single path.
* Paths cannot overlap or cross.
* The entire grid must be filled with paths.

The general version of the problem is known to be **NP-complete**, making it a challenging algorithmic problem.

## Algorithms Implemented

This project compares three different algorithmic approaches:

### Backtracking

A complete search algorithm that systematically explores all possible path configurations while respecting the constraints.

Characteristics:

* Guarantees a valid solution if one exists
* Computationally expensive for large boards
* Explores the full search space using recursion

### Greedy Algorithm

Connects pairs by selecting locally optimal paths (e.g., shortest paths).

Characteristics:

* Extremely fast
* Does not guarantee a valid solution
* May block future paths due to local decisions

### Constraint Satisfaction Problem (CSP)

Models the board as a constraint satisfaction problem where:

* variables represent pairs
* domains represent possible paths
* constraints ensure non-overlapping routes and full coverage

This approach allows pruning the search space through constraint checking.

## Interactive Interface

The project includes a **graphical interface built with Tkinter** that allows:

* manual interaction with the board
* drawing paths between numbers
* verifying solutions
* resetting the board
* visualizing algorithm execution step by step

## Experimental Analysis

A series of experiments were conducted using different board configurations to evaluate:

* success rate
* execution time
* algorithm robustness

Results show that:

* Backtracking reliably finds solutions but can be slow
* Greedy is very fast but frequently fails
* CSP performs similarly to backtracking but can benefit from heuristics

## Technologies

* Python
* Tkinter (GUI)
* Graph search techniques
* Constraint Satisfaction methods

## How to run

Clone the repository:

git clone https://github.com/juandanieltech-design/numberlink-algorithm-solver.git

Navigate to the project directory:

cd numberlink-algorithm-solver

Run the program:

python main.py
## Author

Juan Daniel Vargas
Pontificia Universidad Javeriana
