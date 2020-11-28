import sys
import random as rand #추가
from pygame.locals import *
from paddle import Paddle
from puck import Puck
from goalitem import Goalitem#추가
from scoreScreen import scoreScreen
from startScreen import air_hockey_start, disp_text
from themeScreen import theme_screen
from scoreScreen import * 
from globals import *
from endScreen import game_end
from wall import *
from pspeeditem import *

# Globals, initialized in method `init()`
# Create game objects.
paddle1 = Paddle(const.PADDLE1X, const.PADDLE1Y,const.PADDLE_SIZEA)
paddle2 = Paddle(const.PADDLE2X, const.PADDLE2Y,const.PADDLE_SIZEB)
puck = Puck(width / 2, height / 2)
puck2 = Puck(width / 2, height / 4)  #새로 추가한 퍽
wall = Wall(width / 3, height / 3)
goalitem=Goalitem(width * rand.random(),height * rand.random())#추가
pspeeditem = Pspeeditem(width * rand.random(),height * rand.random())


def init():
    global paddleHit, goal_whistle, clock, screen, smallfont, roundfont,item_sound
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    
    gamelogo = pygame.image.load(os.path.join(auxDirectory, 'AHlogo.png'))
    pygame.display.set_icon(gamelogo)
    pygame.display.set_caption('Air Hockey')
    screen = pygame.display.set_mode((width, height))

    #item_sound=pygame.mixer.Sound(os.path.join(auxDirectory, 'item.wav'))
    item_sound=pygame.mixer.Sound(os.path.join(auxDirectory, 'item.wav'))
    paddleHit = pygame.mixer.Sound(os.path.join(auxDirectory, 'hit.wav'))
    goal_whistle = pygame.mixer.Sound(os.path.join(auxDirectory, 'goal.wav'))

    smallfont = pygame.font.SysFont("comicsans", 35)
    roundfont = pygame.font.SysFont("comicsans", 45)

    clock = pygame.time.Clock()


def score(score1, score2, player_1_name, player_2_name):
    text1 = smallfont.render("{0} : {1}".format(player_1_name, str(score1)), True, const.BLACK)
    text2 = smallfont.render("{0} : {1}".format(player_2_name, str(score2)), True, const.BLACK)

    screen.blit(text1, [40, 0])
    screen.blit(text2, [width - 150, 0])


def rounds(rounds_p1, rounds_p2, round_no):
    disp_text(screen, "Round "+str(round_no), (width/2, 20), roundfont, const.BLACK)
    disp_text(screen, str(rounds_p1) + " : " + str(rounds_p2), (width / 2, 50), roundfont, const.BLACK)


def end(option, speed):
    global rounds_p1, rounds_p2, round_no, score1, score2

    # reset game with everything else same
    if option == 1:#2라운드 땃을 때 reset버튼 누를때
        puck.end_reset(speed)
        puck2.end_reset2(speed)
        wall.end_reset(speed)
        paddle1.reset(22, height / 2)
        paddle2.reset(width - 20, height / 2)
        score1, score2 = 0, 0
        rounds_p1, rounds_p2 = 0, 0
        round_no = 1
        return False  # Tells that game should continue with reset

    # goes to menu
    elif option == 2: #menu버튼
        return True  # Game should restart at startScreen

    # Quit game #quit버튼
    else:
        sys.exit()


def notify_round_change():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    return
        round_text = roundfont.render("ROUND {0} COMPLETE".format(round_no), True, colors[2][0])
        screen.blit(round_text, [width / 2 - 150, height / 2 - 50])

        score_text = roundfont.render("{0}  :  {1}".format(score1, score2), True, const.BLACK)
        screen.blit(score_text, [width / 2 - 37, height / 2])

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # continue
        x, y = width / 2 - 65, height / 2 + 100
        if (mouse[0] > x) and (mouse[0] < x + 150) and (mouse[1] > y) and (mouse[1] < y + 40):
            pygame.draw.rect(screen, colors[4][1], (x, y, 150, 40))
            if click[0] == 1:
                return
        else:
            pygame.draw.rect(screen, colors[4][0], (x, y, 150, 40))
        cont_text = smallfont.render("CONTINUE", True, const.WHITE)
        screen.blit(cont_text, [x + 10, y + 10])

        text = smallfont.render("OR", True, const.BLACK)
        screen.blit(text, [width / 2 - 18, height - 150])
        text = smallfont.render("press space to continue", True, const.BLACK)
        screen.blit(text, [width / 2 - 120, height - 110])

        pygame.display.flip()
        clock.tick(10)


