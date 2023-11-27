from queue import Queue, PriorityQueue
class Level1:
    def __init__(self, map_info):
        self.map_info=map_info
    def is_valid_move(pos, map_info):
        x, y = pos
        return 0 <= x < len(map_info) and 0 <= y < len(map_info[0]) and map_info[x][y] == 0

    def is_valid_diagonal_move(self, grid, x, y, a, b):
        diagonals = [(a, 0), (a, b), (0, b)]

        for dx, dy in diagonals:
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < len(self.map_info) and 0 <= new_y < len(self.map_info[0]) and grid[new_x][new_y] == 0):
                return False

        return True

    def get_neighbors(self,pos,grid):
        x, y = pos
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        neighbors_diagonal = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        neighbor=[]
        for nei in neighbors_diagonal:
            if self.is_valid_diagonal_move(grid, x,y,nei[0]-x,nei[1]-y):
                neighbor.append(nei)
        for nei in neighbors:
            if self.is_valid_move(nei,grid):
                neighbor.append(nei)
        return neighbor
    def bfs(self,map_info, agent):
        start = agent.start
        goal = agent.goal
        visited = set()
        queue = Queue()
        queue.put(start)
        came_from = {}

        while not queue.empty():
            current = queue.get()

            if current == goal:
                print("Path found")
                agent.path = self.reconstruct_path(came_from, start, goal)
                return agent.path

            for neighbor in self.get_neighbors(current, map_info):
                if neighbor not in visited:
                    queue.put(neighbor)
                    visited.add(neighbor)
                    came_from[neighbor] = current

        return None

    def dfs(self, map_info, agent):
        start = agent.start
        goal = agent.goal
        visited = set()
        stack = [start]
        came_from = {}

        while stack:
            current = stack.pop()

            if current == goal:
                agent.path = self.reconstruct_path(came_from, start, goal)
                return agent.path

            if current not in visited:
                visited.add(current)

                neighbors = self.get_neighbors(current, map_info)
                stack.extend(neighbors)
                for neighbor in neighbors:
                    came_from[neighbor] = current

        return None

    def ucs(self, map_info, agent):
        start = agent.start
        goal = agent.goal
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while not priority_queue.empty():
            cost, current = priority_queue.get()

            if current == goal:
                agent.path = self.reconstruct_path(came_from, start, goal)
                return agent.path

            for neighbor in self.get_neighbors(current, map_info):
                new_cost = cost + 1  

                if neighbor not in visited or new_cost < cost_so_far.get(neighbor, float('inf')):
                    priority_queue.put((new_cost, neighbor))
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    visited.add(neighbor)

        return None

    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def astar(self, map_info, agent):
        start = agent.start
        goal = agent.goal
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while not priority_queue.empty():
            cost, current = priority_queue.get()

            if current == goal:
                agent.path = self.reconstruct_path(came_from, start, goal)
                return agent.path

            for neighbor in self.get_neighbors(current, map_info):
                new_cost = cost + 1  
                priority = new_cost + self.manhattan_distance(goal, neighbor)

                if neighbor not in visited or priority < cost_so_far.get(neighbor, float('inf')):
                    priority_queue.put((priority, neighbor))
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    visited.add(neighbor)

        return None
    def reconstruct_path(came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        return path[::-1]

