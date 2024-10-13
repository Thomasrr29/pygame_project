import pygame
import sys
import time
from objects import Tree
from objects import Cross
from objects import Star

class Game: 
    
    def __init__(self): 


        self.game_state = 'MENU'

        self.lives = 3
        self.level_game = 1
        self.points = 0
        self.objects = []
        self.max_objects = 20
        self.max_objects = min(self.max_objects, 70)
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.menu_heigh = 100
        self.game_area_rect = pygame.Rect(0, self.menu_heigh, self.width, self.height - self.menu_heigh)

        self.font = pygame.font.Font(None, 36)

        self.spawn_interval = 2000
        self.spawn_event = pygame.USEREVENT + 1
        self.heart_event = pygame.USEREVENT + 2
        self.remove_event = pygame.USEREVENT + 3
        pygame.time.set_timer(self.spawn_event, self.spawn_interval)
        pygame.time.set_timer(self.spawn_event, self.spawn_interval * 3)
        
    def spawn_objects(self): 

        trees_num = 5        
        heart_num = 1
        num_crosses = 3
        num_stars = 2


        if( len(self.objects) < self.max_objects): 

            for _ in range(trees_num): 
                tree = Tree('assets/tree-solid.png')
                tree.updatePosition(self.width, self.height)
                self.objects.append(tree)

            for _ in range(num_crosses): 
                cross = Cross('assets/xbox-brands-solid.png')
                cross.updatePosition(self.width, self.height)
                self.objects.append(cross)

            for _ in range(num_stars): 
                star = Star('assets/star-solid.png')
                star.updatePosition(self.width, self.height)
                self.objects.append(star)

    def draw_objects(self): 

        for object in self.objects: 
            if object.rect.colliderect(self.game_area_rect): 
                object.draw(self.screen)     

    def handle_events(self): 

        for event in pygame.event.get(): 

            if(event.type == pygame.QUIT): 
                pygame.quit()
                sys.exit()
            
            elif(self.game_state == 'MENU' and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):

                self.game_state = 'PLAYING'
                self.spawn_objects()

            elif(self.game_state == 'GAME OVER' and event.type == pygame.KEYDOWN and event.key == pygame.K_r): 

                self.game_state = 'PLAYING'
                self.points = 0
                self.lives = 3
                self.spawn_objects()
                

            elif event.type == pygame.MOUSEBUTTONDOWN: 
                
                mouse_position = pygame.mouse.get_pos()
                self.handle_click(mouse_position)
            
            elif event.type == self.spawn_event: 

                self.spawn_objects()
 
    def update_game(self): 
        
        
        current_time = time.time()

        for object in self.objects[:]:

            if isinstance(object, Cross):
                if current_time - object.spawn_time_cross > 5: 
                    self.objects.remove(object)

            elif isinstance(object, Star): 
                if current_time - object.spawn_time_star > 3: 
                    self.objects.remove(object)

            elif isinstance(object, Tree): 
                if current_time - object.spawn_time_tree > 5: 
                    self.objects.remove(object)

        self.update_level()

        if(self.lives <= 0): 
            self.game_state = 'GAME OVER'

    def draw_menu(self): 

        score_text = self.font.render(f'Points: {self.points}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        level_text = self.font.render(f'Level: {self.level_game}', True, (255, 255, 0))  
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(level_text, (140, 10))

    def handle_click(self, mouse_position):

        for object in self.objects: 

            if object.checkClick(mouse_position): 
                result = object.on_click()
                self.apply_result(result)
                points = result if isinstance(result, int) else result[0]
                self.max_objects += int(points/2)
                self.objects.remove(object)

    def apply_result(self, result):

        if isinstance(result, tuple): 

            points, lives_impact = result
            self.points += points
            self.lives += lives_impact

        elif isinstance(result, int):
            self.points += result

    def update_level(self):   

        if self.points >= (self.level_game * 10):
            self.level_game += 1

            if(self.spawn_interval > 800): 
                self.spawn_interval -= 20
            
            if self.max_objects < 150:
                self.max_objects += 8
        
            pygame.time.set_timer(self.spawn_event, self.spawn_interval)
                        
    def set_difficulty(self, spawn_object_interval, max_objects): 
        self.spawn_interval = spawn_object_interval
        self.max_objects = min(max_objects, 80)
        pygame.time.set_timer(self.spawn_event, self.spawn_interval)

    def run(self):

        running = True 

        while running: 

            self.handle_events()

            if(self.game_state == 'MENU'): 

                self.screen.fill((0, 0, 0))
                menu_text = self.font.render('Press ENTER to start', True, (255, 255, 255))
                self.screen.blit(menu_text, (self.width // 2 - 100, self.height // 2))
            
            elif(self.game_state == 'PLAYING'): 
                self.update_game()
                self.screen.fill((182, 196, 84))
                self.draw_objects()
                self.draw_menu()

            elif(self.game_state == 'GAME OVER'): 
                self.screen.fill((0, 0, 0))
                game_over_text = self.font.render('GAME OVER', True, (255, 0, 0))
                restart_text = self.font.render('Press R to restart', True, (255, 0, 0))
                self.screen.blit(game_over_text, (self.width // 2 - 50, self.height // 2))
                self.screen.blit(restart_text, (self.width // 2 - 70, self.height // 2 + 100))

            pygame.display.flip()
            pygame.time.Clock().tick(60)