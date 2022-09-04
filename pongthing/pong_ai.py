import pygame
import random
import os
import time
import neat
import visualize
import pickle
from paddle import Paddle
from ball import Ball
pygame.init()

black = (0,0,0)
white = (255, 255, 255)

#Make window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong Time")


def main(genomes, config):

    paddles = []
    
    wall = Paddle(white, 10, 10000)
    wall.rect.x = 20
    wall.rect.y = 0
     
    paddleB = Paddle(white, 10, 100)
    paddleB.rect.x = 670
    paddleB.rect.y = 200

    ball = Ball(white,10,10)
    ball.rect.x = 345
    ball.rect.y = 195


    '''
    paddleC = Paddle(white, 10, 100)
    paddleC.rect.x = 670
    paddleC.rect.y = 200
    '''
    all_sprites_list = pygame.sprite.Group()

    all_sprites_list.add(wall)
    all_sprites_list.add(paddleB)
    all_sprites_list.add(ball)
    #all_sprites_list.add(paddleC)
    #more than one paddle per side works
    #loop for main game not just single player
    mainLoop = True

    #basically just fps control
    clock = pygame.time.Clock()

    scoreA = 0
    scoreB = 0

    #main loop
    while mainLoop == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                         carryOn=False
     
        #Moving the paddles when the user uses the arrow keys (player A) or "W/S" keys (player B) 
        keys = pygame.key.get_pressed()
        '''
        if keys[pygame.K_w]:
            wall.moveUp(5)
        if keys[pygame.K_s]:
            wall.moveDown(5)
        if keys[pygame.K_UP]:
            paddleB.moveUp(5)
        if keys[pygame.K_DOWN]:
            paddleB.moveDown(5)  
        #game logic goes here
        all_sprites_list.update()
        '''
        #Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x>=690:
            scoreA+=1
            ball.rect.x = 345
            ball.rect.y = 195
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x<=0:
            scoreB+=1
            ball.rect.x = 345
            ball.rect.y = 195
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y>490:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y<0:
            ball.velocity[1] = -ball.velocity[1]

        if pygame.sprite.collide_mask(ball, wall) or pygame.sprite.collide_mask(ball, paddleB):
          ball.bounce()


        #drawing things goes here
        screen.fill(black)
        pygame.draw.line(screen, white, [349, 0], [349, 500], 5)
        #draw them sprites
        all_sprites_list.draw(screen)

        #Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(scoreA), 1, white)
        screen.blit(text, (250,10))
        text = font.render(str(scoreB), 1, white)
        screen.blit(text, (420,10))
        
        #update screen
        pygame.display.flip()

        #60 fps
        clock.tick(60)

    pygame.quit()
main()

#loads in config file and such
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(Config)
    #gives info about gen
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)


