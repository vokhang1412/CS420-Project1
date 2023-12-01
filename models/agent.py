class Agent:
    path = []
    def __init__(self, pos) -> None:
        self.pos = pos
        self.path.append(pos)
    def add_path(self, path):
        self.path.extend(path)