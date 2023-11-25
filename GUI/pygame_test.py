# Write a GUI for displaying the game board, the agent's path, and the agent's actions.
# The render should also show the location of Mr. Thanh (T1) and the location of the agent (A). (throughout the game)
# The agent should move one step at a time, and the GUI should update the game board after each step.
# The GUI should also display the number of steps taken by the agent.
# The GUI should also display the agent's actions.
# The GUI must be implemented using pygame and encapsulate in a class.

import pygame
import sys
from helper import *
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
ORANGE = (255,165,0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
MARGIN = 5





