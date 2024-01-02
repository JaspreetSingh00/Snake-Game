from tkinter import *
import random

# *************** Game Backbone


BACKGROUND_COLOR = '#0A0A0A'

window = Tk()
window.title('Snake Game')
window.resizable(False, False)

canvas = None

def start_game():
    global canvas

    canvas = Canvas(window,
                    bg=BACKGROUND_COLOR,
                    width=GRID_SIZE[0] * SQUARE_SIZE, height=GRID_SIZE[1] * SQUARE_SIZE)
    canvas.pack()

    game_loop()

    window.mainloop()


def update_elements():
    snake_step()

def check_collisions():
    check_snake_collisions()
    check_food_collision()

def draw_elements():
    canvas.delete('all')

    draw_grid()
    draw_snake()
    draw_food()

check_game_running = True

game_speed = 3

def game_over():
    canvas.delete("all")

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    canvas.create_text(
        canvas_width/2.0,
        canvas_height/2.0,
        text="Game Over",
        font=("consolas", 80),
        fill="#F12A00")

def game_loop():
    update_elements()
    check_collisions()
    draw_elements()

    if check_game_running:
        update_time = int(1000 / game_speed)
        window.after(update_time, game_loop)
    else:
        game_over()


# *************** Grid ******************

GRID_COLOR = '#FFFFFF'

GRID_SIZE = (10, 10)
SQUARE_SIZE = 70

def draw_grid():
    global canvas

    canvas_width = GRID_SIZE[0] * SQUARE_SIZE
    canvas_height = GRID_SIZE[1] * SQUARE_SIZE

    for i_x in range(GRID_SIZE[0]):
        x_pos = i_x * SQUARE_SIZE
        canvas.create_line(x_pos, 0, x_pos, canvas_height, width=1, fill=GRID_COLOR)

    for i_y in range(GRID_SIZE[1]):
        y_pos = i_y * SQUARE_SIZE
        canvas.create_line(0, y_pos, canvas_width, y_pos, width=1, fill=GRID_COLOR)


# *************** Snake 


SNAKE_COLOR = "#82DE89"

snake_coordinates = [(0, 0), (0, 0), (0, 0)]

next_direction = "down"
cur_dir = "down"


def snake_step():
    global snake_coordinates, cur_dir

    head = snake_coordinates[0]
    snake_coordinates = snake_coordinates[:-1]

    new_head = None
    if next_direction == "down":
        new_head = (head[0], head[1] + 1)
    elif next_direction == "up":
        new_head = (head[0], head[1] - 1)
    elif next_direction == "left":
        new_head = (head[0] - 1, head[1])
    elif next_direction == "right":
        new_head = (head[0] + 1, head[1])

    snake_coordinates.insert(0, new_head)
    cur_dir = next_direction

def draw_snake():
    global canvas
    for x, y in snake_coordinates:
        x_1 = x * SQUARE_SIZE
        y_1 = y * SQUARE_SIZE

        x_2 = (x + 1) * SQUARE_SIZE
        y_2 = (y + 1) * SQUARE_SIZE

        canvas.create_rectangle(x_1, y_1, x_2, y_2, fill=SNAKE_COLOR)

def check_snake_collisions():
    global check_game_running

    head = snake_coordinates[0]
    head_x = head[0]
    head_y = head[1]

    grid_size_x = GRID_SIZE[0]
    grid_size_y = GRID_SIZE[1]

    if head_x < 0 or head_x >= grid_size_x or head_y < 0 or head_y >= grid_size_y:
        check_game_running = False

    if head in snake_coordinates[1:]:
        check_game_running = False

def change_direction(new_direction):
    # Change the current direction of the snake based on
    # the player input
    global next_direction

    if (new_direction == "up" and cur_dir == "down") or \
            (new_direction == "down" and cur_dir == "up") or \
            (new_direction == "left" and cur_dir == "right") or \
            (new_direction == "right" and cur_dir == "left"):
        return

    next_direction = new_direction


# bind the arrow keys to the change direction function
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


# *************** Food 


# Variables
FOOD_COLOR = "#F12A01"

food_position = (0, 0)


def move_food():
    # Change the current position of the food
    global food_position
    new_x = random.randint(0, GRID_SIZE[0] - 1)
    new_y = random.randint(0, GRID_SIZE[1] - 1)

    food_position = (new_x, new_y)

    if food_position in snake_coordinates:
        move_food()

move_food()

def check_food_collision():
    # Check if the snake has eaten the food
    head = snake_coordinates[0]

    if head == food_position:
        move_food()
        increase_score()
        snake_coordinates.append(snake_coordinates[-1])

def draw_food():
    # Draw the food on the canvas
    x_1 = food_position[0] * SQUARE_SIZE
    y_1 = food_position[1] * SQUARE_SIZE
    x_2 = (food_position[0] + 1) * SQUARE_SIZE
    y_2 = (food_position[1] + 1) * SQUARE_SIZE

    canvas.create_rectangle(x_1, y_1, x_2, y_2, fill=FOOD_COLOR)



# *************** Score 


# Variables
score = 0

# Create score Label
label = Label(window, text="Score: {}".format(score), font=('Consolas', 40))
label.pack()


def increase_score():
    # Increase the current score and apply changes to the game
    #  - Update the score label
    #  - Update the game speed
    global score, game_speed
    score = score + 1

    label.config(text="SCORE: {}".format(score))

    game_speed = game_speed + 0.25



if __name__ == '__main__':
    start_game()

