# Tic Tac Toe - Two Player (Friend Mode)
# Clean, simple, and fully playable in the console

# Initialize the board as a list of 9 spaces
board = [" " for _ in range(9)]


def print_board():
    """Print the current state of the board"""
    print()
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()


def check_winner(player):
    """Check if the given player has won"""
    win_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # rows
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # columns
        [0, 4, 8],
        [2, 4, 6],  # diagonals
    ]
    for combo in win_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False


def check_draw():
    """Check if the game is a draw"""
    return all(space != " " for space in board)


def get_player_move(player):
    """Prompt the current player to enter a valid move"""
    while True:
        move = input(f"Player {player}, enter a position (1-9): ")
        if move.isdigit() and 1 <= int(move) <= 9:
            move = int(move) - 1
            if board[move] == " ":
                board[move] = player
                break
            else:
                print("That spot is already taken. Try again.")
        else:
            print("Invalid input. Enter a number from 1 to 9.")


# Main game loop
current_player = "X"
game_over = False

print("Welcome to Tic Tac Toe!")
print_board()

while not game_over:
    get_player_move(current_player)
    print_board()

    if check_winner(current_player):
        print(f"Player {current_player} wins!")
        game_over = True
    elif check_draw():
        print("It's a draw!")
        game_over = True
    else:
        # Switch player
        current_player = "O" if current_player == "X" else "X"
