import time
# TODOS:
# 1 rewrite verify function
# 2 change how counting recursive calls works (add a seperate count calls class
# and decorate?)
# 3 add web scraper
# 4 add AI reader for puzzles from pictures

# Sudoku puzzle solver
def print_puzzle(puzzle):
    puz_str = ''
    for i, cell in enumerate(puzzle):
        puz_str += cell
        row = i // 9
        col = i % 9

        if col == 2 or col == 5:
            puz_str += ' '
        if col == 8:
            puz_str += '\n'
            if row % 3 == 2:
                puz_str += '\n'
            
    print(puz_str, end='')

def parse(grid):
    assert len(grid) == 81
    ''' Parses an iterable sudoku grid of length 81 and
        returns a triple of the rows, columns, and squares
        making up the grid'''

    rows = [grid[r:r+9] for r in range(0,81,9)]
    cols = [grid[c::9] for c in range(9)]
    sqrs = []
    for b in range(0,81,27):
        for s in range(b,b+9,3):
            sqr = [grid[cell] for s_row in range(s,s+19,9)
                              for cell in range(s_row, s_row+3)]
            sqrs.append(sqr)

    return rows, cols, sqrs

def solve(grid, get_all=False):
    ''' Calls the _solve function with specified parameters '''
    #Creates a copy of the passed in puzzle before passing to _solve
    return _solve(grid[:], get_all=get_all)

def _solve(grid, i=0, tried=[], get_all=False):
    cell = grid[i]
    #print('\nNEW SOLVE\ni:{}\ntried: {}\ncell: {}\ngrid:'.format(i, tried, cell))

    # Check the current square for contradictions
    if cell is not '0':
        r, c = i//9 * 9, i%9
        s = (r//27) * 27 + (c//3) * 3
        row, col, sqr = grid[r:r+9], grid[c::9], []
        for s_row in range(s, s+27, 9):
            sqr.extend(grid[s_row:s_row+3])
        
        #print('row: {}\n{}\ncol: {}\n{}\nsqr: {}\n{}'.format(r, row, c, col, s1, sqr))

        # In order not to match the current cell with itself
        row.pop(row.index(cell))
        col.pop(col.index(cell))
        sqr.pop(sqr.index(cell))
        
        rcs = set(row+col+sqr)
        rcs.discard('0')
        # if no solution exists, return None
        if cell in rcs:
            #print('No solution by contradiction')
            return None, 1
        
        # find the next non-empty square and solve it
        try:
            i = grid.index('0', i)
        except ValueError:
            i = -1

        tried = []

    # At this point if the grid is full return a solution
    if i is -1:
        return [grid[:]], 1

    answers = []
    count = 1
    for num in range(1, 10):
        if num in tried:
            continue
        
        grid[i] = str(num)
        tried.append(num)
        answer, sub_count = _solve(grid, i, tried, get_all=get_all)

        count += sub_count       
        if answer:
            if get_all: answers.extend(answer)
            else: return answer, count

    # If there's no solution for this square, return things to normal
    grid[i] = '0'
    if get_all:
        return answers, count
    else:
        return None, count

def verify(rows, cols, sqrs):
    ''' Verify whether the rows, columns, and squares
        passed in could potentially constitute an actual sudoku
        solution; that is, there are no contradictions among any
        of them '''
    all_nums = {str(x) for x in range(1, 10)}
    
    # Check rows
    for row in rows:
        if set(row) != all_nums:
            return False

    # Check cols
    for col in cols:
        if set(col) != all_nums:
            return False

    # Check sqrs
    for sqr in sqrs:
        if set(sqr) != all_nums:
            return False

    return True    

def true_count():
    with open(f_name, 'r') as f:
        s = f.read()

    return len(s)
    
def print_list(lst):
    print('\n'.join([str(item) for item in lst]))
    
if __name__ == '__main__':
    puzzle = list('006002304'+'002060000'+'007005060'+ \
                   '860300702'+'059248630'+'301006085'+ \
                   '070100900'+'000090500'+'408500100')

    puzzle = list('000000200'+'000260708'+'870000001'+ \
                   '060901000'+'009070100'+'000405080'+ \
                   '600000049'+'108034000'+'007000000')

    puzzle = list('906070403'+'000400200'+'070023010'+ \
                  '500000100'+'040208060'+'003000005'+ \
                  '030700050'+'007005000'+'405010708')
    get_all = True
    #puzzle = ['0' for i in range(81)] # total number of possible solutions
    start = time.time()
    answer, count = solve(puzzle, get_all=get_all)
    time_taken = time.time() - start

    if not get_all: answer = [answer]
    
    print('Problem')
    print_puzzle(puzzle)
    
    print('Solutions')
    print('# of solutions:', len(answer))

    for i, a in enumerate(answer):
        print('#', i)
        print_puzzle(a)

    print('number of recursive calls:', count)

    for i, a in enumerate(answer):
        assert verify(*parse(a)), 'answer {} is wrong'.format(i)
    print('Solution(s) verified')

    print('Time taken to solve:', time_taken)

