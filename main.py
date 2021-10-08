import pygame
from pygame.locals import *
from solver import *

FPS = 90  # Frames per second
WIDTH = 690
HEIGHT = 570
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
pygame.display.set_caption("Gomuku")
surface = pygame.display.set_mode((HEIGHT,WIDTH))
clock = pygame.time.Clock()

#---------------------
# Setup Colors 
#---------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (231, 231, 231)
ORANGE = '#ff631c'
BLUE_LIGHT = (40, 53, 88)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
YELLOW_LIGHT = (255, 255, 51)
BROWN = (210, 105, 30)
PINK = (204, 0, 255)
GREEN_LIGHT = (0, 255, 140)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 255, 0)


menuFont = pygame.font.SysFont("CopperPlate Gothic", 60, bold = True)  
helpFont = pygame.font.SysFont("Comic Sans MS", 23)      
wordFont = pygame.font.SysFont("CopperPlate Gothic", 25)  
recordFont = pygame.font.SysFont("Comic Sans MS", 17)  
mapFont = pygame.font.SysFont("Comic Sans MS", 20, bold = True)   
levelFont = pygame.font.SysFont("Comic Sans MS", 25, bold = True)  
buttonFont = pygame.font.SysFont("CopperPlate Gothic", 18, bold = True)


player1 = pygame.image.load('Items/player1.png')
player1 = pygame.transform.scale(player1, (25,25))

player2 = pygame.image.load('Items/player2.png')
player2 = pygame.transform.scale(player2, (25,25))

up_arrow = pygame.image.load("Items/up_arrow.png")
up_arrow = pygame.transform.scale(up_arrow, (15, 15))

down_arrow = pygame.image.load("Items/down_arrow.png")
down_arrow = pygame.transform.scale(down_arrow, (15, 15))

pick_button = pygame.image.load("Items/choose.png")
pick_button = pygame.transform.scale(pick_button, (80, 32))

restart_button = pygame.image.load("Items/restart.png")
restart_button = pygame.transform.scale(restart_button, (84, 32))


up_arrow_rect = Rect(210, 612, 15, 15)
down_arrow_rect = Rect(210, 627, 15, 15)
pick_rect = Rect(75, 650, 80, 32)
restart_rect = Rect(390, 650, 84, 32)

win = 0 # draw a line diagon or vertical or horizontal
draw = 0 # draw match
step = 1
mode = 0
result = []
computerTurn = 0

def display_up_arrow():
	surface.blit(up_arrow, [210, 612])

def display_down_arrow():
	surface.blit(down_arrow, [210, 627])

def display_pick_button():
	surface.blit(pick_button, [75, 650])

def display_restart():
	surface.blit(restart_button, [390, 650])

def display_title_step_1(color = RED):
	step1Text = helpFont.render("1. Choose your mode", True, color)
	surface.blit(step1Text, [5, 575])

def display_title_content_1(color = GRAY_LIGHT):
	if mode == 0:
		modeText = mapFont.render("Player vs Player", True, color)
		surface.blit(modeText, [30, 610])
	elif mode == 1:
		modeText = mapFont.render("Player vs Computer", True, color)
		surface.blit(modeText, [15, 610])
	elif mode == 2:
		modeText = mapFont.render("Computer vs Player", True, color)
		surface.blit(modeText, [15, 610])

	
def display_title_step_2(color = RED):
	step2Text = helpFont.render("2. Good luck to you !!!", True, color)
	surface.blit(step2Text, [310, 575])

def turnToPlayer():
	if turn == 1:
		return 1
	else:
		return 2

def display_title_content_2(color = GRAY_LIGHT):
	if win + draw == 1:
		if win == 1:
			modeText = mapFont.render("Congratulations, Player {}".format(3-turnToPlayer()), True, color)
			surface.blit(modeText, [305, 610])
		if draw == 1:
			modeText = mapFont.render("Draw Match !!!", True, color)
			surface.blit(modeText, [360, 610])
	else:
		modeText = mapFont.render("Player {} Turn".format(turnToPlayer()), True, color)
		surface.blit(modeText, [360, 610])

def display_step_1():
	if step == 1:
		display_title_step_1(YELLOW)
		display_title_content_1()
		display_up_arrow()
		display_down_arrow()
		display_pick_button()
	if step == 2:
		display_title_step_1(GREEN_DARK)
		display_title_content_1(RED)


