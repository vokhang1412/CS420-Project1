# This file contains list of helper functions for the project
import os

def read_map(filename):
    # Read the map file and return the map in the form of a list of lists
    # The first line of the map file contains the number of rows and columns
    # Each inner list represents a row in the map
    # The map file contains 0s and -1s
    # 0s represent empty cells
    # -1s represent cells with obstacles
    # Keys are represent by K1, K2, K3, K4, K5,...
    # Doors are represented by D1, D2, D3, D4, D5,...
    # Mr. Thanh is represented by T1
    # The default agent is A1, which is corresponding to the task to find T1
    # In multiple agent task, the agent is represented by A2, A3, A4,... each will have a corresponding goal T2, T3, T4,...
    # A map can contains multiple floors, each floor will be lead by the line [floor<n>], for example [floor1] will annotate first floor
    # The stairs will be annotate using 2 different symbols, if the stairs is going up, it will be annotated by UP, if the stairs is going down, it will be annotated by DO
    # You can assume that the map file will be in the correct format.

    # Process
    # 1. Open the file
    map_info = []
    agent_pos = []
    goal_pos = []
    key_pos = []
    door_pos = []
    up_stairs_pos = []
    down_stairs_pos = []
    with open(filename, 'r') as f:
        # 2. Read the first line to get the number of rows and columns
        rows, cols = map(int, f.readline().strip().split(','))
        # 3. Loop to find the floor
        while True:
            line = f.readline().strip()
            if not line:
                break
            if line[0] == '[':
                board = []
                # 4. Read the floor
                for _ in range(rows):
                    line = f.readline().strip().split(',')
                    row = []
                    for i in range(cols):
                        # Read blank space
                        if line[i] == '0':
                            row.append(0)
                        # Read obstacles
                        elif line[i] == '-1':
                            row.append(-1)
                        # Read agents
                        elif line[i].find('A') != -1:
                            row.append(0)
                            # Find the number after A
                            num = int(line[i][1:])
                            # Add the agent to the list corresponding to the number
                            while len(agent_pos) < num:
                                agent_pos.append((0, 0, 0))
                            agent_pos[num-1] = (len(map_info), len(board), i)
                        # Read goals
                        elif line[i].find('T') != -1:
                            row.append(0)
                            # Find the number after T
                            num = int(line[i][1:])
                            # Add the goal to the list corresponding to the number
                            while len(goal_pos) < num:
                                goal_pos.append((0, 0, 0))
                            goal_pos[num-1] = (len(map_info), len(board), i)
                        # Read keys
                        elif line[i].find('K') != -1:
                            row.append(0)
                            # Find the number after K
                            num = int(line[i][1:])
                            # Add the key to the list corresponding to the number
                            while len(key_pos) < num:
                                key_pos.append((0, 0, 0))
                            key_pos[num-1] = (len(map_info), len(board), i)
                        # Read UP stairs
                        elif line[i] == 'UP':
                            row.append(0)
                            # Add the UP stairs to the list
                            up_stairs_pos.append((len(map_info), len(board), i))
                        # Read DOWN stairs
                        elif line[i] == 'DO':
                            row.append(0)
                            # Add the DOWN stairs to the list
                            down_stairs_pos.append((len(map_info), len(board), i))
                        # Read doors
                        elif line[i].find('D') != -1:
                            row.append(0)
                            # Find the number after D
                            num = int(line[i][1:])
                            # Add the door to the list corresponding to the number
                            door_pos.append((num-1, (len(map_info), len(board), i)))
                        else:
                            row.append(line[i])
                    board.append(row)
                map_info.append(board)
    # 5. Return the map
    return len(map_info), rows, cols, map_info, agent_pos, goal_pos, key_pos, door_pos, up_stairs_pos, down_stairs_pos

def test_print_map(map_info):
    # This function is used to test the map
    # You can use this function to print the map
    # The map should be printed in the correct format
    # You can use this function to test if the map is read correctly
    for floor in map_info:
        for row in floor:
            for col in row:
                print(col, end=" ")
            print()
        print()
                

