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

paddleA = Paddle(white, 10, 10000000)
paddleA.rect.x = 20
paddleA.rect.y = 0
 '''
paddleB = Paddle(white, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200'''

ball = Ball(white,10,10)
ball.rect.x = 345
ball.rect.y = 195


all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(paddleA)

all_sprites_list.add(ball)
#all_sprites_list.add(paddleC)
#more than one paddle per side works
#loop for main game not just single player
mainLoop = True

#basically just fps control
clock = pygame.time.Clock()

scoreA = 0
scoreB = 0

def main(genomes, config):
    
    paddles = []
    ge = []
    nets = []
    counter = []
    
    for genome_id, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        paddles.append(Paddle(white, 10, 100))
        ge.append(g)
       
    for paddle in paddles:
        paddle.rect.x = 670
        paddle.rect.y = 200
        all_sprites_list.add(paddle)
        count = 0
        counter.append(count)
    
    
    #main loop
    while mainLoop == True and len(paddles) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                         carryOn=False
     
        #Moving the paddles when the user uses the arrow keys (player A) or "W/S" keys (player B) 
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddleA.moveUp(5)
        if keys[pygame.K_s]:
            paddleA.moveDown(5)
        if keys[pygame.K_UP]:
            paddleB.moveUp(5)
        if keys[pygame.K_DOWN]:
            paddleB.moveDown(5)  
        '''
        #game logic goes here
            
        all_sprites_list.update()
        #Check if the ball is bouncing against any of the 4 walls:
        
        if ball.rect.x>=690:
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
        
        for paddle in paddles:
            #this might resolve those fucking issues so remember what this does and also dont submit this homework with this comment still here itll look bad
            if pygame.sprite.collide_mask(ball, paddleA):
                ball.bounce()
               
            if pygame.sprite.collide_mask(ball, paddle):
                goodOne = paddles.index(paddle)
                for paddle in paddles:
                    if goodOne != paddles.index(paddle):
                        ge.fitness[paddles.index(paddle)] -= 2
                        counter[paddles.index(paddle)] += 1
                        goodOne = None
                    if goodOne == paddles.index(paddle):
                        ge[paddles.index(paddle)].fitness += 5
                    if counter[paddles.index(paddle)] == 5:
                        paddles.pop(paddles.index(paddle))
                        ge.pop(paddles.index(paddle))
                        nets.pop(paddles.index(paddle))
                ball.bounce()
               

        #output input ai stuff
        for x, paddle in enumerate(paddles):
            ge[x].fitness += 0.1
           
            output = nets[paddles.index(paddle)].activate((paddles[x].rect.y, ball.rect.x, ball.rect.y))
            if output[0] > 0.5:
                paddle.moveUp(1)
            if output[1] > 0.5:
                paddle.moveDown(1)

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

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)
    #gives info about gen
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)
   
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

