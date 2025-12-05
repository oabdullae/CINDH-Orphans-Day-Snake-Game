import pygame
import pdb
import random

pygame.init()

WIDTH = 900
HEIGHT = 900
PLAYGROUND_DIM = 810 # to divide by 30 cols and rows 
PLAYGROUND_BOXES = 18
BOX_SIZE = 45

TOPRIGHT = 46 # both col and row have same value 46

PADDING = 40
BORDER_THICKNESS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
#GRASS_GREEN = (34, 139, 34) # playground color
GRASS_GREEN = (24, 97, 24) # playground color
CHERRY_RED = (255, 0, 80) # snake color
SUPERMAN_RED = (229, 35, 46) # superman snake red
SUPERMAN_BLUE = (4, 114, 179) # superman snake blue
BG_CLR = (32, 32, 32) # temporary color

TIMEOUT = 8000 # 8 seconds

screen = pygame.display.set_mode((WIDTH, HEIGHT));
clock = pygame.time.Clock()

running = True

def draw_border(top_left, top_right, bottom_left, bottom_right):
     # upper border
    pygame.draw.line(screen, WHITE, top_left, top_right, BORDER_THICKNESS)
     # lower border
    pygame.draw.line(screen, WHITE, bottom_left, bottom_right, BORDER_THICKNESS)
     # left border
    pygame.draw.line(screen, WHITE, top_left, bottom_left, BORDER_THICKNESS)
     # right border
    pygame.draw.line(screen, WHITE, top_right, bottom_right, BORDER_THICKNESS)

def draw_grid():
    for i in range(PLAYGROUND_BOXES):
        pygame.draw.line(
            screen,
            GRASS_GREEN, 
            (TOPRIGHT + BOX_SIZE * i, TOPRIGHT),
            (
                TOPRIGHT + BOX_SIZE * i,
                TOPRIGHT * BOX_SIZE*PLAYGROUND_BOXES
            )
        )
    for i in range(PLAYGROUND_BOXES):
        pygame.draw.line(
            screen, 
            GRASS_GREEN, 
            (TOPRIGHT, TOPRIGHT + BOX_SIZE * i), 
            (
                TOPRIGHT + BOX_SIZE * PLAYGROUND_BOXES,
                TOPRIGHT + BOX_SIZE * i
            )
        )

"""
def shift_body_block(block, direction):
    match direction:
        case "UP":
            
        case "DOWN":

        case "RIGHT":

        case "LEFT":
"""

# ---

def draw_snake_body_block(block, is_head):
    pygame.draw.rect(screen, SUPERMAN_BLUE, block)
    pygame.draw.rect(screen, SUPERMAN_BLUE, block)
    if is_head:
        pygame.draw.rect(screen, SUPERMAN_RED, pygame.Rect(block.x + 10, block.y + 10, BOX_SIZE - 20, BOX_SIZE - 20))

    # TODO internal rect for later
    """
    inner_block = pygame.Rect(block.x + 10, block.y + 10, BOX_SIZE - 1*2 - 10*2, BOX_SIZE - 1*2 - 10*2)
    pygame.draw.rect(screen, SUPERMAN_RED, inner_block)
    """

# ---

