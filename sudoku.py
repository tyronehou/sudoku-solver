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
        
def solve(grid, i=0, tried=[], count=0):
    count += 1
    # Check the current square for contradictions
    cell = grid[i]
    #print('\nNEW SOLVE\ni:{}\ntried: {}\ncell: {}\ngrid:'.format(i, tried, cell))
    #print_puzzle(grid)

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
            #print_puzzle(grid)

            return None, count
        
        # find the next non-empty square and solve it
        try:
            i = grid.index('0', i)
        except ValueError:
            i = -1

        tried = []

    # At this point if the grid is full return a solution
    if i is -1: return grid, count
    
    for num in range(1, 10):
        if num in tried:
            continue
        
        grid[i] = str(num)
        tried.append(num)

        answer, count = solve(grid, i, tried, count)
        if answer is not None:
            return answer, count

    # If there's no solution for this square, return things to normal
    #print('Really no solution')
    #print_puzzle(grid)
    grid[i] = '0'
    return None, count


def verify(rows, cols, sqrs):
    ''' Verify whether the rows, columns, and squares
        passed in constitute an actual sudoku
        solution '''
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

def print_list(lst):
    print('\n'.join([str(item) for item in lst]))
    
if __name__ == '__main__':
    puzzle1 = list('006002304'+'002060000'+'007005060'+ \
                   '860300702'+'059248630'+'301006085'+ \
                   '070100900'+'000090500'+'408500100')

    puzzle2 = list('000000200'+'000260708'+'870000001'+ \
                   '060901000'+'009070100'+'000405080'+ \
                   '600000049'+'108034000'+'007000000')

    answer, count = solve(puzzle2[:])

    print('Problem')
    print_puzzle(puzzle2)

    print('Solution')
    print_puzzle(answer)
    print('number of recursive calls:', count)

    assert verify(*parse(answer))
    print('Solution verified')
