from queue import Queue, PriorityQueue
from models.agent import Agent
from models.board import Board
class Level2:
    def construct_path(self, start, goal, come_from):
        cur = goal
        path = []
        path.extend(cur)
        while cur != start:
            cur = come_from[goal]
            path.extend(cur)
        return path[::-1]
    def find_path(self, agent, start, goal, board):
        path = []
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
            successor = agent.get_successor(cur, board)
            for pos in successor:
                if board.check_valid(agent, pos) and (pos not in dist or dist[pos] > dist[cur] + 1):
                    pq.put((max(abs(pos.x - goal.x), abs(pos.y - goal. y)), pos))
                    come_from[pos] = cur 
                    dist[pos] = dist[cur] + 1
    def bfs_for_agent(self, agent, board):  #find KEYS the agent can reach
        q = Queue()
        q.put(agent.pos)
        while not q.empty():
            cur = q.get()
            if visited[cur]:
                continue
            visited[cur] = True
            if board.is_key(cur):
                self.can_visit_key[board.key_number(cur)] = True
                continue
            if board.is_goal(cur):
                self.can_visit_goal[board.key_number(cur)] = True
                continue
            successors = agent.get_successor(cur, board)
            for pos in successor:
                    q.put(pos)
            
    def bfs_for_keys(self, agent, index, board): #find DOORS the key can reach
        q = Queue()
        q.put(index)
        self.successors[index] = [] # for keys, index always > 0
        while not q.empty():
            cur = q.get()
            if visited[cur]:
                continue
            visited[cur] = True
            if board.is_door(cur):
                self.can_visit_key[board.key_number(cur)] = True
                if board.door_number[cur] != index:
                    self.successors[index].append(cur)
                else:
                    self.can_visit_door[cur] = True
                continue
            successors = agent.get_successor(cur, board)
            for pos in successors:
                q.put(pos)
    def bfs_for_goal(self, board): #find DOORS the goal can reach
        q = Queue()
        q.put(board.goal)
        self.successors[0] = [] # for goal, index = 0
        while not q.empty():
            cur = q.get()
            if visited[cur]:
                continue
            visited[cur] = True
            if board.is_door(cur):
                self.successors[0].append(cur)
                continue
            successors = agents.get_successor(cur, board)
            for pos in successors:
                q.put(pos)
    def find_plan(self, index, agent, board): #dfs
        cur = self.position[index]
        if self.visited[cur] != 0:
            return
        self.visited[cur] = 1
        if index == 0:
            if self.goal_reachable:
                agent.path_plan.append(agent.pos)
                self.ok = True
                return
        elif self.can_visit_door[cur] and self.can_visit_key[board.keys[index]]:
            agent.path_plan.append(agent.pos)
            self.ok = True
            return
        for pos in self.successors[index]:
            id = board.door_number(pos)
            agent.path_plan.append(pos)
            self.find_plan(id, agent, board)
            if self.ok:
                return
            agent.path_plan.pop()
        self.visited[cur] = -1
        
    def convert_path_from_plan(self, agent, board):
        cur = agent.path_plan.pop()
        if cur != agent.pos:
            return
        while not agent.path_plan.empty():
            next = agent.path_plan.pop()
            if board.is_goal(next):
                self.find_path(agent, cur, next, board)
                return
            self.find_path(agent, cur, self.position[board.door_number[next]], board)
            cur = self.find_path(agent, cur, self.position[board.door_number[next]], board)
            self.find_path(agent, cur, next, board)
            cur = next
    def solve(self, board, agent):
        self.bfs_for_agent(agent)
        for i in len(board.keys):
            self.bfs_for_keys(agent, i, board)
        self.bfs_for_goal(board)
        self.path_plan = []
        self.path_plan.append(board.goal)
        self.find_plan(0, agent, board)
        self.convert_path_from_plan(self, agent, board)