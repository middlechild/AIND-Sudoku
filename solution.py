assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Args:
        values(dict)
        box(string)
        value(string)

    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(a, b):
    """
    Cross product of elements in a and elements in b.
    Args:
        a(string) - row id
        b(string) - column id
    """
    return [s+t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print


def eliminate(values):
    """
    Eliminate values.
    Args:
        values(dict): The sudoku in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
            assign_value(values, peer, values[peer])  # NOTE: This line can be commented out
    return values


def only_choice(values):
    """
    Eliminate values using only-choice rule.
    Args:
        values(dict): The sudoku in dictionary form
    """
    for unit in unitlist:
        for digit in '123456789':
            found = [box for box in unit if digit in values[box]]
            if len(found) == 1:
                values[found[0]] = digit
                assign_value(values, found[0], digit)  # NOTE: This line can be commented out
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:

        # Find possible naked twins
        twins = [box for box in unit if len(values[box]) == 2]
        if len(twins) == 2 and values[twins[0]] == values[twins[1]]:

            # Intersect peers - Only shared peers should be modified
            peer_groups = [[peer for peer in peers[box]] for box in twins]
            group1 = set(peer_groups[0])
            group2 = set(peer_groups[1])
            common_peers = group1.intersection(group2)

            first_digit = '' + values[twins[0]][0]
            second_digit = '' + values[twins[0]][1]

            # Remove twin values from peers
            for peer in common_peers:
                if len(values[peer]) > 2:
                    values[peer] = values[peer].replace(first_digit, '').replace(second_digit, '')
                    assign_value(values, peer, values[peer])  # NOTE: This line can be commented out

    return values


def reduce_puzzle(values):
    """
    Args:
        values(dict): The sudoku in dictionary form
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Replace placeholders with a string of possible values
        values = eliminate(values)

        # Only Choice Rule: Every unit must contain exactly one occurrence of every number
        values = only_choice(values)

        # Naked Twins Rule: Find pairs and remove from shared peers
        values = naked_twins(values)

        # Check if stalled
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Args:
        values(dict): The sudoku in dictionary form
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[b]) == 1 for b in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value, return that answer
    for value in values[s]:
        new_sudoku_values = values.copy()
        new_sudoku_values[s] = value
        new_attempt = search(new_sudoku_values)
        if new_attempt:
            return new_attempt


def solve(grid, is_diagonal=True):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        is_diagonal(bool)
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # Only include diagonal units if the puzzle requires it
    if is_diagonal:
        global unitlist
        diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
        unitlist = diagonal_units + unitlist

    # Reduce: Apply different strategies to solve the puzzle before resorting to search
    values = reduce_puzzle(grid_values(grid))

    # Search: Pick a box with a minimal number of possible values and solve each of the puzzles obtained recursively
    values = search(values)

    # print(values)
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
