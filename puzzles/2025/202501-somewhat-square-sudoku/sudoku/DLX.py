import math
import numpy as np
import copy
import sys

sys.setrecursionlimit(10000)

CYCLIC_NUMBER = 111_111_111
candidate_excluded = [1, 3, 4, 6, 7, 8, 9][::-1]  # 倒序遍历

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

def row_number(row):
    return int("".join(str(d) for d in row))

# ========================= #
#  舞蹈链 (Dancing Links)   #
# ========================= #
class DLXNode:
    """舞蹈链的节点"""
    def __init__(self):
        self.left = self.right = self.up = self.down = self
        self.column = None

class DLXColumn(DLXNode):
    """舞蹈链的列节点"""
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.size = 0

class DancingLinks:
    """舞蹈链求解器"""
    def __init__(self, matrix):
        self.header = DLXNode()
        self.columns = []
        self.solution = []
        self.build_linked_matrix(matrix)

    def build_linked_matrix(self, matrix):
        """构建舞蹈链矩阵"""
        col_headers = [DLXColumn(i) for i in range(len(matrix[0]))]
        self.columns = col_headers

        for i, col in enumerate(col_headers):
            col.left = self.header if i == 0 else col_headers[i - 1]
            col.right = self.header if i == len(col_headers) - 1 else col_headers[i + 1]
            col.up = col.down = col
            col.size = 0

        for row in matrix:
            first_node = None
            for col_index in row:
                col = col_headers[col_index]
                node = DLXNode()
                node.column = col
                node.up = col.up
                node.down = col
                col.up.down = node
                col.up = node
                col.size += 1
                if first_node is None:
                    first_node = node
                    first_node.left = first_node.right = first_node
                else:
                    node.left = first_node.left
                    node.right = first_node
                    first_node.left.right = node
                    first_node.left = node

    def cover(self, column):
        """覆盖列"""
        column.right.left = column.left
        column.left.right = column.right
        for row in self.iterate(column.down, "down"):
            for node in self.iterate(row.right, "right"):
                node.down.up = node.up
                node.up.down = node.down
                node.column.size -= 1

    def uncover(self, column):
        """取消覆盖列"""
        for row in self.iterate(column.up, "up"):
            for node in self.iterate(row.left, "left"):
                node.column.size += 1
                node.down.up = node
                node.up.down = node
        column.right.left = column
        column.left.right = column

    def search(self):
        """DLX 递归求解"""
        if self.header.right == self.header:
            return True

        column = min(self.iterate(self.header.right, "right"), key=lambda c: c.size)
        self.cover(column)

        for row in self.iterate(column.down, "down"):
            self.solution.append(row)
            for node in self.iterate(row.right, "right"):
                self.cover(node.column)
            if self.search():
                return True
            self.solution.pop()
            for node in self.iterate(row.left, "left"):
                self.uncover(node.column)

        self.uncover(column)
        return False

    def iterate(self, node, direction):
        """遍历舞蹈链"""
        cur = node
        while cur != getattr(node, direction):
            yield cur
            cur = getattr(cur, direction)

    def solve(self):
        """执行 DLX 求解"""
        if self.search():
            return self.extract_solution()
        return None

    def extract_solution(self):
        """提取数独解"""
        solution = [[-1] * 9 for _ in range(9)]
        for row in self.solution:
            r, c, d = row.column.name // 81, (row.column.name % 81) // 9, (row.column.name % 9) + 1
            solution[r][c] = d
        return solution

# ========================= #
#       计算最大 GCD       #
# ========================= #
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

        solver = DancingLinks(np_to_list(initial_grid_np))
        solution = solver.solve()

        if solution is not None:
            row_nums = [row_number(row) for row in solution]
            overall_gcd = row_nums[0]
            for num in row_nums[1:]:
                overall_gcd = math.gcd(overall_gcd, num)

            local_max_gcd = max(local_max_gcd, overall_gcd)

            if overall_gcd > max_gcd:
                max_gcd = overall_gcd
                best_solution = solution
                best_excluded = d
                best_target = target

# ========================= #
#    输出最佳数独解         #
# ========================= #
if best_solution is not None:
    print("\n======== FINAL BEST SOLUTION ========")
    print("Optimized solution found!")
    print("Best Excluded digit:", best_excluded)
    print("Best GCD target (each row divisible by):", best_target)
    print("Max GCD found:", max_gcd)
    print("Solution grid:")
    for row in best_solution:
        print(row)
else:
    print("No solution found under the optimized constraints.")
