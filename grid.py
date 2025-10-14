import pygame
from perlin_numpy import generate_perlin_noise_2d
from math import floor, ceil
from random import randint
from constants import *

class Grid:
    def __init__(self):
        # create the grid
        noise = generate_perlin_noise_2d((GRID_WIDTH, GRID_HEIGHT), (1, 1))
        self.cells = [[] for _ in range(GRID_WIDTH)]

        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if abs(noise[i][j]) < 0.02:
                    self.cells[i].append(Terrain(i, j, BLUE))
                elif abs(noise[i][j]) > 0.04 and randint(0,100) == 0:
                    self.cells[i].append(Terrain(i, j, DARK_GREEN))
                else:
                    self.cells[i].append(Terrain(i, j, GREEN))

    def get_terrain(self, position: pygame.Vector2):
        x = floor(position.x)
        y = floor(position.y)
        return self.cells[x][y]

    def draw(self, world: pygame.Surface, camera: pygame.Vector3):
        # limit to draw only what it's shown on camera
        low_x = floor(camera.x)
        low_y = floor(camera.y)
        high_x = ceil(camera.x + world.get_width() / camera.z)
        high_y = ceil(camera.y + world.get_height() / camera.z)

        # start offset
        start = -round(camera * camera.z)
        for i in range(low_x, high_x):
            for j in range(low_y, high_y):
                self.cells[i][j].draw(world, camera, start)
        
class Terrain:
    def __init__(self, pos_x, pos_y, color):
        self.position = pygame.Vector3(pos_x, pos_y, 0)
        self.color = color
    
    def draw(self, world: pygame.Surface, camera: pygame.Vector3, start: pygame.Vector3):
        draw_position = start + self.position * camera.z
        pygame.draw.rect(world, self.color, (draw_position.x, draw_position.y, camera.z, camera.z))
