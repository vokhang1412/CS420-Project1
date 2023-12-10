import os
from level import level1
from level import level2
from level import level3
from level import level4

from GUI import display

from helper import *

from models import agent
from models import board

class Game:
    def __init__(self):
        self.level = 1

        self.level1_solver = level1.Level1()
        self.level2_solver = level2.Level2()
        self.level3_solver = level3.Level3()
        self.level4_solver = level4.Level4()
        self.displayer = None

        self.floor = None
        self.rows = None
        self.cols = None
        self.map_info = None
        self.agent_pos = None
        self.goal_pos = None
        self.key_pos = None
        self.door_pos = None
        self.up_stairs_pos = None
        self.down_stairs_pos = None

        self.path_save_for_lv1 = []
        self.agents = []
        self.board = None

    # App Flow:
    # 1. Choose level
    # 2. If level 1, choose algorithm
    # 3. Input map name
    # 4. Read info from map
    # 5. Call solver
    # 6. Display result

    def choose_level(self):
        print("Choose level:")
        print("1. Level 1")
        print("2. Level 2")
        print("3. Level 3")
        print("4. Level 4")
        level = int(input("Your choice: "))
        return level
    
    def choose_algorithm(self):
        print("Choose algorithm:")
        print("1. BFS")
        print("2. DFS")
        print("3. UCS")
        print("4. A*")
        algorithm = int(input("Your choice: "))
        return algorithm
    
    def input_map_name(self):
        # format of map name: input<num>-level<level>.txt
        map_name = input("Choose map (from 1 to 5): ")
        if map_name == '1':
            map_name = 'input1-level' + str(self.level) + '.txt'
        elif map_name == '2':
            map_name = 'input2-level' + str(self.level) + '.txt'
        elif map_name == '3':
            map_name = 'input3-level' + str(self.level) + '.txt'
        elif map_name == '4':
            map_name = 'input4-level' + str(self.level) + '.txt'
        elif map_name == '5':
            map_name = 'input5-level' + str(self.level) + '.txt'
        else:
            print("Invalid map name")
            return self.input_map_name()
        return map_name
    
    def read_map(self, map_name):
        self.floor, self.rows, self.cols, self.map_info, self.agent_pos, self.goal_pos, self.key_pos, self.door_pos, self.up_stairs_pos, self.down_stairs_pos = read_map('./data/' + map_name)

    def call_solver(self, algorithm):
        self.board = board.Board(self.floor, self.rows, self.cols, self.map_info, self.agent_pos, self.goal_pos, self.key_pos, self.door_pos, self.up_stairs_pos, self.down_stairs_pos)
        for i in range(len(self.agent_pos)):
            self.agents.append(agent.Agent((self.agent_pos[i][0], self.agent_pos[i][1], self.agent_pos[i][2]), self.goal_pos[i], self.board))
        if self.level == 1:
            if algorithm == 1:
                self.path_save_for_lv1 = self.level1_solver.bfs(self.map_info[0], self.agents[0])
            elif algorithm == 2:
                self.path_save_for_lv1 = self.level1_solver.dfs(self.map_info[0], self.agents[0])
            elif algorithm == 3:
                self.path_save_for_lv1 = self.level1_solver.ucs(self.map_info[0], self.agents[0])
            elif algorithm == 4:
                self.path_save_for_lv1 = self.level1_solver.astar(self.map_info[0], self.agents[0])
        elif self.level == 2:
            self.level2_solver.solve(self.board, self.agents[0])
        elif self.level == 3:
            self.level3_solver.solve(self.board, self.agents[0])
        elif self.level == 4:
            self.level4_solver.solve(self.board, self.agents)

    def display_result(self):
        self.displayer = display.Display(self.map_info, self.key_pos, self.door_pos, self.up_stairs_pos, self.down_stairs_pos, [], self.goal_pos, [])
        if self.level==1 or self.level == 2 or self.level == 3:
            if len(self.agents[0].path) == 0:
                print("No solution")
                return
            self.displayer.render_info.agents_paths.append(self.agents[0].path.copy())
            self.displayer.render_info.agents_goals.append(self.agents[0].goal.copy())
            self.displayer.to_export.append(self.agents[0].path.copy()) 
        elif self.level == 4:
            if len(self.agents[0].path) == 0:
                print("No solution")
                return
            for i in range(len(self.agents)):
                self.displayer.render_info.agents_paths.append(self.agents[i].path.copy())
                self.displayer.render_info.agents_goals.append(self.agents[i].goal.copy())
                self.displayer.to_export.append(self.agents[i].path.copy())
        self.displayer.run()

    def run(self):
        self.level = self.choose_level()
        if self.level == 1:
            algorithm = self.choose_algorithm()
        else:
            algorithm = 0
        map_name = self.input_map_name()
        self.read_map(map_name)
        self.call_solver(algorithm)
        self.display_result()