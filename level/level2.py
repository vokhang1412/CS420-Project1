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
    def merge(self, arrA, arrB):
        a = 0
        b = 0
        arr = []
        m = {}
        while a < len(arrA) and b < len(arrB):
            if m.get(arrA[a]) == None:
                m[arrA[a]] = True
                arr.append(arrA[a])
            if m.get(arrB[b]) == None:
                m[arrB[b]] = True
                arr.append(arrB[b])
            a += 1
            b += 1
        while a < len(arrA):
            if m.get(arrA[a]) == None:
                arr.append(arrA[a])
                m[arrA[a]] = True
            a += 1
        while b < len(arrB):
            if m.get(arrB[b]) == None:
                m[arrB[b]] = True
                arr.append(arrB[b])
            b += 1
        return arr
    def find_plan(self, agent, board): #dfs
        q = Queue()
        has_key = [False] * len(board.keys)
        plan = {}
        plan[agent.start] = [agent.start]
        q.put(agent.start)
        while True:
            tmp_has_key = has_key.copy()
            door = Queue()
            ok = False
            while not q.empty():
                cur = q.get()
                if cur == agent.start:
                    ok = True
                if cur == board.goal_pos[0]:
                    return plan[cur]                            
                if board.key_number.get(cur) != None:
                    if tmp_has_key[board.key_number[cur]] == False:
                        tmp_has_key[board.key_number[cur]] = True
                        plan[cur].append(cur)
                if board.door_number.get(cur) != None:
                    if has_key[board.door_number[cur]] == False:
                        door.put(cur)
                        continue
                    else:
                        arr = plan[cur]
                        if board.keys[board.door_number[cur]] not in arr:
                            plan[cur] = self.merge(plan[cur], plan[board.keys[board.door_number[cur]]])
                        ok = True
                for pos in board.get_successors(cur):
                    if plan.get(pos) == None:
                        plan[pos] = plan[cur].copy()
                        q.put(pos)
            if not ok:
                break
            has_key = tmp_has_key
            if door.empty():
                break
            while not door.empty():
                q.put(door.get())
        return []
        
    def solve(self, board, agent):
        board.map[agent.start[0]][agent.start[1]][agent.start[2]] = 0
        path_plan = self.find_plan(agent, board)
        if len(path_plan) > 0:
            path_plan.append(board.goal_pos[0])
            for i in range(1, len(path_plan), 1):
                self.find_path(agent, path_plan[i - 1], path_plan[i], board)
                if board.key_number.get(path_plan[i]) != None:
                    agent.has_key[board.key_number[path_plan[i]]] = True