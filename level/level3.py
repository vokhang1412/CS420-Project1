from queue import Queue, PriorityQueue
from models import agent
from models import board
class Level3:
    def construct_path(self, start, goal, come_from):
        cur = goal
        path = []
        path.extend(cur)
        cur = come_from[goal]
        while cur != start:
            path.extend(cur)
            cur = come_from[goal]
        return path[::-1]
    def find_path(self, agent, start, goal, board):
        dist = {}
        come_from = {}
        pq = PriorityQueue()
        pq.put((max(start.x - goal.x, start.y - goal.y), start))
        dist[start] = 0
        while not pq.empty():
            f, cur = pq.get()
            g = f - max(abs(cur.x - goal.x), abs(cur.y - goal. y))
            if g != dist[cur]:
                continue
            if cur == goal:
                agent.add_path(self.construct_path(start, goal, come_from))
                return
            successor = board.get_successor_for_agent(cur, agent)
            for pos in successor:
                if board.check_valid(pos, agent) and (pos not in dist or dist[pos] > dist[cur] + 1):
                    come_from[pos] = cur 
                    dist[pos] = dist[cur] + 1
                    pq.put((max(abs(pos.x - goal.x), abs(pos.y - goal.y)) + dist[pos], pos))
    def bfs_for_agent(self, agent, board):  #find KEYS the agent can reach
        q = Queue()
        q.put(agent.pos)
        visited = {}
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            if cur in board.keys:
                board.can_visit_key[board.key_number[cur]] = True
                continue
            if cur == board.goal_pos[0]:
                board.can_visit_key[0] = True
                continue
            successors = board.get_successors(cur)
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
            if board.door_number.get(cur):
                if board.door_number.get(cur) != index:
                    board.successors[index].append(cur)
                else:
                    board.can_visit_door[cur] = True
                continue
            successors = board.get_successors(cur)
            for pos in successors:
                q.put(pos)
    def bfs_for_goal(self, board): #find DOORS the goal can reach
        q = Queue()
        q.put(board.goal_pos[0])
        visited = {}
        board.goal_successors[0] = [] # for goal, index = 0
        while not q.empty():
            cur = q.get()
            if visited.get(cur):
                continue
            visited[cur] = True
            if board.door_number.get(cur):
                board.goal_successors[0].append(cur)
                continue
            successors = board.get_successors(cur)
            for pos in successors:
                q.put(pos)
    def find_plan(self, index, agent, board): #dfs
        cur = board.keys[index]
        if board.visited.get(cur) == None:
            return
        board.visited[cur] = 1
        if index == 0:
            if board.can_visit_key[0]:
                agent.path_plan.append(agent.pos)
                board.ok = True
                return
        elif board.can_visit_door[cur] and board.can_visit_key[board.keys[index]]:
            agent.path_plan.append(agent.pos)
            board.ok = True
            return
        for pos in board.successors[index]:
            id = board.door_number(pos)
            agent.path_plan.append(pos)
            board.find_plan(id, agent, board)
            if board.ok:
                return
            agent.path_plan.pop()
        board.visited[cur] = -1
        
    def convert_path_from_plan(self, agent, board):
        cur = agent.path_plan.pop()
        if cur != agent.pos:
            return
        while not agent.path_plan.empty():
            next = agent.path_plan.pop()
            if board.is_goal(next):
                self.find_path(agent, cur, next, board)
                return
            self.find_path(agent, cur, board.keys[board.door_number[next]], board)
            cur = board.keys[board.door_number[next]]
            board.has_key[board.door_number[next]] = True
            self.find_path(agent, cur, next, board)
            cur = next
    def solve(self, board, agent):
        self.bfs_for_agent(agent, board)
        for i in range(len(board.keys)):
            self.bfs_for_keys(agent, i, board)
        self.bfs_for_goal(board)
        agent.path_plan = []
        agent.path_plan.append(board.goal_pos[0])
        self.find_plan(0, agent, board)
        self.convert_path_from_plan(agent, board)