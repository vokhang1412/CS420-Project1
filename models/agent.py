import board
class Agent:
    start = None
    path = []
    path_plan = []
    has_key = []
    def __init__(self, start, board) -> None:
        self.start = start
        self.path.append(start)
        self.has_key = self.has_key = [False] * len(board.key_pos)
    def add_path(self, path):
        self.path.extend(path)
    def check_valid_for_agent(self, cur, board):
        if cur[1] < 0 or cur[1] >= self.rows or cur[2] < 0 or cur[2] >= self.cols or self.map[cur[0]][cur[1]][cur[2]] == -1:
            return False
        if self.door_number.get(cur) != None:
            return self.has_key[self.door_number[cur]]
        return True
    def get_successor_for_agent(self, cur):
        successors = []
        for i in range(len(self.dx)):
            pos = (cur[0], cur[1] + self.dx[i], cur[2] + self.dy[i])
            # if pos == (0, 3, 5):
            #     print(self.check_valid_for_agent(pos))
            if self.check_valid_for_agent(pos):
                successors.append(pos)
        for i in range(len(self.dx_diagonal)):
            pos = (cur[0], cur[1] + self.dx_diagonal[i], cur[2] + self.dy_diagonal[i])
            pos1 = (cur[0], cur[1] + self.dx_diagonal[i], cur[2])
            pos2 = (cur[0], cur[1], cur[2] + self.dy_diagonal[i])
            if self.check_valid_for_agent(pos) and self.check_valid_for_agent(pos1) and self.check_valid_for_agent(pos2):
                successors.append(pos)
        pos = (cur[0] + 1, cur[1], cur[2])
        if pos[0] < self.floor and self.is_up.get(cur) == True:
            successors.append(pos)
        pos = (cur[0] - 1, cur[1], cur[2])
        if pos[0] >= 0 and self.is_down.get(cur) == True:
            successors.append(pos)
        return successors
    def check_valid(self, cur):
        if cur[1] < 0 or cur[1] >= self.rows or cur[2] < 0 or cur[2] >= self.cols or self.map[cur[0]][cur[1]][cur[2]] == -1:
            return False
        return True
    def get_successors(self, cur):
        successors = []
        for i in range(len(self.dx)):
            pos = (cur[0], cur[1] + self.dx[i], cur[2] + self.dy[i])
            if self.check_valid(pos):
                successors.append(pos)
        pos = (cur[0] + 1, cur[1], cur[2])
        if pos[0] < self.floor and self.is_down.get(pos):
            successors.append(pos)
        pos = (cur[0] - 1, cur[1], cur[2])
        if pos[0] >= 0 and self.is_up.get(pos):
            successors.append(pos)
        return successors
    