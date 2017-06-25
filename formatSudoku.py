def formatSudoku(fileName):
    f = open(fileName, "r")
    rows = f.read().split("\n")
    width, height = len(rows), len(rows)
    sudoku = [[0 for x in range(width)] for y in range(height)]

    for index in range(height):
        for i in range(width):
            sudoku[index][i] = rows[index][i]
    f.close()
    open(fileName, 'w').close()

    f = open(fileName, 'w')

    for index in range(height - 1):
        f.write(" ".join(sudoku[index]) + "\n")
    f.write(" ".join(sudoku[index]))

    f.close()

if __name__ == '__main__':
    formatSudoku("sudoku6.txt")