# function to display pause screen


def show_pause_screen():
    global mute, music_paused
    """
        Shows the pause screen,
        This function will return,
        2 if the game is to be restarted,
        1 if the game is to be continued
        and exit here itself if exit is pressed
    """

    while True:
        text_pause = smallfont.render("PAUSED", True, const.BLACK)
        screen.blit(text_pause, [width / 2 - 44, 200])
        screen.blit(play_image, [width / 2 - 32, height - 70])

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # RESET
        if (mouse[0] > width / 4) and (mouse[0] < width / 4 + 150) and (mouse[1] > height - 200) and \
                (mouse[1] < height - 160):
            pygame.draw.rect(screen, colors[4][0], (width / 4, height - 200, 150, 40))
            if click[0] == 1:
                return 2
        else:
            pygame.draw.rect(screen, colors[4][1], (width / 4, height - 200, 150, 40))
        text_restart = smallfont.render("RESET", True, const.WHITE)
        screen.blit(text_restart, [width / 4 + 30, height - 195])

        # CONTINUE
        if (mouse[0] > width / 2 - 70) and (mouse[0] < width / 2 + 80) and (mouse[1] > height - 200) and \
                (mouse[1] < height - 160):
            pygame.draw.rect(screen, colors[0][0], (width / 2 - 70, height - 200, 150, 40))
            if click[0] == 1:
                return 1
        else:
            pygame.draw.rect(screen, colors[0][1], (width / 2 - 70, height - 200, 150, 40))
        text_cont = smallfont.render("CONTINUE", True, const.WHITE)
        screen.blit(text_cont, [width / 2 - 60, height - 195])

        # EXIT
        if (mouse[0] > width / 2 + 150) and (mouse[0] < width / 2 + 300) and (mouse[1] > height - 200) and \
                (mouse[1] < height - 160):
            pygame.draw.rect(screen, colors[1][0], (width / 2 + 150, height - 200, 150, 40))
            if click[0] == 1:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, colors[1][1], (width / 2 + 150, height - 200, 150, 40))
        text_exit = smallfont.render("EXIT", True, const.WHITE)
        screen.blit(text_exit, [width / 2 + 190, height - 195])

        # Look for mouse press events.
        events = pygame.event.get()
        for event in events:
            # removing pause using space
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return 1

            # continue by pressing play button as well
            if event.type == pygame.MOUSEBUTTONUP:
                if hits_pause_area(mouse):
                    return 1

            if event.type == QUIT:
                sys.exit()

        # checking if mute button clicked

        if abs(mouse[0] - (width - 100 + 32)) < const.MUTE_BUTTON_RADIUS and \
                abs(mouse[1] - (height / 2 - 250)) < const.MUTE_BUTTON_RADIUS and click[0] == 1:
            mute = not mute

        # mute and unmute audio code
        if mute and (not music_paused):
            pygame.mixer.music.pause()
            music_paused = True
        elif (not mute) and music_paused:
            pygame.mixer.music.unpause()
            music_paused = False

        # displaying mute and unmute button
        if mute:
            screen.blit(mute_image, (width - 100, height / 2 - 250 - 32))
        else:
            screen.blit(unmute_image, (width - 100, height / 2 - 250 - 32))

        pygame.display.flip()
        clock.tick(10)


# function to check is pause area is hit


def hits_pause_area(mouse_xy):
    """ Returns True if the mouse is clicked within the pause area"""

    return (abs(mouse_xy[0] - width / 2) < const.PAUSE_BUTTON_RADIUS) and \
           (abs(mouse_xy[1] - (height - 70 + 32)) < const.PAUSE_BUTTON_RADIUS)


