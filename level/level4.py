from queue import Queue, PriorityQueue
from models import agent
from models import board
class Level4:
    def construct_path(self, start, goal, come_from):
        cur = goal
        path = []
        path.append(cur)
        cur = come_from[goal]
        while cur != start:
            path.append(cur)
            cur = come_from[cur]
        return path[::-1]
    def find_path(self, agent, start, goal, board):
        come_from = {}
        q = Queue()
        q.put(start)
        visited = {}
        visited[start] = True
        while not q.empty():
            cur = q.get()
            visited[cur] = True
            if cur == goal:
                return self.construct_path(start, goal, come_from)
            successor = board.get_successor_for_agent(cur)
            for pos in successor:
                    if visited.get(pos) == None:
                        come_from[pos] = cur 
                        visited[pos] = True
                        q.put(pos)
        return []
    def bfs_for_agent(self, index, agent, board):  #find KEYS the agent can reach
        q = Queue()
        q.put(agent.start)
        visited = {}
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            if cur in board.keys:
                board.can_visit_key[board.key_number[cur]] = True
                continue
            if cur == board.goal_pos[index]:
                board.can_visit_goal[0] = True
                continue
            successors = board.get_successor_for_agent(cur)
            for pos in successors:
                    q.put(pos)
    def bfs_for_keys(self, index, agent, board): #find DOORS the key can reach
        q = Queue()
        pos = board.keys[index]
        q.put(pos)
        visited = {}
        board.successors[index] = []
        
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            
            if board.door_number.get(cur) != None:
                  
                if board.door_number.get(cur) != index:
                    board.successors[index].append(cur)
                else:
                    board.can_visit_door[cur] = True
                continue
            successors = board.get_successors(agent, cur)
            for pos in successors:
                q.put(pos)
    def bfs_for_goal(self, index, agent, board): #find DOORS the goal can reach
        q = Queue()
        q.put(board.goal_pos[index])
        visited = {}
        board.goal_successors[index] = [] # for goal, index = 0
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            if board.door_number.get(cur) != None:
                board.goal_successors[index].append(cur)
                continue
            successors = board.get_successors(agent, cur)
            for pos in successors:
                q.put(pos)
    def find_plan(self, index, can_visit_door, agent, board): #dfs
        cur = board.keys[index]
        if board.visited.get((cur, can_visit_door)) != None:
            return
        board.visited[(cur, can_visit_door)] = 1
        if can_visit_door == True and board.can_visit_key.get(index) == True:
            agent.path_plan.append(agent.pos)
            board.ok = True
            return
        for pos in board.successors[index]:
            id = board.door_number[pos]
            agent.path_plan.append(pos)
            can_visit_door = False
            if board.can_visit_door.get(pos) == True:
                can_visit_door = True
            self.find_plan(id, can_visit_door, agent, board)
            if board.ok:
                return
            agent.path_plan.pop()
        board.visited[cur] = -1
    def solve(self, agent, board):
        while True:
            for i in range(len(agent)):
                ag = agent[i]
                self.bfs_for_agent(i, ag, board)
                for j in range(len(board.keys)):
                    self.bfs_for_keys(ag, j, board)
                self.bfs_for_goal(i, agent, board)
                ag.path_plan = []
                ag.path_plan.append(board.goal_successor)
                ag.path = []
                for j in range(len(board.goal_successors[i])):
                    ag.path_plan.append(board.goal_successors[i][j])
                    can_visit_doors = False
                    if board.can_visit_door.get(board.goal_successors[i][j]) == True: 
                        can_visit_doors = True
                    self.find_plan(board.door_number[board.goal_successors[i][j]], can_visit_doors, ag, board)
                    if len(ag.path_plan) > 1:
                        break
                    ag.path_plan.pop()
                cur = ag.path_plan.pop()
                if cur != ag.start:
                    ag.path.append(ag.start)
                else:
                    cur = ag.path_plan.pop()
                    path = self.find_path(ag, ag.start, cur, board)
                    ag.path.append(path[0])
                    board[ag.start[0]][ag.start[1]][ag.start[2]] = 0
                    ag.start = cur
                    board.map[cur[0]][cur[1]][cur[2]] = -1
                    if cur == board.goal_pos[i]:
                        if i == 0:
                            return
                        # TODO: else generate new task for other agent
                    if board.key_number.get(cur):
                        agent.has_key[board.key_number[cur]] = True
                        