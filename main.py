import math, time

def getSudoku(fileName):
    f = open(fileName, "r")
    rows = f.read().split("\n")

    width, height = len(rows[0].split()), len(rows)
    sudoku = [[0 for x in range(width)] for y in range(height)]

    for index in range(height):
        columns = rows[index].split()
        for counter, column in enumerate(columns):
            sudoku[index][counter] = (int)(columns[counter])

    return sudoku

def prettyPrint(sudoku):
    length = len(sudoku)
    result = ""
    for x in range(length):
        for y in range(length):
            result += str(sudoku[x][y]) + " "
        result += "\n"

    return result

def fillBlock(sudoku,newSudoku,rowNumber, columnNumber):
    sudokuSize =len(sudoku)
    domain = set(i + 1 for i in range(sudokuSize))

    blockLength = int(math.sqrt(sudokuSize))
    blockRow = rowNumber - rowNumber % blockLength
    blockColumn = columnNumber - columnNumber % blockLength
    for x in range(blockLength):
        for y in range(blockLength):
            domain.discard(sudoku[blockRow + x][blockColumn + y])
    for x in range(blockLength):
        for y in range(blockLength):
            if sudoku[blockRow + x][blockColumn + y] == 0:
                newSudoku[blockRow + x][blockColumn + y] = domain.pop()
            else: newSudoku[blockRow + x][blockColumn + y] = sudoku[blockRow + x][blockColumn + y]

def fillSudoku(sudoku):
    sudokuSize = len(sudoku)
    newSudoku= [[0 for x in range(sudokuSize)] for y in range(sudokuSize)]
    blockLength = int(math.sqrt(sudokuSize))
    for x in range (blockLength):
        for y in range (blockLength):
            fillBlock(sudoku,newSudoku,x*blockLength,y*blockLength)
    return newSudoku

class Counter:
    i = 0

    def up(self):
        self.i = self.i + 1

    def count(self):
        return self.i

if __name__ == '__main__':
    sudoku = getSudoku("sudoku.txt")
    newSudoku = fillSudoku(sudoku)
    start_time = time.time()
    counter = Counter()
    print prettyPrint(newSudoku)

    print "Run Time:", (time.time() - start_time) * 1000, "milliseconds"