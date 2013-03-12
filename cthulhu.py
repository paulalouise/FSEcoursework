#!/usr/bin/env python
# import the pygame module, so you can use it
import pygame

from pygame.sprite import Sprite
#SPRITES-----------------------------------------------------------

class character(Sprite):
        """
        Handles character behaviour
        """
        def __init__(self, color, position, obstacle, life, endgame):
                #call constructor parent
                Sprite.__init__(self)
                self.image = pygame.Surface([60,80])
                self.rect = pygame.Rect(0, 0, 60, 80)
                pygame.draw.rect(self.image, pygame.Color("red"), self.rect)
                self.rect.center = position
                self.obstacle = obstacle
                self.life = life
                self.velocity = 0

                
                self.jump = False
                self.fall = False

        def up(self):
                self.jump = True
                
        def down(self):
                self.fall = True
                
        def left(self):
                self.velocity -= 5
                
        def right(self) :
                self.velocity += 5

        def update(self):
                if self.jump:
                        self.rect.move_ip(0, -4)
                        if self.rect.bottom < 175:
                                self.jump = False
                                self.fall = True
                if self.fall:
                        self.rect.move_ip(0, 4)
                        if self.rect.centery > 240:
                                self.fall = False
                                self.jump = False
                                self.rect.centery = 240
                        elif self.down :
                                self.fall = True
                                self.jump = False
                                
                self.rect.move_ip(self.velocity, 0)
                self.rect.left = max(self.rect.left, 0)
                self.rect.right = min(self.rect.right, 800)                
                                                 
                

                if self.rect.colliderect(self.obstacle.rect):
                        if self.life.life > 0 :
                               self.life.die()
                        else :
                               self.obstacle.scroll = False




class obstacles(Sprite):
        """
        Handles obstacle behaviour
        """
        def __init__(self, color, position, score):
                #call constructor parent
                Sprite.__init__(self)
                self.image = pygame.Surface([35,200])
                self.rect = pygame.Rect(0, 0, 35, 200)
                pygame.draw.rect(self.image, pygame.Color("black"), self.rect)
                self.rect.center = position
                self.score = score
                
                self.scroll = True

        def scroll(self):
                self.scroll = True

        def update(self):
                if self.scroll:
                        self.rect.move_ip(0, -5)
                        self.scroll = True
                else :
                        self.rect.move_ip(0, 10)
                if self.rect.centery < 190:
                        self.scroll = False 
                if self.rect.centery > 600 and self.scroll == False:
                        self.scroll = True
                        self.score.increase()
                        
                        
                        
                        
class score(Sprite):
        """
        Displays score.
        """
        def __init__(self, color, position):
                #call constructor parent
                pygame.sprite.Sprite.__init__(self)
                self.color = pygame.Color(color)
                self.score = 0
                
                self.font = pygame.font.Font(None, 36)
                self.render_text()
                self.rect = self.image.get_rect()
                self.rect.center = position
                
        def render_text(self):
                self.image = self.font.render("SCORE: {0}".format(self.score), True, self.color)
                
        def increase(self):
                self.score += 1
                self.render_text()

                
                
                
class life(Sprite):
        """
        Displays score.
        """
        def __init__(self, color, position):
                #call constructor parent
                pygame.sprite.Sprite.__init__(self)
                self.color = pygame.Color(color)
                self.life = 100
                
                self.font = pygame.font.Font(None, 36)
                self.render_text()
                self.rect = self.image.get_rect()
                self.rect.center = position
                
        def render_text(self):
                self.image = self.font.render("LIFE: {0}%".format(self.life), True, self.color)
                
        def die(self):
                self.life -= 1
                self.render_text()
                
class endgame(Sprite):
        """
        Show Game Over
        """
        def __init__(self, color, position):
                #call constructor parent
                pygame.sprite.Sprite.__init__(self)
                self.color = pygame.Color(color)

                self.font = pygame.font.Font(None, 36)
                self.render_text()
                self.rect = self.image.get_rect()
                self.rect.center = position
                
        def render_text(self):
                self.image = self.font.render("GAME OVER", True, self.color)


#END OF SPRITES----------------------------------------------------





# define a main function
def main():
        # create a screen surface of a given size
        screen = pygame.display.set_mode((800,480))
        # set window caption
        pygame.display.set_caption("Jump")
        # control variable for the main loop
        running = True
        # main game loop
        
        background = pygame.Surface([800, 480])
        background.fill(pygame.Color("light blue"))
        for y in range(0, 240, 10):
                rectangle = pygame.Rect(0, 280, 800, 200)
                pygame.draw.rect(background, pygame.Color("dark green"), rectangle)
        
        # draw background on screen
        screen.blit(background, (0, 0))
        pygame.font.init()
        points = score("black", (100,50))
        gameover = endgame("white", (400, 250))
        health = life("red", (700,50))
        obstacle = obstacles("black", (300, 650), points)
        player = character("red", (400, 240), obstacle, health, gameover)
        sprites = pygame.sprite.RenderPlain([player, obstacle, points, health])
        
        
        # display screen surface
        pygame.display.flip()
        running = True

#KEY MAPS----------------------------------------------------------

        key_map = {
                pygame.K_LEFT: [player.left, player.right],
                pygame.K_RIGHT: [player.right, player.left],
                pygame.K_UP: [player.up, player.down]
        }

#END OF KEY MAPS---------------------------------------------------
        
        clock = pygame.time.Clock()
        
        while running:
        
                clock.tick(60)
                pygame.display.set_caption("JUMP - {0:.2f} fps".format(clock.get_fps()))
        
                sprites.update()
                sprites.draw(screen)
                pygame.display.flip()
                sprites.clear(screen, background)
                # read events from the event queue
                for event in pygame.event.get():
                        # on QUIT event, exit the main loop
                        if event.type == pygame.QUIT:
                                running = False
                                
                        elif event.type == pygame.KEYDOWN and event.key in key_map:
                                key_map[event.key][0]()
                        elif event.type == pygame.KEYUP and event.key in key_map:
                                key_map[event.key][1]()
                                
                if health.life <= 0 :        
                        sprites = pygame.sprite.RenderPlain([gameover, points])
                               
                                
# if this module is executed as a script, run the main function
if __name__ == "__main__":
        main()
