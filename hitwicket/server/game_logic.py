class Game:
    def __init__(self):
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.players = {'A': [], 'B': []}
        self.turn = 'A'
        self.winner = None

    def initialize_game(self, player_a_positions, player_b_positions):
        self.board[0] = player_a_positions
        self.board[4] = player_b_positions
        self.players['A'] = [(0, i, player_a_positions[i]) for i in range(5)]
        self.players['B'] = [(4, i, player_b_positions[i]) for i in range(5)]
        self.turn = 'A'

    def is_valid_move(self, player, character_name, move):
        if self.winner:
            return False
        if self.turn != player:
            return False
        
        char_pos = next(((x, y, c) for x, y, c in self.players[player] if c == character_name), None)
        if not char_pos:
            return False
        
        row, col, _ = char_pos
        if character_name.endswith('P'):
            return self._validate_pawn_move(row, col, move)
        elif character_name.endswith('H1'):
            return self._validate_hero1_move(row, col, move)
        elif character_name.endswith('H2'):
            return self._validate_hero2_move(row, col, move)

        return False

    def _validate_pawn_move(self, row, col, move):
        new_row, new_col = row, col
        if move == 'L':
            new_col -= 1
        elif move == 'R':
            new_col += 1
        elif move == 'F':
            new_row += 1 if self.turn == 'A' else -1
        elif move == 'B':
            new_row -= 1 if self.turn == 'A' else +1
        return 0 <= new_row < 5 and 0 <= new_col < 5

    def _validate_hero1_move(self, row, col, move):
        new_row, new_col = row, col
        if move == 'L':
            new_col -= 2
        elif move == 'R':
            new_col += 2
        elif move == 'F':
            new_row += 2 if self.turn == 'A' else -2
        elif move == 'B':
            new_row -= 2 if self.turn == 'A' else +2
        return 0 <= new_row < 5 and 0 <= new_col < 5

    def _validate_hero2_move(self, row, col, move):
        new_row, new_col = row, col
        if move == 'FL':
            new_row += 2 if self.turn == 'A' else -2
            new_col -= 2
        elif move == 'FR':
            new_row += 2 if self.turn == 'A' else -2
            new_col += 2
        elif move == 'BL':
            new_row -= 2 if self.turn == 'A' else +2
            new_col -= 2
        elif move == 'BR':
            new_row -= 2 if self.turn == 'A' else +2
            new_col += 2
        return 0 <= new_row < 5 and 0 <= new_col < 5

    def move_character(self, player, character_name, move):
        char_pos = next(((x, y, c) for x, y, c in self.players[player] if c == character_name), None)
        if not char_pos:
            return

        row, col, _ = char_pos

        if character_name.endswith('P'):
            new_row, new_col = self._calculate_new_position(row, col, move, 1)
        elif character_name.endswith('H1'):
            new_row, new_col = self._calculate_new_position(row, col, move, 2)
        elif character_name.endswith('H2'):
            new_row, new_col = self._calculate_new_position(row, col, move, 2, True)
        
        self._remove_opponents_in_path(row, col, new_row, new_col, player)
        self.board[row][col] = ''
        self.board[new_row][new_col] = character_name

        self.players[player].remove((row, col, character_name))
        self.players[player].append((new_row, new_col, character_name))

    def _calculate_new_position(self, row, col, move, distance, diagonal=False):
        new_row, new_col = row, col
        if move == 'L':
            new_col -= distance
        elif move == 'R':
            new_col += distance
        elif move == 'F':
            new_row += distance if self.turn == 'A' else -distance
        elif move == 'B':
            new_row -= distance if self.turn == 'A' else +distance
        elif move == 'FL':
            new_row += distance if self.turn == 'A' else -distance
            new_col -= distance
        elif move == 'FR':
            new_row += distance if self.turn == 'A' else -distance
            new_col += distance
        elif move == 'BL':
            new_row -= distance if self.turn == 'A' else +distance
            new_col -= distance
        elif move == 'BR':
            new_row -= distance if self.turn == 'A' else +distance
            new_col += distance
        return new_row, new_col

    def _remove_opponents_in_path(self, row, col, new_row, new_col, player):
        opponent = 'B' if player == 'A' else 'A'
        for r in range(min(row, new_row), max(row, new_row) + 1):
            for c in range(min(col, new_col), max(col, new_col) + 1):
                if self.board[r][c].startswith(opponent):
                    self.board[r][c] = ''
                    self.players[opponent] = [(x, y, c) for x, y, c in self.players[opponent] if (x, y) != (r, c)]

    def check_winner(self):
        if not self.players['A']:
            self.winner = 'B'
        elif not self.players['B']:
            self.winner = 'A'

    def get_game_state(self):
        return {
            "board": self.board,
            "turn": self.turn,
            "winner": self.winner
        }