def display_step_2():
	if win + draw == 0:
		display_title_step_2(YELLOW)
		display_title_content_2()
		display_restart()
	else:
		display_title_step_2(GREEN_DARK)
		display_title_content_2(ORANGE)
		display_restart()

def draw_menu():
	pygame.draw.rect(surface, BLUE_LIGHT, [0, 570, 570, 680])
	if step == 1:
		display_step_1()
	if step == 2:
		display_step_1()
		display_step_2()

def draw_line(l):
	clock.tick(FPS)
	if l[-1] == -1:
		line_color = RED
	elif l[-1] == 1:
		line_color = BLUE

	(i1,j1) = l[0]
	(i2,j2) = l[1]
	if l[2] == 1:
		pygame.draw.line(surface, line_color, [3 + j1*30, 15 + i1*30], [27.1 + j2*30, 15 + i2*30], width = 5)
	elif l[2] == 2:
		pygame.draw.line(surface, line_color, [15 + j1*30, 3 + i1*30], [15 + j2*30, 27.1 + i2*30], width = 5)
	elif l[2] == 3:
		pygame.draw.line(surface, line_color, [5 + j1*30, 5 + i1*30], [25.1 + j2*30, 25.1 + i2*30], width = 5)
	elif l[2] == 4:
		pygame.draw.line(surface, line_color, [25.1 + j1*30, 5 + i1*30], [5 + j2*30, 25.1 + i2*30], width = 5)

	pygame.display.flip()

def draw_board():
	draw_menu()
	pygame.draw.rect(surface, GRAY_LIGHT, [0, 0, 570, 570])
	for i in range(19):
		for j in range(19):
			pygame.draw.rect(surface, BLACK, pygame.Rect(j*30, i*30, 30, 30), width = 2)
			if board[i][j] == 1: # Player 1
				surface.blit(player1, [2.5 + j*30, 2.5 + i*30])
			if board[i][j] == -1: # Player 2
				surface.blit(player2, [2.5 + j*30, 2.5 + i*30])
	if win == 1:
		draw_line(result)
	pygame.display.flip()

def mouse_click(x,y):
	global board, turn, win, draw, result
	if y > 570:
		return False
	if board[int(y/30)][int(x/30)] == 0:
		board[int(y/30)][int(x/30)] = turn
		turn *= -1
		l = check_win(board)
		if len(l) > 0:
			win = 1
			result = l
			return
		elif is_full(board) == True:
			draw = 1
		return True
	return False

def get_computer_move():
	global board, turn, win, draw, result
	(x,y) = minimaxSearch(board, turn, 1)
	if board[x][y] == 0:
		board[x][y] = turn
		turn *= -1

	l = check_win(board)
	if len(l) > 0:
		win = 1
		result = l
		return
	elif is_full(board) == True:
		draw = 1

def reset_data():
	global win, step, mode, result, board, turn, draw, computerTurn
	step = 1
	mode = 0
	result = []
	board = [[0 for j in range(19)] for i in range(19)]
	turn = 1
	win = 0 
	draw = 0 
	computerTurn = 0



def main():
	global board, mode, step, computerTurn
	while True:
		clock.tick(FPS)
		for event in pygame.event.get():
			keys_pressed = pygame.key.get_pressed()
			if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
				pygame.quit()

			if computerTurn == 1:
				if win + draw == 0:
					get_computer_move()
				computerTurn = 0

			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = event.pos
				if step == 1:
					if up_arrow_rect.collidepoint(x,y): 
						mode = (mode+1)%3
					if down_arrow_rect.collidepoint(x,y): 
						mode = (mode+2)%3
					if pick_rect.collidepoint(x,y):
						step = 2
						if mode == 2:
							computerTurn = 1
						continue
				if step == 2: # Check mode 0,1,2
					if restart_rect.collidepoint(x, y):
						reset_data()

					if mode == 0:
						if win + draw == 0:
							mouse_click(x,y)
					elif mode == 1:
						if win + draw == 0:
							if mouse_click(x,y):
								computerTurn = 1
					elif mode == 2:
						if win + draw == 0:
							if mouse_click(x,y):
								computerTurn = 1
		draw_board()
		pygame.display.update()
	pygame.quit()

if __name__ == '__main__':
	main()