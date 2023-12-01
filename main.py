import sys
import pygame
from collections import deque
from helper import *
sys.path.insert(0, './data')
sys.path.insert(0, './GUI')
sys.path.insert(0, './level')
sys.path.insert(0, './models')
from GUI import display
from GUI import render_info
from level import level1
from level import level2
from level import level3
from level import level4
from models import agent
from models import board
GRID_WIDTH = 0
GRID_HEIGHT = 0

# Screen size
SCREEN_WIDTH = render_info.SCREEN_WIDTH
SCREEN_HEIGHT = render_info.SCREEN_HEIGHT

if __name__ == '__main__':
    floor, rows, cols, map_info, agent_pos, goal_pos, key_pos, door_pos, up_stairs_pos, down_stairs_pos = read_map('./data/level3.txt')

    displayer = display.Display(map_info, key_pos, door_pos, up_stairs_pos, down_stairs_pos, [], goal_pos) 

    level2_solver = level2.Level2()

    agent_t1 = agent.Agent((agent_pos[0][0], agent_pos[0][1], agent_pos[0][2])) 

    board = board.Board(floor, rows, cols, map_info, agent_pos, goal_pos, key_pos, door_pos, up_stairs_pos, down_stairs_pos)
    # print(board.floor)
    # print(board.rows)
    # print(board.cols)
    # for i in range(len(board.keys)):
    #     print(board.keys[i])
    level2_solver.solve(board, agent_t1)
    # level2_solver.find_path(agent_t1, (0, 4, 6), (1, 4, 9), board)
    print(agent_t1.path)
    # for i in range(len(board.successors)):
    #     print(board.keys[i])
    #     print(len(board.successors[i]))
    #     for j in range(len(board.successors[i])):
    #         print(board.successors[i][j])
    # for i in range(len(board.goal_successors[0])):
    #     print(board.goal_successors[0][i])
    # print(board.key_number[(0, 3, 12)])
    # print(board.door_number[(0, 15, 2)])
    # print(board.key_number[(0, 11, 11)])
    # print(board.can_visit_key[board.key_number[(0, 4, 4)]])
    # print(board.has_key[board.door_number[(0, 3, 5)]])
    displayer.render_info.agents_paths.append(agent_t1.path)

    displayer.to_export.append(agent_t1.path.copy())

    displayer.run()
    
    
