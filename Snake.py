import sys, pygame, random
from pygame.math import Vector2


class Fruit:
    def __init__(self):
        # create x and y position
        self.x = random.randint(0, cellnumber - 1)
        self.y = random.randint(0, cellnumber - 1)
        self.pos = Vector2(self.x, self.y)
    
    # draw a square
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cellsize), int(self.pos.y * cellsize), cellsize, cellsize)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)


class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        self.direction = Vector2(1,0)

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cellsize)
            y_pos = int(block.y * cellsize)
            fruit_rect = pygame.Rect(x_pos, y_pos, cellsize, cellsize)
            pygame.draw.rect(screen, pygame.Color('orange'), fruit_rect)
    
    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy

# pygame setup
pygame.init()
cellsize = 40
cellnumber = 20
screen = pygame.display.set_mode((cellsize * cellnumber, cellsize * cellnumber))

clock = pygame.time.Clock()
running = True

fruit = Fruit()
snake = Snake()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((175, 215,70))
    fruit.draw_fruit()
    snake.draw_snake()

    # RENDER YOUR GAME HERE
    pygame.display.update()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
sys.exit