import numpy as np
import io
import sys
import itertools

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def solve_sudoku():
    # Initial grid: -1 indicates an empty cell.
    initial_grid = np.array([
        [-1, -1, -1, -1, -1, -1, -1, 2, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 5],
        [-1, 2, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 0, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, 2, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, 0, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 2, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, 5, -1, -1]
    ], dtype=int)

    used_digits = set(range(9))  # Valid digits: 0 through 8.
    seen_solutions = set()       # To store unique middle row strings of solutions.

    # Function to get box index (3x3 subgrid) given row and column.
    def get_box(row, col):
        return (row // 3) * 3 + (col // 3)

    # Preprocess the fixed digits in rows, columns, and boxes.
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty_cells = []  # List of empty cell positions, used for MRV heuristic.
    for row in range(9):
        for col in range(9):
            val = initial_grid[row][col]
            if val != -1:
                rows[row].add(val)
                cols[col].add(val)
                boxes[get_box(row, col)].add(val)
            else:
                empty_cells.append((row, col))
    
    # Divisibility check: convert the row (list of digits) into an integer and test divisibility by 999.
    def is_row_valid(row_nums):
        num = int(''.join(map(str, row_nums)))
        return num % 37 == 0

    # Precompute valid completions for a row given its clues.
    def generate_candidates_for_row(row_clues):
        fixed_positions = {i: digit for i, digit in enumerate(row_clues) if digit != -1}
        used_in_row = set(fixed_positions.values())
        all_digits = set(range(9))
        free_positions = [i for i in range(9) if i not in fixed_positions]
        available_digits = list(all_digits - used_in_row)
        
        candidates = []
        for perm in itertools.permutations(available_digits, len(free_positions)):
            candidate = list(row_clues)
            for pos, digit in zip(free_positions, perm):
                candidate[pos] = digit
            # The candidate row is guaranteed to have 9 digits.
            if is_row_valid(candidate):
                candidates.append(tuple(candidate))
        return candidates

    # Precompute candidate rows for each row index based on initial clues, stored as sets for fast lookup.
    precomputed_candidates = {}
    for i in range(9):
        row_clues = list(initial_grid[i])
        # Convert the candidate list into a set.
        precomputed_candidates[i] = set(generate_candidates_for_row(row_clues))

    # Get the most constrained empty cell (MRV heuristic).
    def get_mrv_cell():
        min_candidates = 10
        best_cell = None
        for (row, col) in empty_cells:
            if initial_grid[row][col] == -1:
                box = get_box(row, col)
                candidates = used_digits - (rows[row] | cols[col] | boxes[box])
                num_candidates = len(candidates)
                if num_candidates < min_candidates:
                    min_candidates = num_candidates
                    best_cell = (row, col)
        return best_cell

    # Global validation: check if every row is divisible by 999 and all 3x3 boxes are complete.
    def is_valid_solution():
        for row in range(9):
            if not is_row_valid(initial_grid[row]):
                return False
        for box_idx in range(9):
            box_row = (box_idx // 3) * 3
            box_col = (box_idx % 3) * 3
            box_nums = set()
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    box_nums.add(initial_grid[r][c])
            if box_nums != used_digits:
                return False
        return True

    # Backtracking search with MRV heuristic and strict constraint checking.
    def backtrack():
        cell = get_mrv_cell()
        if not cell:
            # All cells are filled; check complete solution.
            if is_valid_solution():
                # Additionally, verify each row matches one of its precomputed candidates.
                valid = True
                for i in range(9):
                    if tuple(initial_grid[i]) not in precomputed_candidates[i]:
                        valid = False
                        break
                if valid:
                    middle_row_str = ''.join(map(str, initial_grid[4]))
                    if middle_row_str not in seen_solutions:
                        seen_solutions.add(middle_row_str)
                        print("Valid solution found:")
                        for row in initial_grid:
                            print(''.join(map(str, row)))
                        print(f"Middle row value: {middle_row_str}")
                        print("------------------------")
            return

        row, col = cell
        box = get_box(row, col)
        candidates = used_digits - (rows[row] | cols[col] | boxes[box])
        for num in sorted(candidates):
            # Place candidate number.
            initial_grid[row][col] = num
            rows[row].add(num)
            cols[col].add(num)
            boxes[box].add(num)

            # If the row is complete, check against precomputed candidates (using set membership).
            current_row = list(initial_grid[row])
            if -1 not in current_row:
                if tuple(current_row) not in precomputed_candidates[row]:
                    # Completed row doesn't match precomputed valid candidates, so backtrack.
                    initial_grid[row][col] = -1
                    rows[row].remove(num)
                    cols[col].remove(num)
                    boxes[box].remove(num)
                    continue
            
            backtrack()  # Recurse.

            # Undo the assignment.
            initial_grid[row][col] = -1
            rows[row].remove(num)
            cols[col].remove(num)
            boxes[box].remove(num)

    backtrack()

    if not seen_solutions:
        print("No valid solution found.")

solve_sudoku()
