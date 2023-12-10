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
            successor = board.get_successor_for_agent(agent, cur)
            for pos in successor:
                    if visited.get(pos) == None:
                        come_from[pos] = cur 
                        visited[pos] = True
                        q.put(pos)
        return []
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
    def find_plan(self, index, agent, board): #dfs
        q = Queue()
        has_key = agent.has_key
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
                if cur == board.goal_pos[index]:
                    return plan[cur]                            
                if board.key_number.get(cur) != None:
                    if tmp_has_key[board.key_number[cur]] == False:
                        tmp_has_key[board.key_number[cur]] = True
                        plan[cur].append(cur)
                if board.door_number.get(cur) != None and agent.has_key[board.door_number[cur]] == False:
                    if has_key[board.door_number[cur]] == False:
                        door.put(cur)
                        continue
                    else:
                        if board.keys[board.door_number[cur]] not in plan[cur]:
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
        while True:
            cnt = 0
            for i in range(len(agent)):
                ag = agent[i]
                path_plan = self.find_plan(i, ag, board)
                # if i == 0: print(path_plan)
                if len(path_plan) > 0:
                    path_plan.append(board.goal_pos[i])
                    path = self.find_path(ag, path_plan[0], path_plan[1], board)
                    # print(path)
                    pos = path[0]
                    ag.path.append(pos)
                    board.map[ag.start[0]][ag.start[1]][ag.start[2]] = 0
                    board.map[pos[0]][pos[1]][pos[2]] = -2
                    if pos == board.goal_pos[i]:
                        if i == 0:
                            totalscore = 100 - (len(ag.path) - board.floor*(abs(ag.start[1] - board.goal_pos[0][1]) + abs(ag.start[2] - board.goal_pos[0][2])))
                            if totalscore < 0:
                                totalscore = 0
                            if totalscore > 100:
                                totalscore = 100
                            print("Total Score: ",totalscore)
                            return
                        board.goal_pos[i] = self.generate_new_task(board)
                        ag.has_key = [False] * len(board.keys)
                    ag.start = pos
                    if board.key_number.get(pos) != None:
                        ag.has_key[board.key_number[pos]] = True
                else:
                    cnt+= 1
                    ag.path.append(ag.start)
                ag.goal.append(board.goal_pos[i])
            if cnt == len(agent):
                for i in range(len(agent)):
                    agent[i].path = []
                    agent[i].goal = []
                return

    # random new task for other agent
    def generate_new_task(self, board):
        import random
        while True:
            i_rad = random.randint(0, len(board.map) - 1)
            j_rad = random.randint(0, len(board.map[0]) - 1)
            k_rad = random.randint(0, len(board.map[0][0]) - 1)
            new_goal = (i_rad, j_rad, k_rad)
            if board.map[i_rad][j_rad][k_rad] != -1 and new_goal not in board.goal_pos and new_goal not in board.keys and board.door_number.get(new_goal) == None and new_goal not in board.up_stairs_pos and new_goal not in board.down_stairs_pos:
                return (i_rad, j_rad, k_rad)            
        