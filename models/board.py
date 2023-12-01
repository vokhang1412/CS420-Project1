# A Board will have the following attributes:
#     - rows
#     - cols
#     - 2D array
import agent
class Board:
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    dx_diagonal = [1, 1, -1, -1]
    dy_diagonal = [1, -1, 1, -1]
    can_visit_key = {}
    can_visit_door = {}
    is_up = {}
    is_down = {}
    goal_pos = []
    key_pos = []
    door_pos = []
    up_stairs_pos = []
    down_stairs_pos = []
    map = []
    keys = []
    key_number = {}
    door_number = {}
    successors = []
    has_key = []
    goal_successors = []
    visited = {}
    def __init__(self, floor, rows, cols, map_info, agent_pos, goal_pos, key_pos, door_pos, up_stairs_pos, down_stairs_pos) -> None:
        self.floor = floor
        self.rows = rows
        self.cols = cols
        self.keys.append((0, 0, 0))
        self.agent_pos = agent_pos
        self.goal_pos = goal_pos
        self.keys = key_pos
        self.has_key = [False] * len(key_pos)
        for i in range(len(key_pos)):
            self.key_number[key_pos[i]] = i
        self.map = map_info
        for i in range(len(up_stairs_pos)):
            self.is_up[up_stairs_pos[i]] = True
        for i in range(len(down_stairs_pos)):
            self.is_down[down_stairs_pos[i]] = True
        for i in range(len(door_pos)):
            self.door_number[door_pos[i][1]] = door_pos[i][0]
        for i in range(len(key_pos) + 1):
            self.successors.append([])
        for i in range(len(goal_pos)):
            self.goal_successors.append([])
            
    def check_valid_for_agent(self, cur, agent):
        if cur[1] < 0 or cur[2] >= self.rows or cur.y < 0 or cur.y >= self.cols or self.map[cur[0]][cur[1]][cur[2]] == -1:
            return False
        if self.door_number[cur] >= 0:
            return self.has_key[self.door_number[cur]]
        return True
    def get_successor_for_agent(self, cur, agent):
        successors = []
        for i in range(len(self.dx)):
            pos = (cur[0], cur[1] + self.dx[i], cur[2] + self.dy[i])
            if self.check_valid_for_agent(pos, agent):
                successors.append(pos)
        for i in range(len(self.dx_diagonal)):
            pos = (cur[0], cur[1] + self.dx_diagonal[i], cur[2] + self.dy_diagonal[i])
            pos1 = (cur[0], cur[1] + self.dx_diagonal[i], cur[2])
            pos2 = (cur[0], cur[1], cur[2] + self.dy_diagonal[i])
            if self.check_valid_for_agent(pos, agent) and self.check_valid_for_agent(pos1, agent) and self.check_valid_for_agent(pos2, agent):
                successors.append(pos)
        pos = (cur[0] + 1, cur[1], cur[2])
        if pos[0] < self.floor and self.is_up[pos]:
            successors.append(pos)
        pos = (cur[0] - 1, cur[1], cur[2])
        if pos[0] >= 0 and self.is_down[pos]:
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
        if pos[0] < self.floor and self.is_down[pos]:
            successors.append(pos)
        pos = (cur[0] - 1, cur[1], cur[2])
        if pos[0] >= 0 and self.is_up[pos]:
            successors.append(pos)
        return successors