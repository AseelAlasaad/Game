import pygame
import sys


BOARD_SIZE = 8
SQUARE_SIZE = 64
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


images=[]
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
pygame.display.set_caption("Bubbles")
clock = pygame.time.Clock()

red_piece = pygame.image.load("red.png")
yellow_piece = pygame.image.load("yellow.png")

red_piece = pygame.transform.scale(red_piece, (SQUARE_SIZE, SQUARE_SIZE))
images.append(red_piece)
yellow_piece = pygame.transform.scale(yellow_piece, (SQUARE_SIZE, SQUARE_SIZE))
images.append(yellow_piece)

board = [
    [None, "Y", None, "Y", None, "Y", None, "Y"],
    ["Y", None, "Y", None, "Y", None, "Y", None],
    [None, "Y", None, "Y", None, "Y", None, "Y"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["R", None, "R", None, "R", None, "R", None],
    [None, "R", None, "R", None, "R", None, "R"],
    ["R", None, "R", None, "R", None, "R", None]
]

piece_image=[]
def draw_board():
   
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 0:
                color=BLACK
            else:
                color=WHITE
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))    
            piece = board[row][col]
            if piece:
                if  piece == "R":
                    piece_image=images[0]
                elif piece == "Y":
                    piece_image=images[1]    
            
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def draw_selection(row, col):
    pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                        10)
    

