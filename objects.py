import pygame
import random
import time 

class GameObject : 

    def __init__(self, image_path, points):
      
     self.image = pygame.image.load(image_path)
     self.image = pygame.transform.scale(self.image, (50, 50))
     self.rect = self.image.get_rect()
     self.points = points

    def draw(self, surface): 
        surface.blit(self.image, self.rect)
    
    def checkClick(self, mouse_position): 
        return self.rect.collidepoint(mouse_position)
    
    def updatePosition(self, width, height): 
        self.rect.x = random.randint(0, width)
        self.rect.y = random.randint(0, height)

    
class Tree(GameObject): 

    def __init__(self, image_path):
        super().__init__(image_path, points=1)

        self.spawn_time_tree = time.time()

    def on_click(self):

        self.points = 1
        return self.points


class Cross(GameObject): 

    def __init__(self, image_path):
        super().__init__(image_path, points=-30)
        self.lives_impact = -1
        self.spawn_time_cross = time.time()

    def on_click(self):
        
      

        return self.points, self.lives_impact


class Star(GameObject): 

    def __init__(self, image_path): 
        
        super().__init__(image_path, points=0)
        self.bonus_points = 5
        self.spawn_time_star = time.time()

    def on_click(self):
        return self.bonus_points
    