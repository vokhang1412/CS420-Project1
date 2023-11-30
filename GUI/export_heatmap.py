import pygame
import helper

CELL_SIZE = 20
MARGIN = 2

class HeatmapExporting:
    map_info = []
    path = []
    agent_num = 0

    def __init__(self, map_info, path, agent_num):
        self.map_info = map_info
        self.path = path
        self.agent_num = agent_num
        for cell in path:
            self.map_info[cell[0]][cell[1]][cell[2]] += 1
        max = 0
        for floor in self.map_info:
            for row in floor:
                for cell in row:
                    if cell > max:
                        max = cell
        self.heat_per_step = 255 / max
        helper.test_print_map(self.map_info)

    def export_heatmap(self, floor):
        surface = pygame.Surface((len(self.map_info[floor][0]) * (CELL_SIZE + MARGIN), len(self.map_info[floor]) * (CELL_SIZE + MARGIN)), pygame.SRCALPHA)
        for i in range(len(self.map_info[floor])):
            for j in range(len(self.map_info[floor][i])):
                rect = pygame.Rect(j * (CELL_SIZE + MARGIN), i * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
                if self.map_info[floor][i][j] == 0:
                    pygame.draw.rect(surface, (255, 255, 255), rect)
                elif self.map_info[floor][i][j] == -1:
                    pygame.draw.rect(surface, (0, 0, 0), rect)
                else:
                    pygame.draw.rect(surface, (255, 255 - self.map_info[floor][i][j] * self.heat_per_step, 255 - self.map_info[floor][i][j] * self.heat_per_step), rect)
        pygame.image.save(surface, "floor" + str(floor) + ".png")

    def export(self):
        # create a folder for the agent
        import os
        if not os.path.exists("agent " + str(self.agent_num)):
            os.makedirs("agent " + str(self.agent_num))
        os.chdir("agent " + str(self.agent_num))

        # export the heatmap
        for floor in range(self.map_info.__len__()):
            self.export_heatmap(floor)
        os.chdir("..")