def draw_valid_moves(moves):
    for move in moves:
        row, col = move
        pygame.draw.rect(screen, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        




def move_piece(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = None

    if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
       removePiece(board,start_row,end_row,start_col,end_col)

def removePiece(board,sr,er,sc,ec):
    captured_row = (sr + er) // 2
    captured_col = (sc + ec) // 2
    board[captured_row][captured_col] = None
    

## Checks to see if the piece on the board
		
def on_board(row, col):
    if (row>=0 and col>=0 and row< 8 and col< 8):
        return True
    else:
        return False


def get_valid_moves(piece, row, col):
    valid_moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for drow, dcol in directions:
        new_row, new_col = row + drow, col + dcol
        if on_board(new_row, new_col):
         if  board[new_row][new_col]== None:
            valid_moves.append((new_row, new_col))
         elif  board[new_row][new_col] not in (piece, piece):
            new_row += drow
            new_col += dcol
            if on_board(new_row, new_col) and board[new_row][new_col] == None:
                valid_moves.append((new_row, new_col))

    return valid_moves

def alpha_beta_minimax(board, depth, alpha, beta, maximizing_player, cpu_color):
    
    def get_next_player_color(current_color):
        return "R" if current_color == "Y" else "Y"
    if depth == 0:
        return evaluate_board(board, cpu_color)

    eval_fn = max if maximizing_player else min
    best_eval = float('-inf') if maximizing_player else float('inf')

    player_color = cpu_color if maximizing_player else get_next_player_color(cpu_color)

    for move in get_all_moves(board, player_color):
        new_board = simulate_move(board, move)
        eval = alpha_beta_minimax(new_board, depth - 1, alpha, beta, not maximizing_player, cpu_color)
        best_eval = eval_fn(best_eval, eval)

        if maximizing_player:
            alpha = max(alpha, eval)
        else:
            beta = min(beta, eval)

        if beta <= alpha:
            break

    return best_eval


def get_all_moves(board, color):
    all_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == color:
                moves = get_valid_moves(color, row, col)
                for move in moves:
                    all_moves.append(((row, col), move))
    return all_moves


 #calculates the total number of pieces on the board to stop the game

def evaluate_board(board, color):
    # Count the number of pieces for the AI player
    AI_pieces=0
    for row in board:
        AI_pieces+=row.count(color)
        
   # Determine the color of the opponent
    
    if color == "Y":
        color = "R"
    else:
       color = "Y"

    Humman_pieces=0
    for row in board:
        Humman_pieces+=row.count(color)
    print(AI_pieces - Humman_pieces)    
    return AI_pieces - Humman_pieces



def simulate_move(board, move):
    
    start, end = move
    new_board = []
    for row in board:
     new_row = []
     for element in row:
        new_row.append(element)
     new_board.append(new_row)
        
    move_piece(new_board, start, end)
    return new_board


def cpu_move_alpha_beta(cpu_color):
    all_moves = get_all_moves(board, cpu_color)
    best_move = None
    best_eval = float('-inf')

    for move in all_moves:
        new_board = simulate_move(board, move)
        eval = alpha_beta_minimax(new_board, 3, float('-inf'), float('inf'), False, cpu_color)
        if eval > best_eval:
            best_eval = eval
            best_move = move

    move_piece(board, best_move[0], best_move[1])



def check_for_endgame(player_color):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
	 
            if board[row][col] == player_color:
                moves = get_valid_moves(player_color, row, col)
                if moves:
                    return False  # Player has valid moves
    return 'win'             
def game_results(result, winning_color=None,user_color=None):
    if user_color == 'R':
         winning_color='Y'
    else:
        winning_color='R'
    # print(winning_color)
    font = pygame.font.Font(None, 48)
    if result == "win":
        if winning_color == 'R':
            text = font.render("RED Win!", True, BLUE)
           
        else:
            text = font.render("YALLOW Win!", True, RED)
            print(text)

    else:
        return

    text_rect = text.get_rect(center=(BOARD_SIZE * SQUARE_SIZE // 2, BOARD_SIZE * SQUARE_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    pygame.time.delay(3000)                
				                            
def main_menu():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    
                    running = False
                    
                elif event.key == pygame.K_h:
                   
                   if event.key == pygame.K_ESCAPE:
                       # Return to the main menu when pressing ESCAPE
                       selected_color_screen_active = False
                   else:    
                    show_help_screen()
                elif event.key == pygame.K_q:
                  
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text1 = font.render("Bubbles Game", True, RED)
        text = font.render("Choose an option:", True, WHITE)
        text_play = font.render("Press 'P' to play", True, WHITE)
        text_help = font.render("Press 'H' for help", True, WHITE)
        text_quit = font.render("Press 'Q' to quit", True, WHITE)
        text_rect1 = text1.get_rect(center=(BOARD_SIZE * SQUARE_SIZE // 2, BOARD_SIZE * SQUARE_SIZE // 4))
        text_rect = text.get_rect(center=(BOARD_SIZE * SQUARE_SIZE // 2, BOARD_SIZE * SQUARE_SIZE // 2))
        text_play_rect = text_play.get_rect(center=(BOARD_SIZE * SQUARE_SIZE // 2, BOARD_SIZE * SQUARE_SIZE * 3 // 5))
        text_help_rect = text_help.get_rect(center=(BOARD_SIZE * SQUARE_SIZE // 2, BOARD_SIZE * SQUARE_SIZE * 3.5 // 5))
        text_quit_rect = text_quit.get_rect(center=(BOARD_SIZE * SQUARE_SIZE // 2, BOARD_SIZE * SQUARE_SIZE * 4 // 5))

        screen.blit(text1, text_rect1)
        screen.blit(text, text_rect)
        screen.blit(text_play, text_play_rect)
        screen.blit(text_help, text_help_rect)
        screen.blit(text_quit, text_quit_rect)

        pygame.display.flip()
        
SCREEN_WIDTH = 515
SCREEN_HEIGHT = 515
def show_help_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    help_screen_active = True

    while help_screen_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
               
                    help_screen_active = False

        screen.fill(BLACK)
        font = pygame.font.Font(None, 24)

 

        text2 = font.render("Rules of Bubbles:", True, RED)
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(text2, text2_rect)

        rules = [
            "1. The game is played on an 8x8 board.",
            "2. Each player starts with 12 pieces",
            "3. The pieces can move in all directions ",
            "4. A piece can capture an opponent's piece",
            " by jumping over it diagonally.",
            "5. The player who captures all the",
            " opponent's pieces wins the game."      
        ]

        y = 150
        for rule in rules:
            text = font.render(rule, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(text, text_rect)
            y += 30

        pygame.display.flip()
        clock.tick(60)
        
def show_selected_color():
    selected_color=None
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    selected_color_screen_active = True

    while selected_color_screen_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to the main menu when pressing ESCAPE
                    selected_color_screen_active = False

        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)


        text2 = font.render("Choose a color: Red (R) or Yallow (Y)", True, WHITE)
        text_rect2 = text2.get_rect(center=(BOARD_SIZE * SQUARE_SIZE // 2, BOARD_SIZE * SQUARE_SIZE // 2))
        screen.blit(text2, text_rect2)
        
        selecting_color = True
        pygame.display.flip()
        while selecting_color:
          for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_r:
                   return "R"
               if event.key == pygame.K_y:
                   return "Y"
           clock.tick(60)

       
             



main_menu()
def endGame():
    pygame.quit()
    sys.exit()
      
def main():


    user_color = show_selected_color()
    if user_color == "R":
       ai_color = "Y"
    else:
        ai_color = "R"
        
    if user_color == "R":
        user_turn=True
    else:
        user_turn=False
    selected_piece = None
    selected_row, selected_col = -1, -1
    valid_moves = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if user_turn and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row=pos[1] // SQUARE_SIZE
                piece = board[row][col]
                if selected_piece and (row, col) in valid_moves:
                    move_piece(board, (selected_row, selected_col), (row, col))
                    selected_piece = None
                    valid_moves = []
                    user_turn = False

                    game_result = check_for_endgame(user_color)
                    if game_result:
                        game_results(game_result, user_color if game_result == "win" else ai_color, user_color)
                        print(game_result)
                        running = False
                elif piece == user_color:
                    selected_piece = piece
                    selected_row, selected_col = row, col
                    valid_moves = get_valid_moves(piece, row, col)
                else:
                    selected_piece = None
                    valid_moves = []

        draw_board()

        if selected_piece:
            draw_selection(selected_row, selected_col)
            draw_valid_moves(valid_moves)

        pygame.display.flip()
        clock.tick(60)

        if  user_turn==False:
            cpu_move_alpha_beta(ai_color)
            user_turn = True

            game_result = check_for_endgame(user_color)
            if game_result:
                game_results(game_result, user_color if game_result == "win" else ai_color, user_color)
                running = False

    endGame()


if __name__ == "__main__":
    main()
