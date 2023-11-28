import sys
import pygame
from collections import deque
from helper import *

sys.path.insert(0, './classes')
sys.path.insert(0, './data')
sys.path.insert(0, './GUI')
sys.path.insert(0, './level')

from GUI import display
from GUI import render_info

GRID_WIDTH = 0
GRID_HEIGHT = 0

# Screen size
SCREEN_WIDTH = render_info.SCREEN_WIDTH
SCREEN_HEIGHT = render_info.SCREEN_HEIGHT

if __name__ == '__main__':
    map_info, agent_pos, goal_pos, key_pos, door_pos, up_stairs_pos, down_stairs_pos = read_map('./data/map.txt')

    displayer = display.Display(map_info, key_pos, door_pos, up_stairs_pos, down_stairs_pos, [], goal_pos) 

    displayer.render_info.agents_paths = [[(0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0), (0, 5, 0)]]

    displayer.run()
    
