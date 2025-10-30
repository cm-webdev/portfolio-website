# new refactored version: tic_tac_toe_class.py


class TicTacToe:
    def __init__(self, board=None, current_player="X", status="In Play"):
        """Initialize or restore the game state."""
        self.board = board if board is not None else [" " for _ in range(9)]
        self.current_player = current_player
        self.status = status  # e.g., "In Play", "X Wins", "Draw"
        self.message = "Player X's turn."

    def get_display(self):
        """
        Formats the board into a string, using the logic from your old print_board(),
        but returns the string instead of printing it.
        """
        # Note: self.board is used instead of the global 'board'
        output = []
        output.append(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        output.append("---|---|---")
        output.append(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        output.append("---|---|---")
        output.append(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")

        # Join the lines into a single string with newlines
        return "\n".join(output)

    def get_board_state(self):
        """Returns the minimal data needed to save the game to session."""
        return {
            "board": self.board,
            "current_player": self.current_player,
            "status": self.status,
            "message": self.message,
        }

    def check_winner(self, player):
        """Check if the given player has won (Same logic as before)"""
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
        return any(
            all(self.board[i] == player for i in combo) for combo in win_combinations
        )

    def check_draw(self):
        """Check if the game is a draw"""
        return all(space != " " for space in self.board) and self.status == "In Play"

    def make_move(self, move_index):
        """Handles a move from a web form (0-8 index)"""
        # 1. Validation (Check if the game is over or spot is taken)
        if self.status != "In Play":
            self.message = f"Game Over. {self.status}"
            return

        if not (0 <= move_index < 9) or self.board[move_index] != " ":
            self.message = "That spot is invalid or taken. Try again."
            return

        # 2. Apply Move
        self.board[move_index] = self.current_player

        # 3. Check Game End
        if self.check_winner(self.current_player):
            self.status = f"Player {self.current_player} wins!"
            self.message = self.status
        elif self.check_draw():
            self.status = "Draw"
            self.message = "It's a draw!"
        else:
            # 4. Switch Player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.message = f"Player {self.current_player}'s turn."
