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

    def randomize_fruit(self):
        self.x = random.randint(0, cellnumber - 1)
        self.y = random.randint(0, cellnumber - 1)
        self.pos = Vector2(self.x, self.y)


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

    def change_direction(self, direction):
        if self.direction.x != direction.x and self.direction.y != direction.y:
            self.direction = direction

    def grow(self):
        self.body.insert(len(self.body) - 1, self.body[-1])


class Main:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
    
    def update(self):
        self.snake.move_snake()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

# pygame setup
pygame.init()
cellsize = 40
cellnumber = 20
screen = pygame.display.set_mode((cellsize * cellnumber, cellsize * cellnumber))

clock = pygame.time.Clock()
running = True


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                main_game.snake.change_direction(Vector2(0,1))
            elif event.key == pygame.K_UP:
                main_game.snake.change_direction(Vector2(0,-1))
            elif event.key == pygame.K_LEFT:
                main_game.snake.change_direction(Vector2(-1,0))
            elif event.key == pygame.K_RIGHT:
                main_game.snake.change_direction(Vector2(1,0))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((175, 215,70))

    # RENDER YOUR GAME HERE
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
sys.exit