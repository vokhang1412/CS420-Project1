# The class MapInfo should be able to store all the information of the map
# It contains a 3D array, each 2D array represents a floor. This array is static and will not change throughout the game.
# It also contains a list of agents, each agent is an object of the class Agent.

class MapInfo:
    map_info = []
    agents = []
    
    def __init__(self, map_info, agents):
        self.map_info = map_info
        self.agents = agents

