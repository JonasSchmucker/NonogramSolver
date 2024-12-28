#!/usr/bin/python3

from z3 import *
import argparse
import csv

def read_level(filename):
    # Open the file
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                # int_row = [int(item) if item is not "" else -1 for item in row]  # Convert each item in the row to an integer
                int_row = [-1 if item.strip() == "" or item == " " or item == "\t" else int(item) for item in row]  # Convert each item in the row to an integer
                data.append(int_row)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(-1)

def handle_args():
    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle using Z3 solver.")
    parser.add_argument("file", type=str, help="Path to the input file")

    # Parse command-line arguments
    return parser.parse_args()

def get_neighbors(matrix, row, col):
    # List of relative positions of the 8 neighbors
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
        ( 0, -1), (0, 0) , ( 0, 1),   # Left, Self, Right
        ( 1, -1), ( 1, 0), ( 1, 1)    # Bottom-left, Bottom, Bottom-right
    ]
    
    # List to store valid neighbors
    valid_neighbors = []
    
    # Iterate over each relative position
    for dr, dc in neighbors:
        new_row, new_col = row + dr, col + dc
        
        # Check if the new position is within bounds of the matrix
        if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
            valid_neighbors.append(matrix[new_row][new_col])
    
    return valid_neighbors

def add_nonogram_line_single_constraint(solver: Solver, vars, constraint, var_string):
    or_list = []
    constraint_var = Int(var_string)
    for start_index in range(len(vars) - constraint + 1):
        and_list = []
        and_list.append(start_index == constraint_var)
        if start_index != 0:
            and_list.append(Not(vars[start_index - 1]))
        for i in range(constraint):
            and_list.append(vars[start_index + i])
        if (start_index + constraint) != len(vars):
            and_list.append(Not(vars[start_index + constraint]))
        or_list.append(And(and_list))
    solver.add(Or(or_list))
    return constraint_var

def add_nonogram_line_constraint(solver: Solver, vars, line, var_string_prefix):
    last_constraint_var = -1
    constraint_sum = 0
    for constraint_id, constraint in enumerate(line):
        if constraint == -1: 
            continue
        constraint_sum += constraint
        this_constraint_var = add_nonogram_line_single_constraint(solver, vars, constraint, var_string_prefix + "_" + str(constraint_id))
        solver.add(last_constraint_var < this_constraint_var)
        last_constraint_var = this_constraint_var + constraint
    solver.add(sum(If(var, 1, 0) for var in vars) == constraint_sum)



def solve_level(level):
    (rows, columns) = (level[:int(len(level) / 2)], level[int(len(level) / 2):])
    solver = Solver()
    level_size = len(rows)
    vars = [[Bool(f"var_{i}_{o}") for i in range(level_size)] for o in range(level_size)]

    # add row constraints
    for row_index, row in enumerate(rows):
        add_nonogram_line_constraint(solver, vars[row_index], row, "row_" + str(row_index))

    # add column constraints
    for column_index, column in enumerate(columns):
        column_vars = [row[column_index] for row in vars]
        add_nonogram_line_constraint(solver, column_vars, column, "column_" + str(column_index))


    # Check satisfiability
    if solver.check() == sat:
        model = solver.model()
        return [[model[square] for square in row] for row in vars]  # Return the values of the variables
    else:
        print("No solution exists")
        exit(-1)

def main():
    args = handle_args()

    level = read_level(args.file)
    if len(level) % 2 != 0:
        print("Invalid level format ")
        exit(-1)
        
    """
    for row in level:
        for square in row:
            print(square if square != -1 else " ", end=" ")
        print()
    """
    print()
    
    solution = solve_level(level)
    for row in solution:
        for square in row:
            print("X" if square else "O", end=" ")
        print()

if __name__ == "__main__":
    main()