def update_snake(snake_body, direction):
    # is the snake gonna eat

    snake_ate = False
    # delete tail snake_body[-1] if snake didnt eat
    if not snake_ate:
        # delete tail snake_body[-1]
        pygame.draw.rect(screen, BG_CLR, snake_body[-1])
        snake_body.pop(-1)
    else:
        pass # keep tail if snake ate

    

    # add a new block in front of the head if there is no collision
    new_block = None
    match direction:
        case "UP":
            new_block = pygame.Rect(
                snake_body[0].x,
                snake_body[0].y - BOX_SIZE,
                BOX_SIZE,
                BOX_SIZE
            )
        case "DOWN":
            new_block = pygame.Rect(
                snake_body[0].x,
                snake_body[0].y + BOX_SIZE,
                BOX_SIZE,
                BOX_SIZE
            )

        case "LEFT":
            new_block = pygame.Rect(
                snake_body[0].x - BOX_SIZE,
                snake_body[0].y,
                BOX_SIZE,
                BOX_SIZE
            )

        case "RIGHT":
            new_block = pygame.Rect(
                snake_body[0].x + BOX_SIZE,
                snake_body[0].y,
                BOX_SIZE,
                BOX_SIZE
            )
        
    # detect wall collisions
    if new_block.x not in range(TOPRIGHT, TOPRIGHT + (PLAYGROUND_BOXES * BOX_SIZE)):
        return False # There is a collision
    if new_block.y not in range(TOPRIGHT, TOPRIGHT + (PLAYGROUND_BOXES * BOX_SIZE)):
        return False # There is a collision

    # detect body collisions
    for i in range(len(snake_body)):
        if snake_body[i].x == new_block.x and snake_body[i].y == new_block.y:
            return False

    snake_body.insert(0, new_block)
    draw_snake_body_block(snake_body[0], True)
    draw_snake_body_block(snake_body[1], False)
    return True

# ---

def draw_food(col, row):
    # temp draw food
    egg = pygame.Rect(col + 5, row + 5, 35, 35)
    pygame.draw.rect(screen, WHITE, egg)
    return egg

# ---

def spawn_food(free_boxes):
    random_flat_coords = random.choice(free_boxes)
    j = random_flat_coords % PLAYGROUND_BOXES
    i = (random_flat_coords - j) // PLAYGROUND_BOXES
    food_rect = draw_food(TOPRIGHT + j * BOX_SIZE, TOPRIGHT + i * BOX_SIZE)
    free_boxes.remove(random_flat_coords)
    return random_flat_coords, food_rect

# ---

def block_to_flat_coords(block):
    i = (block.y - TOPRIGHT) // BOX_SIZE
    j = (block.x - TOPRIGHT) // BOX_SIZE
    return PLAYGROUND_BOXES * i + j

# ---

def clear_old_food(flat_coords, free_boxes):
    j = flat_coords % PLAYGROUND_BOXES
    i = (flat_coords - j) // PLAYGROUND_BOXES
    cleared = pygame.Rect(TOPRIGHT + j * BOX_SIZE, TOPRIGHT + i * BOX_SIZE, BOX_SIZE, 
        BOX_SIZE)
    pygame.draw.rect(screen, BG_CLR, cleared)
    free_boxes.append(flat_coords)
    
# ---

first_body_block = pygame.Rect(
    #TOPRIGHT + BOX_SIZE * ((PLAYGROUND_BOXES-1)//2),
    #TOPRIGHT+ BOX_SIZE *((PLAYGROUND_BOXES-1)//2),
    TOPRIGHT + BOX_SIZE * 8,
    TOPRIGHT+ BOX_SIZE * 8,
    BOX_SIZE,
    BOX_SIZE
)
"""
second_body_block = pygame.Rect(
    first_body_block.x + BOX_SIZE,
    first_body_block.y, 
    BOX_SIZE, 
    BOX_SIZE
)
third_body_block = pygame.Rect(
    first_body_block.x + BOX_SIZE * 2,
    first_body_block.y, 
    BOX_SIZE, 
    BOX_SIZE
)
"""

# initialize free boxes as the whole grid being free
free_boxes = []
for i in range(18*18):
    free_boxes.append(i)


# initialize snake body
snake_body = [first_body_block]
for i in range(1, 6):
    body_block = pygame.Rect(
        first_body_block.x + BOX_SIZE * i,
        first_body_block.y,
        BOX_SIZE,
        BOX_SIZE
    )
    snake_body.append(body_block)
# snake_body = [first_body_block, second_body_block, third_body_block]
snake_direction = "LEFT"

for i in range(len(snake_body)):
    free_boxes.remove(block_to_flat_coords(snake_body[i]))



