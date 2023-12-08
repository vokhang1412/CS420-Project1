import pygame
import export_heatmap
import random
from .render_info import RenderInfo

period = 0.2

class Display:
    def __init__(self, map_info, keys, doors, up_stairs, down_stairs, paths, goal_pos):
        self.delta_time = 0
        self.accu_time = 0
        pygame.init()
        self.screen = pygame.display.set_mode((RenderInfo.SCREEN_WIDTH, RenderInfo.SCREEN_HEIGHT))
        self.screen.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.zoom_rate = 1

        self.render_info = RenderInfo(map_info, keys, doors, up_stairs, down_stairs, goal_pos)

        self.surface = pygame.Surface((self.render_info.board_width, self.render_info.board_height), pygame.SRCALPHA)

        self.center_x = RenderInfo.SCREEN_WIDTH / 2 - self.surface.get_width() / 2
        self.center_y = RenderInfo.SCREEN_HEIGHT / 2 - self.surface.get_height() / 2

        self.screen.blit(self.surface, (self.center_x, self.center_y))

        self.render_info.agents_paths = paths

        self.to_export = []

        self.render_info.agents_current_pos = []

    def run(self):
        while True:
            self.delta_time = self.clock.tick(self.fps) / 1000.0
            self.accu_time += self.delta_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.render_info.go_up()
                    elif event.key == pygame.K_DOWN:
                        self.render_info.go_down()

            if self.accu_time >= period:
                self.accu_time -= period
                self.render_info.update_current_pos()
                
            self.render_info.draw(self.surface)

            self.screen.blit(self.surface, (self.center_x, self.center_y))
            pygame.display.flip()

            if self.render_info.agents_paths[0] == []:
                pygame.time.wait(2000)
                for path in self.to_export:
                    exporter = export_heatmap.HeatmapExporting(self.render_info.map_info, path, self.to_export.index(path) + 1)
                    exporter.export()
                pygame.quit()
                quit()