def render_field(background_color):
    # Render Logic
    screen.fill(background_color)
    # center circle
    pygame.draw.circle(screen, const.WHITE, (int(width / 2), int(height / 2)), 70, 5)
    # borders
    pygame.draw.rect(screen, const.WHITE, (0, 0, width, height), 5)
    # D-box
    pygame.draw.rect(screen, const.WHITE, (0, height / 2 - 150, 150, 300), 5)
    pygame.draw.rect(screen, const.WHITE, (width - 150, height / 2 - 150, 150, 300), 5)
    # goals
    pygame.draw.rect(screen, const.BLACK, (0, const.GOAL_Y1, 5, const.GOAL_WIDTH))
    pygame.draw.rect(screen, const.BLACK, (width - 5, const.GOAL_Y1, 5, const.GOAL_WIDTH))
    # Divider
    pygame.draw.rect(screen, const.WHITE, (width / 2, 0, 3, height))

    # PAUSE 
    screen.blit(pause_image, (width / 2 - 32, height - 70))
    

def resetround(player):
    puck.round_reset(player)
    puck2.round_reset2(player)
    wall.round_reset(player)
    paddle1.reset(22, height / 2)
    paddle2.reset(width - 20, height / 2)


def reset_game(speed, player):
    const.PADDLE_SIZEA=40#추가
    const.PADDLE_SIZEB=40#추가
    const.PADDLE_SPEEDA=400
    const.PADDLE_SPEEDB=400
    paddle1.radius=const.PADDLE_SIZEA#추가
    paddle2.radius=const.PADDLE_SIZEB#추가
    paddle1.speed=const.PADDLE_SPEED
    paddle2.speed=const.PADDLE_SPEED
    puck.reset(speed, player)
    puck2.reset2(speed, player)
    wall.reset(speed,player)
    paddle1.reset(22, height / 2)
    paddle2.reset(width - 20, height / 2)
    goalitem.reset(width * rand.random(),height * rand.random())#추가
    pspeeditem.reset(width * rand.random(),height * rand.random())#추가
    

def inside_goal(side):
    """ Returns true if puck is within goal boundary"""
    if side == 0:
        return (puck.x - puck.radius <= 0) and (puck.y >= const.GOAL_Y1) and (puck.y <= const.GOAL_Y2)

    if side == 1:
        return (puck.x + puck.radius >= width) and (puck.y >= const.GOAL_Y1) and (puck.y <= const.GOAL_Y2)

def inside_goal2(side):
    """ Returns true if puck is within goal boundary"""
    if side == 0:
        return (puck2.x - puck2.radius <= 0) and (puck2.y >= const.GOAL_Y1) and (puck2.y <= const.GOAL_Y2)

    if side == 1:
        return (puck2.x + puck2.radius >= width) and (puck2.y >= const.GOAL_Y1) and (puck2.y <= const.GOAL_Y2)
def redraw_A():
    paddle1.radius=const.PADDLE_SIZEA#변경
def redraw_B():
    paddle2.radius=const.PADDLE_SIZEB#변경 const.PADDLE_SIZE를 A와 B로 나눔.

def respeedset_A():
    paddle1.speed=const.PADDLE_SPEEDA

def respeedset_B():
    paddle2.speed=const.PADDLE_SPEEDB

