import pygame
import random

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1500

class RenderInfo:
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT

    def __init__(self, map_info, keys, doors, up_stairs, down_stairs, goals):
        self.map_info = map_info
        self.floor = 1
        self.keys = keys
        self.doors = doors
        self.up_stairs = up_stairs
        self.down_stairs = down_stairs
        self.goals = goals
        self.font = pygame.font.SysFont('Arial', 12)
        self.colors = []
        self.agents_paths = []
        for i in range(len(self.goals)):
            self.colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.cell_size = 20
        self.margin = 2
        self.board_height = len(map_info[0]) * (self.cell_size + self.margin)
        self.board_width = len(map_info[0][0]) * (self.cell_size + self.margin)
        self.agents_current_pos = []

    def update_current_pos(self):
        self.agents_current_pos = []
        for path in self.agents_paths:
            if len(path) > 0:
                self.agents_current_pos.append(path.pop(0))
        if self.agents_current_pos[0][0] != self.floor - 1:
            self.floor = self.agents_current_pos[0][0] + 1

    def draw(self, surface):
        surface.fill((255, 255, 255))
        floor_info = self.map_info[self.floor - 1]
        for i in range(len(floor_info)):
            for j in range(len(floor_info[i])):
                if floor_info[i][j] == 0 or floor_info[i][j] == -2:
                    rect = pygame.Rect(j * (self.cell_size + self.margin), i * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                    pygame.draw.rect(surface, (128, 128, 128), rect)
                elif floor_info[i][j] == -1:
                    rect = pygame.Rect(j * (self.cell_size + self.margin), i * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                    pygame.draw.rect(surface, (0, 0, 0), rect)
        # If the cell is a key, add text K<num> to the cell
        for key in self.keys:
            if key[0] == self.floor - 1:
                rect = pygame.Rect(key[2] * (self.cell_size + self.margin), key[1] * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                text = self.font.render('K' + str(self.keys.index(key) + 1), True, (0, 0, 0))
                text_rect = text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2))
                surface.blit(text, text_rect)
        # If the cell is a door, add text D<num> to the cell
        for door in self.doors:
            if door[1][0] == self.floor - 1:
                rect = pygame.Rect(door[1][2] * (self.cell_size + self.margin), door[1][1] * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                text = self.font.render('D' + str(door[0] + 1), True, (0, 0, 0))
                text_rect = text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2))
                surface.blit(text, text_rect)
        # If the cell is an UP stairs, add text UP to the cell
        for up_stairs in self.up_stairs:
            if up_stairs[0] == self.floor - 1:
                rect = pygame.Rect(up_stairs[2] * (self.cell_size + self.margin), up_stairs[1] * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                text = self.font.render('UP', True, (0, 0, 0))
                text_rect = text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2))
                surface.blit(text, text_rect)
        # If the cell is a DOWN stairs, add text DOWN to the cell
        for down_stairs in self.down_stairs:
            if down_stairs[0] == self.floor - 1:
                rect = pygame.Rect(down_stairs[2] * (self.cell_size + self.margin), down_stairs[1] * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                text = self.font.render('DO', True, (0, 0, 0))
                text_rect = text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2))
                surface.blit(text, text_rect)
        # If the cell is a goal, add text T<num> to the cell
        for goal in self.goals:
            if goal[0] == self.floor - 1:
                rect = pygame.Rect(goal[2] * (self.cell_size + self.margin), goal[1] * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                # color = (255, 0, 0) if self.goals.index(goal) == 0 else random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
                color = self.colors[self.goals.index(goal)]
                pygame.draw.rect(surface, color, rect)
                text = self.font.render('T' + str(self.goals.index(goal) + 1), True, (0, 0, 0))
                text_rect = text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2))
                surface.blit(text, text_rect)
        # If the cell is an agent, add text A<num> to the cell
        for agent in self.agents_current_pos:
            if agent and agent[0] == self.floor - 1:
                rect = pygame.Rect(agent[2] * (self.cell_size + self.margin), agent[1] * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                color = self.colors[self.agents_current_pos.index(agent)]
                pygame.draw.rect(surface, color, rect)
                text = self.font.render('A' + str(self.agents_current_pos.index(agent) + 1), True, (0, 0, 0))
                text_rect = text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2))
                surface.blit(text, text_rect)
            surface.blit(surface, (0, 0))
        
            

    def go_up(self):
        if self.floor == len(self.map_info):
            return
        self.floor += 1

    def go_down(self):
        if self.floor == 1:
            return
        self.floor -= 1

    def set_agents_paths(self, agents_paths):
        self.agents_paths = agents_paths
