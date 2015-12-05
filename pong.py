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
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0]
paddle1_pos = 200
paddle2_pos = 200
paddle1_vel = 0
paddle2_vel = 0
player1_score = 0
player2_score = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists 

    if direction == True:
        ball_vel = [random.randrange(120, 240) / 60.0, (-(random.randrange(60,180) / 60.0))]
        ball_pos = [WIDTH / 2, HEIGHT / 2]
    elif direction == False:
        ball_vel = [(-(random.randrange(120, 240) / 60.0)), (-(random.randrange(60,180) / 60.0 ))]
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos  # these are numbers
    global player1_score, player2_score  # these are ints
    
    player1_score = 0
    player2_score = 0
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    paddle1_pos = 200
    paddle2_pos = 200
    paddle1_vel = 0
    paddle2_vel = 0
    
    rand_dir = (random.choice([True, False]))
    spawn_ball(rand_dir)

# helper function for paddle position update 
def paddle_update(pad_pos, pad_vel):  
    if pad_pos + pad_vel >= HALF_PAD_HEIGHT and pad_pos + pad_vel <= HEIGHT - HALF_PAD_HEIGHT:
        pad_pos += pad_vel
        
    return pad_pos       
        

def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, player1_score, player2_score
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]   
  
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 10, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen - uses paddle_update helper function 
    paddle1_pos = paddle_update(paddle1_pos, paddle1_vel)
    paddle2_pos = paddle_update(paddle2_pos, paddle2_vel)
                                
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([(WIDTH - HALF_PAD_WIDTH), paddle2_pos - HALF_PAD_HEIGHT], [(WIDTH - HALF_PAD_WIDTH), paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")

    # determine whether paddle and ball collide    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    if ball_pos[0] >= (WIDTH - PAD_WIDTH) - BALL_RADIUS:
        ball_vel[0] = - ball_vel[0]
        
        if ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] *= 1.1
        
        else: 
            player1_score += 1
            spawn_ball(False)
            
            
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        ball_vel[0] = - ball_vel[0]
        
        if ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] *= 1.1
            
        else: 
            player2_score += 1 
            spawn_ball(True)
        
    # draw scores
    canvas.draw_text(str(player1_score), [175, 50], 50, "White")
    canvas.draw_text(str(player2_score), [425, 50], 50, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5 
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5 
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5 
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel= 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0 
        
def button_handler():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button = frame.add_button("Reset", button_handler, 50)



# start frame
new_game()
frame.start()
