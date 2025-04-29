import math
import numpy as np
import copy
import sys

sys.setrecursionlimit(10000)

CYCLIC_NUMBER = 111_111_111
candidate_excluded = [1, 3, 4, 6, 7, 8, 9][::-1]  

def factors(n):
    result = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            result.add(i)
            result.add(n // i)
    return sorted(result, reverse=True)

def np_to_list(grid_np):
    return [list(row) for row in grid_np]

initial_grid_np = np.array([
    [-1, -1, -1, -1, -1, -1, -1, 2, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 5],
    [-1,  2, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1,  0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1,  2, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1,  0, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1,  2, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1,  5, -1, -1]
], dtype=int)
initial_grid = np_to_list(initial_grid_np)

def is_valid(grid, r, c, num, allowed):
    if num not in allowed:
        return False
    for j in range(9):
        if grid[r][j] == num:
            return False
    for i in range(9):
        if grid[i][c] == num:
            return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if grid[i][j] == num:
                return False
    return True

def row_number(row):
    return int("".join(str(d) for d in row))

solution_found = None

def solve_sudoku_optimized(grid, allowed, target, cell=0):
    global solution_found
    if solution_found is not None:
        return
    if cell == 81:
        solution_found = copy.deepcopy(grid)
        return
    r, c = divmod(cell, 9)
    if grid[r][c] != -1:
        if c == 8 and row_number(grid[r]) % target != 0:
            return
        solve_sudoku_optimized(grid, allowed, target, cell + 1)
        return
    for num in allowed:
        if is_valid(grid, r, c, num, allowed):
            grid[r][c] = num
            if c == 8 and row_number(grid[r]) % target != 0:
                grid[r][c] = -1
                continue
            solve_sudoku_optimized(grid, allowed, target, cell + 1)
            if solution_found is not None:
                return
            grid[r][c] = -1

best_solution = None
best_excluded = None
best_target = None
max_gcd = 0

for d in candidate_excluded:
    allowed = set(range(10)) - {d}
    valid_candidate = all(initial_grid[i][j] in allowed for i in range(9) for j in range(9) if initial_grid[i][j] != -1)
    if not valid_candidate:
        continue

    max_value = CYCLIC_NUMBER * (45 - d)
    cand_targets = factors(max_value)

    local_max_gcd = 0

    for target in cand_targets:
        if target < max_gcd:  
            break  

        solution_found = None
        grid_copy = copy.deepcopy(initial_grid)
        solve_sudoku_optimized(grid_copy, allowed, target, 0)

        if solution_found is not None:
            row_nums = [row_number(row) for row in solution_found]
            overall_gcd = row_nums[0]
            for num in row_nums[1:]:
                overall_gcd = math.gcd(overall_gcd, num)

            local_max_gcd = max(local_max_gcd, overall_gcd)

            print("\nFound a solution!")
            print(f"Excluded digit: {d}")
            print(f"GCD target (each row divisible by): {target}")
            print(f"Current GCD: {overall_gcd}")
            print("Solution grid:")
            for row in solution_found:
                print(row)
            print(f"Row numbers: {row_nums}")
            print("-" * 50)

            if overall_gcd > max_gcd:
                max_gcd = overall_gcd
                best_solution = solution_found
                best_excluded = d
                best_target = target


if best_solution is not None:
    print("\n======== FINAL BEST SOLUTION ========")
    print("Optimized solution found!")
    print("Best Excluded digit:", best_excluded)
    print("Best GCD target (each row divisible by):", best_target)
    print("Max GCD found:", max_gcd)
    print("Solution grid:")
    for row in best_solution:
        print(row)
    row_nums = [row_number(row) for row in best_solution]
    print("Row numbers:", row_nums)
else:
    print("No solution found under the optimized constraints.")
