import pygame
import sys
import time
from objects import Tree
from objects import Monster
from objects import Star
from objects import Heart
from objects import BossMonster

class Game: 
    
    def __init__(self): 

        pygame.mouse.set_visible(False)
        self.custom_cursor = pygame.image.load('assets/aim.png')
        self.custom_cursor = pygame.transform.scale(self.custom_cursor, (50, 50))
        self.game_state = 'MENU'

        self.lives = 3
        self.level_game = 1
        self.points = 0
        self.objects = []
        self.trees_num = 3
        self.monster_num = 3
        self.stars_num = 2
        self.heart_num = 1
        self.boss_num = 1

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

        if( len(self.objects) < self.max_objects): 

            for _ in range(self.trees_num): 
                tree = Tree('assets/leaf.png')
                tree.updatePosition(self.width, self.height)
                self.objects.append(tree)

            for _ in range(self.monster_num): 
                monster = Monster('assets/monster.png')
                monster.updatePosition(self.width, self.height)
                self.objects.append(monster)

            for _ in range(self.stars_num): 
                star = Star('assets/star.png')
                star.updatePosition(self.width, self.height)
                self.objects.append(star)

            for _ in range(self.heart_num): 
                heart = Heart('assets/heart.png')
                heart.updatePosition(self.width, self.height)
                self.objects.append(heart)
            
            for _ in range(self.boss_num): 
                boss = BossMonster('assets/cthulhu.png')
                boss.updatePosition(self.width, self.height)
                self.objects.append(boss)

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
                self.trees_num = 3
                self.monster_num = 4
                self.stars_num = 2
                self.heart_num = 1
                self.points = 0
                self.level_game = 1
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

            if isinstance(object, Monster):
                if current_time - object.spawn_time_monster > 4: 
                    self.objects.remove(object)

            elif isinstance(object, Star): 
                if current_time - object.spawn_time_star > 2: 
                    self.objects.remove(object)

            elif isinstance(object, Tree): 
                if current_time - object.spawn_time_tree > 3: 
                    self.objects.remove(object)

            elif isinstance(object, Heart): 
                if current_time - object.heart_spawn_time > 1.5: 
                    self.objects.remove(object)

            elif isinstance(object, BossMonster): 
                if current_time - object.boss_spawn_time > 1.8: 
                    self.objects.remove(object)

        self.update_level()

        if(self.lives <= 0): 
            self.game_state = 'GAME OVER'

    def draw_menu(self): 

        score_text = self.font.render(f'Points: {self.points}', True, (255, 255, 0))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 0))
        level_text = self.font.render(f'Level: {self.level_game}', True, (255, 255, 0))  
        self.screen.blit(level_text, (10, 20))
        self.screen.blit(score_text, (150, 20))
        self.screen.blit(lives_text, (320, 20))

    def draw_titles(self, text, font_size, position, color_font, color_shadow):

        font = pygame.font.Font(None, font_size)

        main_text = font.render(text, True, color_font)
        offset_text1 = font.render(text, True, color_shadow)

        self.screen.blit(main_text, position)
        self.screen.blit(offset_text1, (position[0] + 3, position[1] + 3))

    def draw_background_image(self, image): 

        self.background = pygame.image.load(image)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen.blit(self.background, (0, 0))

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

        if self.points >= (self.level_game * 20):
            
            self.level_game += 1
            self.trees_num += 2

            if(self.spawn_interval > 800): 
                self.spawn_interval -= 20
            
            if self.max_objects < 120:
                self.max_objects += 4

            if(self.level_game > 6): 
                self.monster_num += 3

            if(self.level_game > 8): 
                self.heart_num += 1
                self.stars_num += 1
        
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

                self.draw_background_image('assets/4k-background-fd313fxzl511betu.jpg')    
                self.draw_titles('REACTION GAME', 140, (self.width // 2 - 400, 300), (255, 255, 255), (0, 128, 255)) 
                self.draw_titles('Press SPACE for start ...', 80, (self.width // 2 - 250, 400), (255, 255, 0), (128, 0, 128))
            
            elif(self.game_state == 'PLAYING'): 

                self.screen.fill((0, 0, 0))
                self.update_game()
                self.draw_objects()
                self.draw_menu()

            elif(self.game_state == 'GAME OVER'): 
                
                self.draw_background_image('assets/1280x720_game-over-4k.jpg')
                self.draw_titles('Press R to restart ...', 40, (self.width // 2 - 50, 500), (255, 255, 255), (128, 0, 128))


            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.custom_cursor, (mouse_x - self.custom_cursor.get_width() // 2, mouse_y - self.custom_cursor.get_width() // 2))

            pygame.display.flip()
            pygame.time.Clock().tick(60)