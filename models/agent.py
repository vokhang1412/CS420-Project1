import board
class Agent:
    start = None
    path = None
    path_plan = []
    goal = []
    has_key = []
    def __init__(self, start, goal, board) -> None:
        self.start = start
        self.path = [start]
        self.goal = [goal]
        self.has_key = [False] * len(board.keys)
    def add_path(self, path):
        self.path.extend(path)
    