class Agent:
    start = (0, 0)
    goal = (0, 0)
    path = []
    def __init__(self, pos) -> None:
        self.pos = pos
        self.path.append(pos)
    def add_path(self, path):
        self.path.extend(path)