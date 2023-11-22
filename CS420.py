from collections import deque
import random

def generate_board(rows, cols):
    board = [[0 for _ in range(cols)] for _ in range(rows)]

    for _ in range(rows * cols // 5):  
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        board[row][col] = -1  

    return board

def is_valid_move(grid, x, y):
    rows, cols = len(grid), len(grid[0])
    return 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0

def is_valid_diagonal_move(grid, x, y, dx, dy):
    rows, cols = len(grid), len(grid[0])
    diagonals = [(dx, 0), (dx, dy), (0, dy)]

    for dx, dy in diagonals:
        new_x, new_y = x + dx, y + dy
        if not (0 <= new_x < rows and 0 <= new_y < cols and grid[new_x][new_y] == 0):
            return False

    return True

def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(start, [])])

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == goal:
            print("The path: ")
            print_path(grid, path)
            return path + [(x, y)]

        for dx, dy, direction in [(-1, -1, 'upleft'), (-1, 1, 'upright'), (1, -1, 'downleft'), (1, 1, 'downright')]:
            new_x, new_y = x + dx, y + dy
            if is_valid_diagonal_move(grid, x, y, dx, dy) and not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append(((new_x, new_y), path + [(x, y, direction)]))

        for dx, dy, direction in [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(grid, new_x, new_y) and not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append(((new_x, new_y), path + [(x, y, direction)]))

    return []

def print_path(grid, path):
    for step in path:
        (row, col, direction) = step
        
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if (r, c) == (row, col):
                    print("X", end=" ")
                elif grid[r][c] == 0:
                    print(".", end=" ")
                elif grid[r][c] == -1:
                    print("#", end=" ")
            print()
        print()
        print(f"Move {direction.upper()}:")
def print_final(grid, x, y):
    for r in range(len(grid)):
            for c in range(len(grid[0])):
                if (r, c) == (x, y):
                    print("X", end=" ")
                    continue
                elif grid[r][c] == 0:
                    print(".", end=" ")
                elif grid[r][c] == -1:
                    print("#", end=" ")
            print()
    print()
# Example usage:
if __name__ == "__main__":
    rows, cols = 10, 10
    grid = generate_board(rows, cols)
    # grid = [
    #     [0, 0, 0, 0, 0],
    #     [0, 0, -1, 0, 0],
    #     [0, 0, 0, -1, 0],
    #     [0, -1, 0, 0, 0],
    #     [0, 0, 0, -1, 0],
    # ]

    start = (0, 0)
    goal = (8,8)
    grid[8][8]=0
    path = bfs(grid, start, goal)

    if path:
        print_final(grid,8,8)
        print(f"Agent reached Mr. Thanh in {len(path)-1} steps.")
    else:
        print("No valid path found.")
