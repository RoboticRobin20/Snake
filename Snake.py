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
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize_fruit(self):
        self.x = random.randint(0, cellnumber - 1)
        self.y = random.randint(0, cellnumber - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        # Load Snake Head Graphics
        self.snake_head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.snake_head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.snake_head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.snake_head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()

        # Load Snake Tail Graphics
        self.snake_tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.snake_tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.snake_tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.snake_tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()

        # Load Snake Straight Body Graphics
        self.snake_body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.snake_body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()

        # Load Snake Turned Body Graphics
        self.snake_body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.snake_body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.snake_body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.snake_body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()


    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cellsize)
            y_pos = int(block.y * cellsize)
            snake_rect = pygame.Rect(x_pos, y_pos, cellsize, cellsize)
            
            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rect)
            else: 
                self.update_body_graphics(index)
                screen.blit(self.snake_body, snake_rect)    
                
    def update_head_graphics(self):
        self.head_relation = self.body[0] - self.body[1]
        if self.head_relation == Vector2(1,0): self.head = self.snake_head_right
        elif self.head_relation == Vector2(-1,0): self.head = self.snake_head_left
        elif self.head_relation == Vector2(0,-1): self.head = self.snake_head_up
        elif self.head_relation == Vector2(0,1): self.head = self.snake_head_down
    
    def update_tail_graphics(self):
        self.tail_relation = self.body[-1] - self.body[-2]
        if self.tail_relation == Vector2(0,1): self.tail = self.snake_tail_down
        elif self.tail_relation == Vector2(0,-1): self.tail = self.snake_tail_up
        elif self.tail_relation == Vector2(1,0): self.tail = self.snake_tail_right
        elif self.tail_relation == Vector2(-1,0): self.tail = self.snake_tail_left
        
    def update_body_graphics(self, index):
        print('updating body graphics', index)
        self.previous_block = self.body[index + 1] - self.body[index]
        self.next_block = self.body[index - 1] - self.body[index]
        # pygame.draw.rect(screen,(150,100,100),snake_rect)
        if self.previous_block.x == self.next_block.x:
            self.snake_body = self.snake_body_vertical
        elif self.previous_block.y == self.next_block.y:
            self.snake_body = self.snake_body_horizontal
        else:
            if self.previous_block.y == -1 and self.next_block.x == -1 or self.next_block.y == -1 and self.previous_block.x == -1:
                self.snake_body = self.snake_body_tl
            elif self.previous_block.y == -1 and self.next_block.x == 1 or self.next_block.y == -1 and self.previous_block.x == 1:
                self.snake_body = self.snake_body_tr
            elif self.previous_block.y == 1 and self.next_block.x == 1 or self.next_block.y == 1 and self.previous_block.x == 1:
                self.snake_body = self.snake_body_br
            elif self.previous_block.y == 0 and self.next_block.x == 0 or self.next_block.y == 0 and self.previous_block.x == 0:
                self.snake_body = self.snake_body_bl
        
    
    def move_snake(self):
        if self.new_block is True:
            body_copy = self.body[:]
            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy

    def change_direction(self, direction):
        if self.direction.x != direction.x and self.direction.y != direction.y:
            self.direction = direction

    def add_block(self):
        self.new_block = True
        # self.body.insert(len(self.body) - 1, self.body[-1])


class Main:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_failure()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize_fruit()
            while self.fruit.pos in self.snake.body[1:]:
                self.fruit.randomize_fruit()
            self.snake.add_block()
    
    def check_failure(self):
        if not 0 <= self.snake.body[0].x <= cellnumber or not 0 <= self.snake.body[0].y <= cellnumber:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


# pygame setup
pygame.init()
cellsize = 40
cellnumber = 20
screen = pygame.display.set_mode((cellsize * cellnumber, cellsize * cellnumber))
clock = pygame.time.Clock()

# Load Apple Graphic
apple = pygame.image.load('Graphics/apple.png').convert_alpha()

running = True


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 1000)

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