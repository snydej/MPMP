# Written by Joshua Snyder (joshsnyder@msn.com)
# 
# This is a solution to Matt Parker's Math(s) Puzzle #5
# https://www.youtube.com/watch?v=TEkJMFTyZwM
#
# For the most part this was a quick and drity solution but I've gone back and 
# added some comments to help people understand how this works with a few thrown
# in for those who may not be familiar with python. I also added some pretty
# printing code at the end.

# The width and height of the triagular grid
SIZE = 4

# The 6 directions that can be moved in, in the form (delta_x, delta_y)
directions = ((1, 0), (0, -1), (-1, -1), (-1, 0), (0, 1), (1, 1))

def move(point, direction):
    '''Returns a new point moved one step in the given direction'''
    
    # point is a tuple of 2 items. This does the same as:
    # x = point[0]
    # y = point[1]
    x, y = point
    dx, dy = direction
    return x + dx, y + dy

def in_bounds(point):
    x, y = point
    return x >= 0 and y < SIZE and x <= y

def new_grid(missing):
    '''Creates a new triangular grid with one coin missing'''
    
    # [True] * 3 gives [True, True, True] for example
    # each row of the grid has a different number of spaces
    # range(1, 5) gives [1, 2, 3, 4], which are the lengths of each row
    # Google "python list comprehension" for more info
    result = [[True] * i for i in range(1, SIZE + 1)]
    
    x, y = missing
    result[y][x] = False
    
    return result

def filled_points(grid):
    '''Returns a list of points in the grid that have coins there'''
    return [(x, y)
        for y, row in enumerate(grid)
        for x, filled in enumerate(row)
        if filled]

def find_solutions(grid, last_end, num_turns, jumps, accumulate):
    ''' 
    Recursively explores all possible move sequences.
    
    grid: A triangular array of booleans indicating where coins are
    last_end: Where the last jump ended. If the next jump begins there that jump
        doesn't cost an extra move
    num_turns: The number of turns made so far
    moves: a list of the jumps made so far in the form (start_point, end_point)
    accumulate: This is a function is called with every solution that is found
    '''
    filled = filled_points(grid)
    
    # If only one coin is left this is a solution.
    if len(filled) == 1:
        accumulate(num_turns, jumps)
        return
    
    # for each coin that's left
    for start in filled:
        st_x, st_y = start
        
        # for each direction the coin can be moved
        for d in directions:
            middle = move(start, d)
            mid_x, mid_y = middle
            
            end = move(middle, d)
            end_x, end_y = end
            
            # Check that the move is valid
            if not in_bounds(end) or not grid[mid_y][mid_x] \
                    or grid[end_y][end_x]:
                continue
            
            # Apply the move
            grid[st_y][st_x] = False
            grid[mid_y][mid_x] = False
            grid[end_y][end_x] = True
            jumps.append((start, end))
            
            new_turns = num_turns + (start != last_end)
            
            # Recursively explore all possibilities starting from this state
            find_solutions(grid, end, new_turns, jumps, accumulate)
            
            # grid and moves are updated, not copied, so must backtrack
            grid[st_y][st_x] = True
            grid[mid_y][mid_x] = True
            grid[end_y][end_x] = False
            jumps.pop()

def find_minimum():
    # This keeps track of the shortest solution seen
    def acc(num_turns, jumps):
        if num_turns < acc.min_turns:
            acc.min_turns = num_turns
            # Must make a copy here because the orignal moves array will get
            # modified. "[:]" is a special case of the slice syntax. It gives
            # you a copy of the entire list back.
            acc.jumps = jumps[:]
    
    acc.min_turns = 100
    
    # Explore 3 options for which coin to remove first
    for coin in ((0, 0), (0, 1), (1, 2)):
        find_solutions(new_grid(coin), None, 0, [], acc)
    
    return acc.min_turns, acc.jumps

# The solution in "raw" form
num_turns, jumps = find_minimum()

# Everything after this point is dedicated to pretty printing the solution

def convert_point(point):
    '''
    Converts points to this form:
    https://www.think-maths.co.uk/sites/default/files/2020-04/CoinGrid_1.png
    '''
    x, y = point
    # Uses triangular numbers of course :)
    return 1 + x + y * (y + 1) // 2

def chain_jumps(jumps):
    ''' This peices together the individual jumps into moves '''
    result = []
    prev_end = None
    
    for start, end in jumps:
        if start != prev_end:
            # This jump is the start of a new move
            chain = [start, end]
            result.append(chain)
        else:
            # This jump continues the current chain of jumps and is part of the
            # same move
            chain.append(end)
        
        prev_end = end
    
    return result

def format_move(move):
    return '-'.join(str(convert_point(p)) for p in move)

# The end point of the first jump must be the initial coin removed
print('Remove %d' % convert_point(jumps[0][1]))
print('Moves: ' + ', '.join(format_move(m) for m in chain_jumps(jumps)))

# Output:
# Remove 2
# Moves: 7-2, 1-4, 9-7-2, 6-1-4-6, 10-3