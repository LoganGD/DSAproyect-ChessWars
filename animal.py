import pygame
from constants import *
from actions import Actions
import random
import math
from grid import Grid

# documenta esto
def prob(p, dt):
    success = random.random() < (p * dt)
    return success

class Animal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)

class Cow(Animal):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.position = pygame.Vector2(pos_x, pos_y)
        self.action = Actions.RUNNING
        self.angle = 0

    def update(self, dt):
        if self.action == Actions.WALKING:
            self.walk(dt)
        if self.action == Actions.RUNNING:
            self.run(dt)
        if self.action == Actions.IDLE:
            pass
    
    def walk(self, dt):
        if prob(0.3, dt):
            self.angle += random.gauss(0.5, 0.5)
            print(self.angle)
        self.position.x += math.cos(self.angle) * dt * 0.5
        self.position.y += math.sin(self.angle) * dt * 0.5
    
    def run(self, dt):
        if prob(0.3, dt):
            self.angle += random.gauss(0.5, 0.5)

        self.position.x += math.cos(self.angle) * dt
        self.position.y += math.sin(self.angle) * dt

    def draw(self, world: pygame.Surface, grid: Grid, camera: pygame.Vector3):
        pos_x = ( self.position.x - camera.x + 1/2) * camera.z
        pos_y = ( self.position.y - camera.y + 1/2) * camera.z

        terrain = grid.get_terrain(self.position)

        if pos_x < 0 or pos_x > world.get_width():
            return
        if pos_y < 0 or pos_y > world.get_height():
            return

        font_size = round(camera.z)
        font = pygame.font.Font(None, font_size) # None for default
        self.text = font.render("cow", True, BLACK, terrain.color)
        text_rect = self.text.get_rect(center=(pos_x, pos_y))
        world.blit(self.text, text_rect)
