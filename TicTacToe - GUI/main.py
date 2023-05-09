import pygame
import time

# Initialize Pygame
pygame.init()

# Set the window size
WINDOW_SIZE = (300, 300)

# Set the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tic Tac Toe")

# Set the font
font = pygame.font.Font(None, 80)

# Initialize the game variables
player = "X"
board = [["", "", ""], ["", "", ""], ["", "", ""]]
game_over = False

# Draw the Tic Tac Toe board
def draw_board():
    screen.fill(WHITE)
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, BLACK, (i*100, j*100, 100, 100), 2)
            text = font.render(board[j][i], True, BLACK)
            screen.blit(text, (i*100+30, j*100+15))

# Check if the game is over
def check_game_over():
    global game_over
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            game_over = True
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            game_over = True
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        game_over = True
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        game_over = True
        return board[0][2]
    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        game_over = True
        return "Tie"

# Main game loop
while not game_over:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            i, j = x//100, y//100
            if board[j][i] == "":
                board[j][i] = player
                player = "O" if player == "X" else "X"
                winner = check_game_over()
                if winner:
                    game_over = True

    # Draw the board
    draw_board()

    # Update the display
    pygame.display.update()

# Display the winner
if winner != "Tie":
    text = font.render(winner + " wins!", True, BLACK)
else:
    text = font.render("It's a tie!", True, BLACK)

screen.fill(WHITE)
screen.blit(text, (40, 120))
pygame.display.update()
time.sleep(3)

# Quit Pygame
pygame.quit()