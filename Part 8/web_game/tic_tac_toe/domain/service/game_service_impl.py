from typing import List
from tic_tac_toe.domain.service.game_service import GameService
from tic_tac_toe.domain.model.game import CurrentGame


class GameServiceImpl(GameService):

    def next_move(self, game: CurrentGame) -> CurrentGame:
        board = game.get_board()

        best_score = -1000
        move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = self.minimax(board, False)
                    board[i][j] = 0

                    if score > best_score:
                        best_score = score
                        move = (i, j)

        if move:
            board[move[0]][move[1]] = 2

        game.set_board(board)

        return game

    def validate(self, old_game: CurrentGame | None, new_game: CurrentGame) -> bool:
        # 1. If no old game → assume empty board
        if old_game is None:
            old_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        else:
            old_board = old_game.get_board()

        new_board = new_game.get_board()

        # 1. Check board size (3x3)
        if len(new_board) != 3:
            return False
        for row in new_board:
            if len(row) != 3:
                return False

        # 2. Check allowed values (0, 1, 2)
        for i in range(3):
            for j in range(3):
                if new_board[i][j] not in (0, 1, 2):
                    return False

        # 3. Compare boards
        changes = 0

        for i in range(3):
            for j in range(3):

                old_cell = old_board[i][j]
                new_cell = new_board[i][j]

                if old_cell == new_cell:
                    continue

                if old_cell != 0:
                    return False

                if new_cell == 0:
                    return False

                # Valid new move
                changes += 1

        # 4. Must be exactly ONE move
        if changes != 1:
            return False

        return True

    def is_finished(self, game: CurrentGame) -> bool:
        return self.check_winner(game.get_board()) is not None

    def check_winner(self, board: List[List[int]]) -> int | None:

        for row in board:
            if row[0] == row[1] == row[2] != 0:
                return row[0]

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != 0:
                return board[0][col]

        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2]

        if self.is_draw(board):
            return 0

        return None

    @staticmethod
    def is_draw(board: List[List[int]]) -> bool:
        for row in board:
            if 0 in row:
                return False
        return True

    def minimax(self, board: List[List[int]], is_maximizing: bool):

        winner = self.check_winner(board)

        if winner == 2:
            return 1

        if winner == 1:
            return -1

        if self.is_draw(board):
            return 0

        if is_maximizing:
            best_score = -1000

            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 2
                        score = self.minimax(board, False)
                        board[i][j] = 0
                        best_score = max(score, best_score)

            return best_score

        else:
            best_score = 1000

            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, True)
                        board[i][j] = 0
                        best_score = min(score, best_score)

            return best_score