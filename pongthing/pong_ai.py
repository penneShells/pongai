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

def main(genomes, config):
    black = (0,0,0)
    white = (255, 255, 255)
    all_sprites_list = pygame.sprite.Group()

    #Make window
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong Time")


    pygame.init()
    paddles = []
    nets = []
    ge = []
    balls = []
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
        ball = Ball(white,10,10)
        balls.append(ball)
        ball.rect.x = 345
        ball.rect.y = 195
        all_sprites_list.add(ball)

    mainLoop = True

    #basically just fps control
    clock = pygame.time.Clock()

    #main loop
    while mainLoop == True and len(paddles) != 0 and count != 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                         carryOn=False

        #Check if the ball is bouncing against any of the 4 walls:
        for ball in balls:
            if ball.rect.x>=690:
                ball.rect.x = 345
                ball.rect.y = 195
                ball.velocity[0] = -ball.velocity[0]
                counter[balls.index(ball)] += 1
            for x, count in enumerate(counter):
                if counter[x] == 1:
                    counter.pop(x)
                    paddles.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                    all_sprites_list.remove(x)
                    balls.pop(x)
            if ball.rect.x<=0:
                ball.rect.x = 345
                ball.rect.y = 195
                ball.velocity[0] = -ball.velocity[0]
                
            if ball.rect.y>490:
                ball.velocity[1] = -ball.velocity[1]
            if ball.rect.y<0:
                ball.velocity[1] = -ball.velocity[1]
           

        for x, ball in enumerate(balls):
                   
            if pygame.sprite.collide_mask(balls[x], paddles[x]):
                ge[x].fitness += 10
                ball.bounce()
                       
        for x, paddle in enumerate(paddles):
            ge[x].fitness += 0.1
           
            output = nets[paddles.index(paddle)].activate((paddles[x].rect.y, balls[x].rect.x, balls[x].rect.y))
            if output[0] > 0.5:
                paddle.moveUp(1)
            if output[1] > 0.5:
                paddle.moveDown(1)

        #drawing things goes here
        screen.fill(black)
        pygame.draw.line(screen, white, [349, 0], [349, 500], 5)
        #draw them sprites
        all_sprites_list.draw(screen)
       

        #update screen
        pygame.display.flip()

        #60 fps
        clock.tick(60)
        all_sprites_list.update()
    pygame.quit()


#loads in config file and such
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
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close
   
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)


