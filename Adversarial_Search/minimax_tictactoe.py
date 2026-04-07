"""
=============================================================================
  MINIMAX TIC-TAC-TOE  —  Fully Commented for Deep Understanding
=============================================================================

THE BIG IDEA (read this first!)
---------------------------------
Minimax is just answering ONE question recursively:
  "If both players play perfectly from THIS board position, what is the result?"

We assign scores to outcomes:
  +10  →  X (the AI / Maximizer) wins
  -10  →  O (the human / Minimizer) wins
   0   →  Draw

WHY +10 and -10?
  Because X wants to MAXIMIZE the score (get as high as possible).
  And O wants to MINIMIZE the score (get as low as possible).
  This "tug of war" is the core of Minimax.

THE RECURSION MENTAL MODEL:
  Think of a tree. Each node is a board state.
  Each branch is a possible move.
  The leaves (bottom nodes) are finished games with known scores.
  Minimax "bubbles up" scores from leaves to the root.
  - Maximizer nodes pick the HIGHEST child score
  - Minimizer nodes pick the LOWEST child score
=============================================================================
"""


# =============================================================================
# BOARD REPRESENTATION
# =============================================================================

def create_board():
    """
    The board is a simple list of 9 cells, indexed 0-8:
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8

    Empty cell = ' '  |  X = 'X'  |  O = 'O'
    """
    return [' '] * 9   # Creates ['', '', '', '', '', '', '', '', '']


def print_board(board):
    """Prints the board in a nice grid format."""
    print()
    for row in range(3):
        # Each row has 3 cells: indices (row*3), (row*3 + 1), (row*3 + 2)
        cells = board[row*3 : row*3 + 3]
        print(f" {cells[0]} | {cells[1]} | {cells[2]} ")
        if row < 2:
            print("---+---+---")
    print()


# =============================================================================
# WIN / DRAW DETECTION
# =============================================================================

# All 8 possible winning combinations (rows, columns, diagonals)
WINNING_COMBOS = [
    [0, 1, 2],  # top row
    [3, 4, 5],  # middle row
    [6, 7, 8],  # bottom row
    [0, 3, 6],  # left column
    [1, 4, 7],  # middle column
    [2, 5, 8],  # right column
    [0, 4, 8],  # diagonal top-left to bottom-right
    [2, 4, 6],  # diagonal top-right to bottom-left
]


def check_winner(board, player):
    """
    Returns True if 'player' has won on this board.
    We just check if any winning combo is fully occupied by 'player'.
    """
    for combo in WINNING_COMBOS:
        # combo is something like [0, 1, 2]
        # We check: does player occupy ALL three cells in this combo?
        if all(board[cell] == player for cell in combo):
            return True
    return False


def is_board_full(board):
    """Returns True if no empty cell remains (draw situation)."""
    return ' ' not in board


def get_available_moves(board):
    """Returns a list of indices where the board is still empty."""
    return [i for i, cell in enumerate(board) if cell == ' ']


# =============================================================================
# THE MINIMAX FUNCTION  ← THIS IS THE HEART OF EVERYTHING
# =============================================================================

def minimax(board, depth, is_maximizing):
    """
    The Minimax algorithm. This function answers:
      "What is the BEST possible score achievable from this board position,
       assuming both players play perfectly?"

    Parameters:
    -----------
    board          : current state of the game (list of 9 cells)
    depth          : how many moves deep we are in the recursion tree.
                     Used to prefer faster wins over slower ones.
    is_maximizing  : True  → it's X's turn (X wants the HIGHEST score)
                     False → it's O's turn (O wants the LOWEST score)

    Returns:
    --------
    An integer score:
        +10 - depth  → X wins    (higher depth = slower win = less preferred)
        -10 + depth  → O wins    (higher depth = slower loss = less preferred)
         0           → Draw

    HOW THE RECURSION WORKS (step by step):
    ----------------------------------------
    1. CHECK BASE CASES (has the game ended?):
       - If X already won → return a positive score
       - If O already won → return a negative score
       - If it's a draw   → return 0

    2. IF GAME HASN'T ENDED:
       - Try EVERY available move on a copy of the board
       - For each move, RECURSIVELY call minimax with the next player's turn
       - Collect all the scores that come back

    3. BUBBLE UP:
       - If it's X's turn (maximizing): return the HIGHEST score found
       - If it's O's turn (minimizing): return the LOWEST score found

    THINK OF IT THIS WAY:
    The function doesn't know the future — it SIMULATES the future
    by trying every possible move until the game ends, then works backwards.
    """

    # ----- BASE CASES (Termination conditions) -----
    # These stop the recursion. Without base cases, recursion = infinite loop!

    if check_winner(board, 'X'):
        # X won! Return a positive score.
        # We subtract 'depth' so the AI prefers WINNING SOONER
        # (a win at depth 1 scores +9, at depth 3 scores +7, etc.)
        return 10 - depth

    if check_winner(board, 'O'):
        # O won! Return a negative score.
        # We add 'depth' so the AI prefers LOSING LATER (delays defeat)
        return -10 + depth

    if is_board_full(board):
        # No winner and board is full → draw
        return 0

    # ----- RECURSIVE CASES -----
    # Game isn't over. Try every move and recurse.

    available = get_available_moves(board)

    if is_maximizing:
        # -------------------------------------------------------
        # X's turn: X is the MAXIMIZER
        # X wants to find the move that leads to the HIGHEST score
        # -------------------------------------------------------

        best_score = -1000   # Start with a very low score (will be replaced)

        for move in available:
            # STEP 1: Make the move (place X on this cell)
            board[move] = 'X'

            # STEP 2: Recursively ask: "What's the best O can do now?"
            #         is_maximizing flips to False because it's now O's turn
            score = minimax(board, depth + 1, False)
            #
            # ↑ THIS IS THE KEY RECURSIVE CALL ↑
            # We go one level deeper in the tree.
            # The function will eventually hit a base case and return a score.
            # That score bubbles back up here.

            # STEP 3: Undo the move (backtrack!)
            # This is crucial — we're exploring hypothetically.
            # We MUST restore the board so we can try the next move.
            board[move] = ' '

            # STEP 4: Keep track of the best (highest) score seen
            best_score = max(best_score, score)

        return best_score   # Return the best score X can achieve

    else:
        # -------------------------------------------------------
        # O's turn: O is the MINIMIZER
        # O wants to find the move that leads to the LOWEST score
        # -------------------------------------------------------

        best_score = 1000   # Start with a very high score (will be replaced)

        for move in available:
            # STEP 1: Make the move (place O on this cell)
            board[move] = 'O'

            # STEP 2: Recursively ask: "What's the best X can do now?"
            #         is_maximizing flips to True because it's now X's turn
            score = minimax(board, depth + 1, True)

            # STEP 3: Undo the move (backtrack!)
            board[move] = ' '

            # STEP 4: Keep track of the best (lowest) score seen
            best_score = min(best_score, score)

        return best_score   # Return the best score O can achieve


