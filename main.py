import sys
from helper import *

sys.path.insert(0, './class')
sys.path.insert(0, './data')
sys.path.insert(0, './GUI')
sys.path.insert(0, './level')

if __name__ == '__main__':
    # Read the map file
    filename = './data/map.txt'
    map_info, agent_pos, goal_pos, key_pos, door_pos, up_stairs_pos, down_stairs_pos = read_map(filename)
    # Print the map
    test_print_map(map_info)
    print(agent_pos)
    print(goal_pos)
    print(key_pos)
    print(door_pos)
    print(up_stairs_pos)
    print(down_stairs_pos)