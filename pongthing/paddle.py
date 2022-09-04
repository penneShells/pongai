import pygame
black = [0, 0, 0]

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        #calls the sprite constructor
        super().__init__()

        #give paddle dimensions and make background transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)

        #draw it
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
      
    def moveDown(self, pixels):
        self.rect.y += pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y > 400:
          self.rect.y = 400
