import sys
from helper import *

sys.path.insert(0, './class')
sys.path.insert(0, './data')
sys.path.insert(0, './GUI')
sys.path.insert(0, './level')

if __name__ == '__main__':
    # Read the map file
    map_info, agent_pos, goal_pos = read_map('./data/map.txt')
    # Print the map
    test_print_map(map_info)
    print(agent_pos)
    print(goal_pos)
    