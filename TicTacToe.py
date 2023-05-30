import pygame
import time
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

ENABLE_GRAPH = True

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

#Initialize graph
graph = nx.DiGraph()

# Draw the Tic Tac Toe board
def draw_board():
    screen.fill(WHITE)
    for i in range(3): 
        for j in range(3):
            pygame.draw.rect(screen, BLACK, (i*100, j*100, 100, 100), 2) 
            text = font.render(board[j][i], True, BLACK) 
            screen.blit(text, (i*100+30, j*100+15)) 
    #draw toggle button
    pygame.draw.rect(screen, GRAY, (0, 300, 300, 100), 0)
    text = font.render("Toggle", True, BLACK)
    screen.blit(text, (100, 320))

# Check if the game is over
def check_game_over():
    for i in range(3): 
        if board[i][0] == board[i][1] == board[i][2] != "": 
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "": 
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        return "Tie"

def ai_turn(): 
    best_score = -float('inf')
    best_move_i = -1
    best_move_j = -1
    alpha = -float('inf')
    beta = float('inf')
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                graph.add_node("Start")
                score = minimax(0, False, alpha, beta, 0, 0)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move_i = i
                    best_move_j = j
    
    board[best_move_i][best_move_j] = "O"
    #update graph if graph is enabled
    if ENABLE_GRAPH == True:
        plt.clf()
        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, node_size=1500, edge_color="black")
        nx.draw_networkx_labels(graph, pos, labels={node: node for node in graph.nodes()})
        plt.pause(0.1)
        graph.clear()

def minimax(depth, isMax, alpha, beta, prvi, prvj):
    result = check_game_over()
    if result == "Tie":
        return 0
    if result == "X":
        return -1
    if result == "O":
        return 1

    if isMax:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(depth + 1, False, alpha, beta, i, j)
                    #Adding nodes and edges to graph if enabled
                    if ENABLE_GRAPH == True:
                        if depth == 0:
                            graph.add_edge("Start", f"({i},{j})")
                        else:
                            graph.add_edge(f"{depth-1} ({prvi},{prvj})", f"{depth} ({i},{j})")
                    board[i][j] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(depth + 1, True, alpha, beta, i, j)
                    #Adding nodes and edges to graph if enabled
                    if ENABLE_GRAPH == True:
                        if depth == 0:
                            graph.add_edge("Start", f"{depth} ({i},{j})")
                        else:
                            graph.add_edge(f"{depth-1} ({prvi},{prvj})", f"{depth} ({i},{j})")
                    board[i][j] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score
         
# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse click events
            x, y = event.pos
            i, j = x // 100, y // 100

            # Check if the click is within the board boundaries
            if 0 <= i < 3 and 0 <= j < 3:
                # human turn
                if board[j][i] == "":
                    board[j][i] = "X"
                    
                    # check if game is over before ai plays
                    winner = check_game_over()
                    if winner:
                        running = False
                    else:
                        # ai turn
                        ai_turn()

                        # check if game is over before human plays
                        winner = check_game_over()
                        if winner:
                            running = False
          
    # Draw the board
    draw_board()

    # Update the display
    pygame.display.update()

time.sleep(1)
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