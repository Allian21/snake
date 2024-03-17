import turtle
import time
import random
import os


delay = 0.1

#Input
name = input("Enter your name: ")


score = 0

#window
wn = turtle.Screen()
wn.title("Slithering Serpent: The Ultimate Snake Adventure")
wn.setup(width=800, height=800)
wn.tracer(0)

#score file
SCORES_FILE = "Snake game 2\score.txt"

#update score
def update_score(name, score):
    try:
        scores = {}
        with open(SCORES_FILE, "r") as file:
            for line in file:
                n, s = line.strip().split(", ")
                s = int(''.join(filter(str.isdigit, s)))  # Extract only digits from the score string
                scores[n] = s

        with open(SCORES_FILE, "w") as file:
            scores[name] = max(scores.get(name, 0), score)  # Update score if higher
            for n, s in scores.items():
                file.write(f"{n}, ({s})\n")
    except IOError as e:
        print(f"Error writing to scores file: {e}")





def get_scores():
    scores = []
    with open(SCORES_FILE, "r") as file:
        for line in file:
            name, score_str = line.strip().split(",")
            score_digits = ''.join(char for char in score_str if char.isdigit())  # Extract only digits from the score string
            score = int(score_digits)  # Convert the extracted digits to an integer
            scores.append((name, score))
    return scores



def display_scores():
    scores = get_scores()

    print("Scores:")
    for name, score in scores:
        print(f"{name}: {score}")

    print("\nPress 'q' to quit")

    
    wn.listen()
    wn.onkeypress(bye, 'q')

    wn.mainloop()  




# Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("blue")
head.penup()
head.goto(0, 0)
head.direction = 'stop'
head.hideturtle()

# Snake Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)
food.hideturtle()

# Shrinking Food
shrink_food = turtle.Turtle()
shrink_food.speed(0)
shrink_food.shape("circle")
shrink_food.color("#FF5733")  
shrink_food.penup()
shrink_food.goto(0, -100)
shrink_food.hideturtle()

# Score Board
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()
pen.shape('square')
pen.color('black')
pen.goto(0, 360)
pen.write("Score: 0", align='center', font=('Arial', 24, 'normal'))  

#for the body
segments = []

#Game State(menu/intro, ingame)
game_state = 'intro'  # menu

#start game and movements
def start_game():
    global game_state
    game_state = 'ingame'

def go_up():
    if head.direction != 'down':
        head.direction = 'up'

def go_down():
    if head.direction != 'up':
        head.direction = 'down'

def go_right():
    if head.direction != 'left':
        head.direction = 'right'

def go_left():
    if head.direction != 'right':
        head.direction = 'left'

def move():
    if head.direction == 'up':
        head.sety(head.ycor() + 20)
    if head.direction == 'down':
        head.sety(head.ycor() - 20)
    if head.direction == 'right':
        head.setx(head.xcor() + 20)
    if head.direction == 'left':
        head.setx(head.xcor() - 20)

#game over
def game_over():
    global delay, score, segments
    head.direction = 'stop'
    time.sleep(1)
    for segment in segments:
        segment.goto(2000, 2000)
    segments.clear()
    head.goto(0, 0)
    score_write()
    print("Game Over!")

    
    pen.clear()
    pen.goto(0, 0)
    pen.write("Game Over!\nPress 'q' to quit or 's' to view scores", align='center', font=('Arial', 20, 'normal'))
    wn.update()  

    
    while True:
        choice = wn.textinput("Game Over!", "Press 'q' to quit or 's' to view scores")
        if choice and choice.lower() == 'q':
            bye()
            break
        elif choice and choice.lower() == 's':
            display_scores()
            break







    
    score = 0
    delay = 0.1

def bye():
    turtle.bye()

#food eat then update score
def score_inc():
    global score
    score += 1

    # Update score in scores file
    update_score(name, score)

#if orange food eaten, subtract score
def shrink_food_eaten():
    global score
    if score > 0:  #for score not to go below 0
        score -= 1

    
    update_score(name, score)


def score_write():
    pen.clear()  
    
    pen.write(f'Score: {score}', align='center', font=('Arial', 24, 'normal'))

# Key Bindings
wn.listen()
wn.onkeypress(bye, 'q')
wn.onkeypress(start_game, 'p')
wn.onkeypress(go_up, 'w')
wn.onkeypress(go_down, 's')
wn.onkeypress(go_left, 'a')
wn.onkeypress(go_right, 'd')

# Main game loop
while True:
    wn.update()

    if game_state == 'intro':  # Check if menu pa
        wn.bgpic('C:\Python\Snake game 2\MAIN MENU (1).gif')
        pen.clear()
    elif game_state == 'ingame':  # Check if nagdula na
        wn.bgpic('C:\Python\Snake game 2\grass2.2.gif')
        head.showturtle()
        food.showturtle()
        shrink_food.showturtle()
        score_write()

    # Checks for Collision with FOOD
    if head.distance(food) < 20:

        score_inc()
        score_write()

        flag = 0
        x = 0
        y = 0
        while flag == 0:
            flag = 1
            # Random
            x = random.randint(-380, 380)
            y = random.randint(-380, 350)  # This is so within the window lang ang food mag spawn
            for segment in segments:
                if segment.distance(x, y) < 20:  # Check if the food kay close sa food
                    flag = 0
                    break
        food.goto(x, y)  # I spawn ang food randomly in the game

        # Body
        new_segment = turtle.Turtle()  # Creates a segment instance
        new_segment.speed(0)
        new_segment.shape('square')
        new_segment.color("#619bcc")
        new_segment.penup()
        segments.append(new_segment)  # Add ug new segment (body) to the snake

        delay -= 0.0015  # Increase speed every kaon

    #check if nakaon na ang orange food/shrink food
    if head.distance(shrink_food) < 20:

        shrink_food_eaten()
        score_write()

        if len(segments) > 0:
            segments[-1].goto(2000, 2000)  #shrink the snake by removing a segment
            segments.pop()  #remove from the list
        shrink_food.goto(random.randint(-380, 380), random.randint(-380, 350))  # Respawn shrink food

    # Head follow body so snake like
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    #check if head hits body
    for segment in segments:  
        if head.distance(segment) < 20:
            game_over()
            break

    #check if snake hit boundary/window
    if head.xcor() < -380:
        head.goto(380, head.ycor())
    if head.xcor() > 380:
        head.goto(-380, head.ycor())
    if head.ycor() < -380:
        head.goto(head.xcor(), 380)
    if head.ycor() > 380:
        head.goto(head.xcor(), -380)

    time.sleep(delay)  # Waits for delay amount of time before looping again

wn.mainloop()  
