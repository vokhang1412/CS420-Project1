# This class store the information of an agent, including its start position, current position, its goal, and its path.

class Agent:
    start = ()
    current = ()
    goal = ()
    path = []
    
    def __init__(self, start, goal):
        self.start = start
        self.current = start
        self.goal = goal
        self.path = []
