class Agent:
    dx = [0, 0, 1, -1, 1, 1, -1, -1]
    dy = [1, -1, 0, 0, 1, -1, 1, -1]
    def __init__(self) -> None:
        self
    def get_successor(self, cur, board):
        successor = []
        for i in range(len(self.dx)):
            pos = cur
            pos.x += self.dx[i]
            pos.y += self.dy[i]
            if pos.x >= 1 and pos.x <= board.n and pos.y >= 1 and pos.y <= board.m and board[pos.x][pos.y] != -1:
                successor.append(pos);
        return successor
    def get_path(self, path):
        self.path = []
        self.path.extend(path)
    def count_heuristic(self, goal):
        self.h = max(abs(goal.x - self.cur.x), abs(goal.y - self.cur.y))
        return self.h