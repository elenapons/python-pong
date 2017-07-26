# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = [[0,0],[0,0]]
paddle2_pos = [[0,0],[0,0]]
paddle1_pos[0] = [HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]     
paddle1_pos[1] = [HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
paddle2_pos[0] = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]
paddle2_pos[1] = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
points_player1 = 0
points_player2 = 0

# initialize ball_pos and ball_vel for new ball in middle of table
ball_pos = [0, 0]
ball_vel = [0, 0]



# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [300,200]
    ball_vel[0] = random.randrange(120, 240)
    ball_vel[1] = - (random.randrange(60, 180))    
    if direction == LEFT:
        ball_vel[0] = - ball_vel[0]
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2, points_player1, points_player2  # these are ints
    points_player1 = 0
    points_player2 = 0
    spawn_ball(LEFT)
    
def button_handler_reset():
    new_game()
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, points_player1, points_player2

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball. Calculate ball position
    ball_pos[0] += ball_vel[0] / 60.0 # draw is called 60 times/second
    ball_pos[1] += ball_vel[1] / 60.0 # draw is called 60 times/second 
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[0] = ball_vel[0]
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[0] = ball_vel[0]
        ball_vel[1] = - ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if not paddle1_pos[1][1] + paddle1_vel[1] <= 0 and not paddle1_pos[0][1] + paddle1_vel[1]>= HEIGHT:   
        paddle1_pos[0][1] += paddle1_vel[1] # paddle1 and paddle2 are a list of lists, I need to acces the y of both lists
        paddle1_pos[1][1] += paddle1_vel[1]
        
    if not paddle2_pos[1][1] + paddle2_vel[1] <= 0 and not paddle2_pos[0][1] + paddle2_vel[1]>= HEIGHT: 
        paddle2_pos[0][1] += paddle2_vel[1]
        paddle2_pos[1][1] += paddle2_vel[1]
    
    # draw paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide
    # paddle_pos == [[x, y], [x', y']]
    if ball_pos[0] + BALL_RADIUS + PAD_WIDTH >= WIDTH and (ball_pos[1] >= paddle2_pos[1][1] and ball_pos[1] <= paddle2_pos[0][1]):
        ball_vel[0] = - ball_vel[0]
        ball_vel[1] = ball_vel[1]
        ball_vel[0] -= 70
    elif ball_pos [0] + BALL_RADIUS + PAD_WIDTH >= WIDTH:
        spawn_ball(LEFT)
        points_player1 += 1   
    if ball_pos[0] - BALL_RADIUS - PAD_WIDTH <= 0 and (ball_pos[1] >= paddle1_pos[1][1] and ball_pos[1] <= paddle1_pos[0][1]):
        ball_vel[0] = - ball_vel[0]
        ball_vel[1] = ball_vel[1]
        ball_vel[0] += 70
    elif ball_pos[0] - BALL_RADIUS - PAD_WIDTH <= 0:
        spawn_ball(RIGHT)
        points_player2 += 1
    # draw scores
    canvas.draw_text(str(points_player1), (140, 50), 32, "White")
    canvas.draw_text(str(points_player2), (440, 50), 32, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    # paddle1 and paddle2 are a list of lists, I need to acces the y of both lists
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = 5     
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = -5      
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = 5
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = -5
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', button_handler_reset, 150) # draw reset button
# start frame
new_game()
frame.start()