# =============================================================================
# AI MOVE SELECTOR
# =============================================================================

def get_best_move(board, ai_player):
    """
    Finds the best move for the AI by calling minimax for every available
    move, then picking the one with the best score.

    This is the "top level" call — it's NOT recursive itself.
    It just runs minimax once per available move and compares results.

    Parameters:
    -----------
    board      : current board state
    ai_player  : 'X' or 'O' — which player the AI is controlling

    Returns:
    --------
    The index (0-8) of the best move.
    """

    best_score = -1000       # We'll look for the maximum score
    best_move  = None        # The move that achieves that score

    for move in get_available_moves(board):
        # Hypothetically place the AI's piece
        board[move] = ai_player

        # Ask minimax: "What score does this lead to?"
        # depth=0 because we're at the root of the search
        # is_maximizing depends on who we are:
        #   - If AI is 'X', then after X moves, it's O's turn → False
        #   - If AI is 'O', then after O moves, it's X's turn → True
        if ai_player == 'X':
            score = minimax(board, 0, False)   # X just moved, now O's turn
        else:
            score = minimax(board, 0, True)    # O just moved, now X's turn

        # Undo the hypothetical move
        board[move] = ' '

        # Track the best score and corresponding move
        if ai_player == 'X':
            # X is maximizer: keep the highest score
            if score > best_score:
                best_score = score
                best_move  = move
        else:
            # O is minimizer: keep the lowest score
            if score < -best_score:   # flip comparison for minimizer
                best_score = score
                best_move  = move

    return best_move


# =============================================================================
# THE GAME LOOP
# =============================================================================

def play_game():
    """
    Main game loop. Human plays as 'O', AI plays as 'X'.
    X always goes first.
    """

    board     = create_board()
    ai        = 'X'       # AI is X (the Maximizer)
    human     = 'O'       # Human is O (the Minimizer)
    current   = 'X'       # X goes first

    print("=" * 45)
    print("   MINIMAX TIC-TAC-TOE  |  You = O, AI = X")
    print("=" * 45)
    print("\nBoard positions:")
    print(" 0 | 1 | 2 \n---+---+---\n 3 | 4 | 5 \n---+---+---\n 6 | 7 | 8 ")

    while True:

        print_board(board)

        # Check for win or draw BEFORE making a move
        if check_winner(board, 'X'):
            print(">>> X (AI) wins! The AI played perfectly.")
            break
        if check_winner(board, 'O'):
            print(">>> O (You) wins! Impressive!")
            break
        if is_board_full(board):
            print(">>> It's a draw! Both played perfectly.")
            break

        if current == ai:
            # AI's turn
            print("AI (X) is thinking...")
            move = get_best_move(board, ai)
            board[move] = ai
            print(f"AI plays at position {move}")

        else:
            # Human's turn
            while True:
                try:
                    move = int(input("Your turn (O) — enter position (0-8): "))
                    if move not in range(9):
                        print("Please enter a number between 0 and 8.")
                    elif board[move] != ' ':
                        print("That cell is already taken!")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")

            board[move] = human

        # Switch turns
        current = 'O' if current == 'X' else 'X'


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    play_game()


# =============================================================================
# MENTAL MODEL SUMMARY — HOW TO SOLVE ANY MINIMAX PROBLEM
# =============================================================================
#
# STEP 1: Define your PLAYERS and ROLES
#   - Who is the Maximizer? (wants highest score)
#   - Who is the Minimizer? (wants lowest score)
#
# STEP 2: Define your SCORES
#   - What score means "Maximizer wins"?   → positive number (e.g. +10)
#   - What score means "Minimizer wins"?   → negative number (e.g. -10)
#   - What score means "Draw"?             → 0
#
# STEP 3: Define your BASE CASES
#   - When does the game END? (win/loss/draw)
#   - Each base case returns the appropriate score.
#
# STEP 4: Write the RECURSIVE CASE
#   - Try EVERY possible move
#   - For each move:
#       a) Apply the move
#       b) Recurse with flipped player
#       c) Undo the move (backtrack)
#       d) Track best score (max if Maximizer, min if Minimizer)
#   - Return the best score found
#
# STEP 5: Pick the BEST MOVE at the root
#   - Run minimax for each available move from the starting position
#   - Choose the move with the best score
#
# This exact pattern works for Chess, Connect 4, Go (with limits), Checkers,
# and any two-player zero-sum game with perfect information!
# =============================================================================
