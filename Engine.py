board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
         [5, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 7, 0, 0, 0, 0, 3, 1],
         [0, 0, 3, 0, 1, 0, 0, 8, 0],
         [9, 0, 0, 8, 6, 3, 0, 0, 5],
         [0, 5, 0, 0, 9, 0, 6, 0, 0],
         [1, 3, 0, 0, 0, 0, 2, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 7, 4],
         [0, 0, 5, 2, 0, 6, 3, 0, 0]]


def print_board(puzzle):
    for i in range(9):
        for j in range(9):
            print(puzzle[i][j], end=" ")
        print()


def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0:
                return r, c
    return None, None


def row_contains(puzzle, guess, row):
    for i in range(9):
        if puzzle[row][i] == guess:
            return True
    return False


def col_contains(puzzle, guess, col):
    for i in range(9):
        if puzzle[i][col] == guess:
            return True
    return False


def box_contains(puzzle, guess, row, col):
    # box_row, box_col is the index of the top left of the box
    # that row, col is in
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if puzzle[i][j] == guess:
                return True
    return False


def is_valid_guess(puzzle, guess, row, col):

    return not ((row_contains(puzzle, guess, row))
                or (col_contains(puzzle, guess, col))
                or (box_contains(puzzle, guess, row, col)))


def solve_board(puzzle):
    # finds next square to check
    row, col = find_next_empty(puzzle)

    # if either of the indices is None, the puzzle is solved
    if row is None:
        return True

    # puzzle is not solved so try guessing a number
    for guess in range(1, 10):
        # check if guess is valid before putting it in list
        if is_valid_guess(puzzle, guess, row, col):
            puzzle[row][col] = guess

            # board is solved
            if solve_board(puzzle):
                return True

        # board isn't solved
        puzzle[row][col] = 0

    # backtrack
    return False
