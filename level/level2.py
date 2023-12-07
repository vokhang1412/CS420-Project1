from queue import Queue, PriorityQueue
from models import agent
from models import board
class Level2:
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
                agent.add_path(self.construct_path(start, goal, come_from))
                return
            successor = board.get_successor_for_agent(agent, cur)
            for pos in successor:
                    if visited.get(pos) == None:
                        come_from[pos] = cur 
                        visited[pos] = True
                        q.put(pos)
    def bfs_for_agent(self, agent, board):  #find KEYS the agent can reach
        q = Queue()
        q.put(agent.start)
        visited = {}
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            if cur in board.keys:
                board.can_visit_key[0][board.key_number[cur]] = True
                continue
            successors = board.get_successor_for_agent(agent, cur)
            for pos in successors:
                q.put(pos)
            
    def bfs_for_keys(self, agent, index, board): #find DOORS the key can reach
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
            successors = board.get_successors(cur)
            for pos in successors:
                q.put(pos)
    def bfs_for_goal(self, agent, board): #find DOORS the goal can reach
        q = Queue()
        q.put(board.goal_pos[0])
        visited = {}
        board.goal_successors[0] = [] # for goal, index = 0
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            if board.door_number.get(cur) != None and agent.has_key[board.door_number[cur]] == False:
                board.goal_successors[0].append(cur)
                continue
            successors = board.get_successors(cur)
            for pos in successors:
                q.put(pos)
    def find_plan(self, index, can_visit_door, agent, board): #dfs
        cur = board.keys[index]
        if board.visited[0].get((cur, can_visit_door)) != None:
            return
        board.visited[0][(cur, can_visit_door)] = 1
        if can_visit_door == True and board.can_visit_key[0].get(index) == True:
            agent.path_plan.append(agent.start)
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
        
    def convert_path_from_plan(self, agent, board):
        cur = agent.path_plan.pop()
        if cur != agent.start:
            return
        while agent.path_plan:
            next = agent.path_plan.pop()
            if next == board.goal_pos[0]:
                self.find_path(agent, cur, next, board)
                return
            self.find_path(agent, cur, board.keys[board.door_number[next]], board)
            cur = board.keys[board.door_number[next]]
            agent.has_key[board.door_number[next]] = True
    def solve(self, board, agent):
        self.bfs_for_agent(agent, board)
        for i in range(len(board.keys)):
            self.bfs_for_keys(agent, i, board)
        self.bfs_for_goal(agent, board)
        agent.path_plan = []
        agent.path_plan.append(board.goal_pos[0])
        
        for i in range(len(board.goal_successors[0])):
            agent.path_plan.append(board.goal_successors[0][i])
            can_visit_doors = False
            if board.can_visit_door.get(board.goal_successors[0][i]) == True: 
                can_visit_doors = True
            self.find_plan(board.door_number[board.goal_successors[0][i]], can_visit_doors, agent, board)
            if len(agent.path_plan) > 1:
                break
            agent.path_plan.pop()
        self.convert_path_from_plan(agent, board)