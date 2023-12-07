import board
class Agent:
    start = None
    path = None
    path_plan = []
    has_key = []
    def __init__(self, start, board) -> None:
        self.start = start
        self.path = [start]
        self.has_key = [False] * len(board.keys)
    def add_path(self, path):
        self.path.extend(path)
    