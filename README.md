# Nonogram Solver

a solver for the popular puzzle game [Nonogram](https://de.puzzle-nonograms.com/?size=3).
This solver utilizes the z3 SAT-solver

## Usage

```bash
./main.py ./levels/test_hard.csv 
```

Output:

```
X X X O O O O O O X X X O O X X X O X O 
X X X X O O O O O X X X O O O X X X X O 
O X X X X X O X X X X X X X X X X O O O 
O X X X X X X X X X O X X O O O O O O X 
O X X X X X O X X X O O X O O O O O O O 
O X X X X X X X X X X O O O O O O O O O 
X O X X X X X X X O O O O O O O O O X O 
X O X O O X X X O O X O X O O O O O X X 
X O O O O O O X X O O X X X O O O O X X 
X O O O O O O X X O O O X X O O O O O O 
X X X O O O X X X X O O X X O O O O O X 
X X X X X O O O O O O O X O O X O O O X 
X X X X X X O O O O O O X O O X O O O X 
X X X X X X O O O O O X X O O X X O O O 
O X X X X X X X X X X O O O X X X O O O 
O O O O X X X X X X O O O X X X X O O O 
X X X X X X X X X X O O O X X X O O O O 
X X X O X X X X X X O X X X X O O O O O 
O X X X O X X X X O O X X X O O O O O O 
O O O O O X X X O O O X X X O O O O O O 
```
