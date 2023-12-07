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
    def bfs_for_agent(self, index, agent, board):  #find KEYS the agent can reach
        q = Queue()
        q.put(agent.start)
        
        visited = {}
        board.can_visit_key[index].clear()
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            # if agent.start == (0, 15, 7):
            #     print(cur)
            if cur == board.goal_pos[index]:
                board.can_visit_goal[index] = True
                continue
            
            if cur in board.keys and agent.has_key[board.key_number[cur]] == False:
                # if agent.start == (0, 15, 7):
                    # print(agent.has_key)
                    # print(cur)
                board.can_visit_key[index][board.key_number[cur]] = True
                continue
            successors = board.get_successor_for_agent(agent, cur)
            for pos in successors:
                # if agent.start == (0, 15, 7):
                #     print(pos)
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
            if board.door_number.get(cur) != None and agent.has_key[board.door_number[cur]] == False:
                if board.door_number.get(cur) != index:
                    board.successors[index].append(cur)
                else:
                    board.can_visit_door[cur] = True  
                continue
            successors = board.get_successors(cur)
            for pos in successors:
                q.put(pos)
    def bfs_for_goal(self, index, agent, board): #find DOORS the goal can reach
        q = Queue()
        q.put(board.goal_pos[index])
        visited = {}
        board.goal_successors[index] = []
        while not q.empty():
            cur = q.get()
            if visited.get(cur) != None:
                continue
            visited[cur] = True
            if board.door_number.get(cur) != None and agent.has_key[board.door_number[cur]] == False:
                board.goal_successors[index].append(cur)
                continue
            successors = board.get_successors(cur)
            for pos in successors:
                q.put(pos)
    def find_plan(self, index, agent_index, can_visit_door, agent, board): #dfs
        cur = board.keys[index]
        # if agent_index == 0 and agent.start == (0, 15, 7) and cur == (0, 11, 8): 
            # print(cur)
            # print(can_visit_door)
            # print(board.can_visit_key[agent_index].get(index))
        if board.visited[agent_index].get((cur, can_visit_door)) != None:
            return
        board.visited[agent_index][(cur, can_visit_door)] = 1
        if can_visit_door == True and board.can_visit_key[agent_index].get(index) == True:
            agent.path_plan.append(agent.start)
            board.ok = True
            return
        for pos in board.successors[index]:
            id = board.door_number[pos]
            agent.path_plan.append(pos)
            can_visit_door = False
            if board.can_visit_door.get(pos) == True:
                can_visit_door = True
            self.find_plan(id, agent_index, can_visit_door, agent, board)
            if board.ok:
                return
            agent.path_plan.pop()
    def solve(self, board, agent):
        # print(board.goal_pos)
        # print(board.agent_pos)
        # agent[1].start = (0, 4, 4)
        # agent[1].has_key[board.key_number[(0, 4, 4)]] = True
        # board.goal_pos[1] = (0, 3, 5)
        # print(board.key_number)
        # for i in range(len(agent)):
        #     print(agent[i].path)
        while True:
            for i in range(len(agent)):
                self.bfs_for_agent(i, agent[i], board)
                board.can_visit_door.clear()
                for j in range(len(board.keys)):
                    self.bfs_for_keys(j, agent[i], board)
                # if i == 0:
                #     for j in range(len(board.keys)):
                #         print(board.successors[j])
                self.bfs_for_goal(i, agent[i], board)
                # if i == 0: print(board.goal_successors[i])
                board.ok = False
                agent[i].path_plan = []
                agent[i].path_plan.append(board.goal_pos[i])
                if board.can_visit_goal[i] == False:
                    for j in range(len(board.goal_successors[i])):
                        agent[i].path_plan.append(board.goal_successors[i][j])
                        can_visit_doors = False
                        if board.can_visit_door.get(board.goal_successors[i][j]) == True: 
                            can_visit_doors = True
                        self.find_plan(board.door_number[board.goal_successors[i][j]], i, can_visit_doors, agent[i], board)
                        if len(agent[i].path_plan) > 2:
                            break
                        agent[i].path_plan.pop()
                else:
                    agent[i].path_plan.append(agent[i].start)
                # print(agent[i].path_plan)
                cur = agent[i].path_plan.pop()
                # print(agent[i].has_key)
                # print(agent[i].start)
                # print(cur)
                if cur != agent[i].start:
                    agent[i].path.append(agent[i].start)
                else:
                    cur = agent[i].path_plan.pop()
                    while cur != board.goal_pos[i] and agent[i].path_plan and board.keys[board.door_number[cur]] == agent[i].start:
                        cur = agent[i].path_plan.pop()
                    if cur != board.goal_pos[i]:
                        cur = board.keys[board.door_number[cur]]
                    path = self.find_path(agent[i], agent[i].start, cur, board)
                    # if agent[i].start == (0, 4, 4):
                    #     print(cur)
                    # print(path)
                    agent[i].path.append(path[0])
                    board.map[agent[i].start[0]][agent[i].start[1]][agent[i].start[2]] = 0
                    agent[i].start = path[0]
                    board.map[path[0][0]][path[0][1]][path[0][2]] = -1
                    if agent[i].start == board.goal_pos[i]:
                        if i == 0:
                            print(agent[i].path)
                            return
                        # TODO: else generate new task for other agent
                        else:
                            board.goal_pos[i] = self.generate_new_task(board)
                            agent[i].has_key = [False] * len(board.keys)
                    # print(agent[i].start)
                    # if agent[i].start == (0, 4, 4): print(board.key_number.get(agent[i].start))
                    if board.key_number.get(agent[i].start) != None:
                        # if agent[i].start == (0, 4, 4):
                        #     print(agent[i].start)
                        agent[i].has_key[board.key_number[agent[i].start]] = True
                board.visited[i].clear()
                board.can_visit_goal[i] = False
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
        