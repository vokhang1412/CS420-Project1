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
from GUI import menu
GRID_WIDTH = 0
GRID_HEIGHT = 0

# Screen size
SCREEN_WIDTH = render_info.SCREEN_WIDTH
SCREEN_HEIGHT = render_info.SCREEN_HEIGHT

if __name__ == '__main__':
    
    game = menu.Game()
    game.run()
    