# Game Loop
def game_loop(speed, player1_color, player2_color, background_color, player_1_name, player_2_name):
    global rounds_p1, rounds_p2, round_no, music_paused
    rounds_p1, rounds_p2, round_no = 0, 0, 1

    pygame.mixer.music.load(os.path.join(auxDirectory, 'back.mp3'))  # background music
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.2)

    music_paused = False  # to check if music is playing or paused

    # mute if start screen was mute
    if mute and (not music_paused):
        pygame.mixer.music.pause()
        music_paused = True

    while True:
        global score1, score2

        for event in pygame.event.get():

            # check for space bar
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                ch = show_pause_screen()

                # if the return value is 2 reset everything
                if ch == 2:
                    score1 = 0
                    score2 = 0
                    rounds_p1 = 0
                    rounds_p2 = 0
                    round_no = 1
                    reset_game(speed, 1)
                    reset_game(speed, 2)
                    puck.angle = 0
                    puck2.angle = 0
                    wall.angle = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # check mouse click events
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_xy = pygame.mouse.get_pos()

                # check if the mouse is clicked within the pause area.
                if hits_pause_area(mouse_xy):
                    ch = show_pause_screen()

                    # if the return value is 2 reset everything

                    if ch == 2:
                        score1 = 0
                        score2 = 0
                        rounds_p1 = 0
                        rounds_p2 = 0
                        round_no = 1
                        reset_game(speed, 1)
                        reset_game(speed, 2)
                        puck.angle = -0.3
                        puck2.angle = 0.3
                        wall.angle = 0

        key_presses = pygame.key.get_pressed()

        # Process Player 1 Input
        w = key_presses[pygame.K_w]
        s = key_presses[pygame.K_s]
        d = key_presses[pygame.K_d]
        a = key_presses[pygame.K_a]

        # Process Player 2 Input
        up = key_presses[pygame.K_UP]
        down = key_presses[pygame.K_DOWN]
        right = key_presses[pygame.K_RIGHT]
        left = key_presses[pygame.K_LEFT]

        # time period between two consecutive frames.
        time_delta = clock.get_time() / 1000.0

        
        #아이템 범위 추가
        goalitem.check_vertical_bounds(height)
        goalitem.check_boundary(width)
        if goalitem.effect_A(paddle1) :
           redraw_A()
           goalitem.x=width *rand.random()
           goalitem.y=height *rand.random()
           screen.blit(goalitem.image,(int(goalitem.x),int(goalitem.y)))
           pygame.display.update()
           if not music_paused:
               pygame.mixer.Sound.play(item_sound)

        if goalitem.effect_B(paddle2):
            redraw_B()
            goalitem.x=width *rand.random()
            goalitem.y=height *rand.random()
            screen.blit(goalitem.image,(int(goalitem.x),int(goalitem.y)))
            pygame.display.update()
            if not music_paused:
                pygame.mixer.Sound.play(item_sound)
           
        pspeeditem.check_vertical_bounds(height)
        pspeeditem.check_boundary(width)
        if pspeeditem.effect_A(paddle1) :
           respeedset_A()
           pspeeditem.x=width *rand.random()
           pspeeditem.y=height *rand.random()
           screen.blit(pspeeditem.image,(int(pspeeditem.x),int(pspeeditem.y)))
           pygame.display.update()
           if not music_paused:
               pygame.mixer.Sound.play(item_sound)
        
        if pspeeditem.effect_B(paddle2) :
           respeedset_B()
           pspeeditem.x=width *rand.random()
           pspeeditem.y=height *rand.random()
           screen.blit(pspeeditem.image,(int(pspeeditem.x),int(pspeeditem.y)))
           pygame.display.update()
           if not music_paused:
               pygame.mixer.Sound.play(item_sound)

           #del goalitem



        
        # Update Paddle1
        paddle1.move(w, s, a, d, time_delta)
        paddle1.check_vertical_bounds(height)
        paddle1.check_left_boundary(width)

        if paddle1.collision_with_paddle(paddle2) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)

        # Update Paddle2
        paddle2.move(up, down, left, right, time_delta)
        paddle2.check_vertical_bounds(height)
        paddle2.check_right_boundary(width)

        if paddle2.collision_with_paddle(paddle1) and not music_paused:#패들 충돌 및 소리까지
             pygame.mixer.Sound.play(paddleHit)

        puck.move(time_delta)
        puck2.move(time_delta)
        wall.move(time_delta)

        # Hits the left goal!
        if inside_goal(0):
            if not music_paused:
                pygame.mixer.Sound.play(goal_whistle)  # Added sound for goal
            score2 += 1
            reset_game(speed, 1)
        
        if inside_goal2(0):
            if not music_paused:
                pygame.mixer.Sound.play(goal_whistle)  # Added sound for goal
            score2 += 1
            reset_game(speed, 1)

        # Hits the right goal!
        if inside_goal(1):
            if not music_paused:
                pygame.mixer.Sound.play(goal_whistle)  # Added sound for goal
            score1 += 1
            reset_game(speed, 2)

        if inside_goal2(1):
            if not music_paused:
                pygame.mixer.Sound.play(goal_whistle)  # Added sound for goal
            score1 += 1
            reset_game(speed, 2)

        # check puck collisions and update if necessary.
        puck.check_boundary(width, height)
        puck2.check_boundary(width, height)
        wall.check_boundary(width, height)

        if puck.collision_paddle(paddle1) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)  # Added sound for paddle hit

        if puck2.collision_paddle(paddle1) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)

        if puck.collision_paddle(paddle2) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)

         
        if puck2.collision_paddle(paddle2) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)
        
        if wall.collision_paddle(puck) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)
        
        if wall.collision_paddle(puck2) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)

        
        wall.collision_with_paddle(paddle1)
        wall.collision_with_paddle(paddle2)
            

        # Update round points 
        if score1 == const.SCORE_LIMIT:
            if not rounds_p1 + 1 == const.ROUND_LIMIT:
                notify_round_change()
            round_no += 1
            rounds_p1 += 1
            score1, score2 = 0, 0
            resetround(1)

        if score2 == const.SCORE_LIMIT:
            if not rounds_p2 + 1 == const.ROUND_LIMIT:
                notify_round_change()
            round_no += 1
            rounds_p2 += 1
            score1, score2 = 0, 0
            resetround(2)

        # playing area should be drawn first score
        render_field(background_color)

        # show score
        score(score1, score2, player_1_name, player_2_name)

        # display endscreen or rounds
        if rounds_p1 == const.ROUND_LIMIT:  # Player one denotes left player
            if end(game_end(screen, clock, background_color, player_1_name), speed):
                if music_paused:
                    pygame.mixer.music.unpause()
                pygame.mixer.stop()
                return
        elif rounds_p2 == const.ROUND_LIMIT:  # Player two denotes right player
            if end(game_end(screen, clock, background_color, player_2_name), speed):
                if music_paused:
                    pygame.mixer.music.unpause()
                pygame.mixer.stop()
                return

        else:
            rounds(rounds_p1, rounds_p2, round_no)

        # drawing the paddle and the puck reset
        wall.draw(screen)
        screen.blit(goalitem.image,(int(goalitem.x),int(goalitem.y)))
        screen.blit(pspeeditem.image,(int(pspeeditem.x),int(pspeeditem.y)))
        paddle1.draw(screen, player1_color)
        paddle2.draw(screen, player2_color)
        puck.draw(screen)
        puck2.draw(screen)
        

        # refresh screen.
        pygame.display.flip()
        clock.tick(const.FPS)


if __name__ == "__main__":
    global mute
    mute = False  # to keep state of mute
    init()
    while True:
        gameChoice, player1_color, player2_color, mute, player_1_name, player_2_name = air_hockey_start(
            screen, clock, width, height, mute)
        background_color = theme_screen(screen, clock, width, height, mute)
        init()
        """
        주의: 다음 라인애서 const값을 변경합니다.
        """
        const.SCORE_LIMIT,const.ROUND_LIMIT = scoreScreen(screen, clock, width, height, mute)#게임 스코어방식
        init()
        if gameChoice == 1:
            puck.speed = const.EASY
            puck2.speed = const.EASY
            wall.speed = const.EASY*0
            game_loop(const.EASY, player1_color, player2_color, background_color, player_1_name, player_2_name)
        elif gameChoice == 2:
            puck.speed = const.HARD
            puck2.speed = const.HARD
            wall.speed = const.HARD*0
            game_loop(const.HARD, player1_color, player2_color, background_color, player_1_name, player_2_name)
        elif gameChoice == 0:
            sys.exit()