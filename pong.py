# import the pygame module, so you can use it
import pygame
import random

from pygame.sprite import Sprite
class Ball(Sprite):

        def __init__(self, color, position):
                # call parent class constructor
                Sprite.__init__(self)
                # create surface
                self.image = pygame.Surface([6, 6])
                # draw filled circle
                pygame.draw.circle(self.image, pygame.Color(color), (3,3), 3)
                # get sprite bounding box
                self.rect = self.image.get_rect()
                # set sprite initial position
                self.rect.center = position
        def update(self):
                x = random.randint(-3,3)
                y = random.randint(-3,3)
                self.rect.move_ip(x, y)
                
                
class Racket(Sprite):

        def __init__(self, color, position):
                Sprite.__init__(self)
                self.image = pygame.Surface([4, 20])
                self.rect = pygame.Rect(0, 0, 4, 20) # (x, y, width, height)
                pygame.draw.rect(self.image, pygame.Color(color), self.rect)
                self.rect.center = position
        def update(self):
                y = random.randint(-10,10)
                self.rect.move_ip(0, y)

# define a main function
def main():
        # create a screen surface of a given size
        screen = pygame.display.set_mode((320,240))
        # set window caption
        pygame.display.set_caption("PONG")
        # create background surface
        background = pygame.Surface([320, 240])
        background.fill(pygame.Color("black"))
        for y in range(0, 240, 10):
                pygame.draw.line(background, pygame.Color("white"), (160,y), (160,y+3))
        # draw background on screen
        screen.blit(background, (0, 0))
        # create the ball sprite
        ball = Ball("white", (160,120))
        # create two racket sprites
        player1 = Racket("green", (10, 120))
        player2 = Racket("orange", (310, 120))
        # list of sprites to render
        sprites = pygame.sprite.RenderPlain([ball, player1, player2])
        # display screen surface
        pygame.display.flip()
        # control variable for the main loop
        running = True
        # clock to control the game frame rate
        clock = pygame.time.Clock()
        # main game loop
        while running:
                # set game frame rate
                clock.tick(10)
                pygame.display.set_caption("PONG - {0:.2f} fps".format(clock.get_fps()))
                # animate sprites
                sprites.update()
                sprites.draw(screen)
                # display screen
                pygame.display.flip()
                # draw background over sprites
                sprites.clear(screen, background)
                # read events from the event queue
                for event in pygame.event.get():
                        # on QUIT event, exit the main loop
                        if event.type == pygame.QUIT:
                                running = False
# if this module is executed as a script, run the main function
if __name__ == "__main__":
        main()