# Define the box properties (e.g., a 100x100 square starting at 50, 50)
size = 810
playground = pygame.Rect(46, 46, size, size)
# Draw the box using the Rect object
pygame.draw.rect(screen, BG_CLR, playground)

food_flat_coords, food_rect = spawn_food(free_boxes)
food_timeout = 0

pygame.display.flip()
# MAIN LOOP
while running:
    # pdb.set_trace()
    arrow_key_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake_direction != "DOWN":
                    arrow_key_pressed = True
                    snake_direction = "UP"
                    if not update_snake(snake_body, "UP"):
                        running = False
            if event.key == pygame.K_DOWN:
                if snake_direction != "UP":
                    arrow_key_pressed = True
                    snake_direction = "DOWN"
                    if not update_snake(snake_body, "DOWN"):
                        running = False
            if event.key == pygame.K_RIGHT:
                if snake_direction != "LEFT":
                    arrow_key_pressed = True
                    snake_direction = "RIGHT"
                    if not update_snake(snake_body, "RIGHT"):
                        running = False
            if event.key == pygame.K_LEFT:
                if snake_direction != "RIGHT":
                    arrow_key_pressed = True
                    snake_direction = "LEFT"
                    if not update_snake(snake_body, "LEFT"):
                        running = False
    # screen.fill(BLACK) # to change later for only deleting the relevant parts
    if not arrow_key_pressed:
        if not update_snake(snake_body, snake_direction):
            running = False
            continue
        pass


    draw_border(
        (PADDING, PADDING),
        (WIDTH - PADDING, PADDING),
        (PADDING, HEIGHT - PADDING),
        (WIDTH - PADDING, HEIGHT - PADDING)
    )
    """ Draws lil red border
    pygame.draw.line(screen, RED, (PADDING, PADDING),
        (WIDTH - PADDING, PADDING), 1)
    pygame.draw.line(screen, RED, (PADDING, HEIGHT- PADDING),
        (WIDTH - PADDING, HEIGHT - PADDING), 1)
    pygame.draw.line(screen, RED, (PADDING, PADDING),
        (PADDING, HEIGHT - PADDING), 1)
    pygame.draw.line(screen, RED, (WIDTH - PADDING, PADDING),
        (WIDTH - PADDING, HEIGHT - PADDING), 1)
    """
    """
    for i in range(18):
        snake = pygame.Rect(TOPRIGHT + i*BOX_SIZE,TOPRIGHT, BOX_SIZE, BOX_SIZE)
        pygame.draw.rect(screen, SUPERMAN_RED, snake)
        #inner_snake = pygame.Rect(46+1 + 10 + i*BOX_SIZE, 46+1 + 10, BOX_SIZE -2 - 20, BOX_SIZE -2- 20)
        #pygame.draw.rect(screen, SUPERMAN_BLUE, inner_snake)
    """
    
    #snake1 = pygame.Rect(47+27, 47, 25, 25)
    #pygame.draw.rect(screen, CHERRY_RED, snake1)
    #pygame.draw.rect(screen, BLACK, snake_body[0]);
    #pygame.draw.rect(screen, BLACK, snake_body[1]);

    # print snake
    for i in range(len(snake_body)):
        is_head = False
        if i == 0:
            is_head = True
        draw_snake_body_block(snake_body[i], is_head)
    """
    r = pygame.Rect(TOPRIGHT, TOPRIGHT, BOX_SIZE, BOX_SIZE)
    pygame.draw.rect(screen, SUPERMAN_BLUE, r) 
    """


    draw_grid()
    pygame.display.flip() # refresh equivalent

    dt = clock.tick(3)
    food_timeout += dt
    if food_timeout >= TIMEOUT:
        food_timeout -= TIMEOUT
        # respawn food somewhere else
        clear_old_food(food_flat_coords, free_boxes)
        food_flat_coords, food_rect = spawn_food(free_boxes)


pygame.quit()
