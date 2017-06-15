import random, math, time

def getSudoku(fileName):
    f = open(fileName, "r")
    rows = f.read().split("\n")

    width, height = len(rows[0].split()), len(rows)
    sudoku = [[Square() for x in range(width)] for y in range(height)]

    for index in range(height):
        columns = rows[index].split()
        for counter, column in enumerate(columns):
            val = (int)(columns[counter])
            if val != 0:
                sudoku[index][counter].isFixed = True
            sudoku[index][counter].value = (int)(columns[counter])

    return sudoku

def prettyPrint(sudoku):
    length = len(sudoku)
    result = ""
    for x in range(length):
        for y in range(length):
            result += str(sudoku[x][y].value) + " "
        result += "\n"

    return result

def fillBlock(sudoku,rowNumber, columnNumber):
    sudokuSize =len(sudoku)
    domain = set(i + 1 for i in range(sudokuSize))

    blockLength = int(math.sqrt(sudokuSize))
    blockRow = rowNumber - rowNumber % blockLength
    blockColumn = columnNumber - columnNumber % blockLength
    for x in range(blockLength):
        for y in range(blockLength):
            domain.discard(sudoku[blockRow + x][blockColumn + y].value)
    for x in range(blockLength):
        for y in range(blockLength):
            if sudoku[blockRow + x][blockColumn + y].value == 0:
                sudoku[blockRow + x][blockColumn + y].value = domain.pop()
            #else: newSudoku[blockRow + x][blockColumn + y] = sudoku[blockRow + x][blockColumn + y]

def fillSudoku(sudoku):
    sudokuSize = len(sudoku)
    #newSudoku= [[0 for x in range(sudokuSize)] for y in range(sudokuSize)]
    blockLength = int(math.sqrt(sudokuSize))
    for x in range (blockLength):
        for y in range (blockLength):
            fillBlock(sudoku,x*blockLength,y*blockLength)
    #return newSudoku

def switchSquares(sudoku, (firstRow, firstCol, secondRow, secondCol)):
    return 0

def updateEvaluation(sudoku, evaluationValue, firstRow, firstCol, secondRow, secondCol):
    return 0

def initialEvaluation(sudoku, score):
    #Loop over iedere rij en tel het aantal nummers dat ontbreekt
    for x in range(len(sudoku)):
        domain = set(i + 1 for i in range(len(sudoku)))
        for y in range(len(sudoku)):
            domain.discard(sudoku[x][y].value)
        score.plus(len(domain))

    #Loop over iedere kolom en tel het aantal nummers dat ontbreekt
    for y in range(len(sudoku)):
        domain = set(i + 1 for i in range(len(sudoku)))
        for x in range(len(sudoku)):
            domain.discard(sudoku[x][y].value)
        score.plus(len(domain))

def inBlock(sudoku, rowNumber, columnNumber, number):
    length = int(math.sqrt(len(sudoku)))
    blockRow = rowNumber - rowNumber % length
    blockColumn = columnNumber - columnNumber % length
    for x in range(length):
        for y in range(length):
            if sudoku[blockRow + x][blockColumn + y] == number:
                return True
    return False

def iteratedLocalSearch(sudoku, score):

    top = len(sudoku)-1
    firstRandomRow = random.randint(0, top)
    firstRandomColumn = random.randint(0, top)
    print firstRandomRow
    #secondRandomRow = random.randint(0, len(sudoku)-1)
    #secondRandomColumn = random.randint(0, len(sudoku)-1)
    print firstRandomColumn
    #print secondRandomColumn
    return 0


class Score:
    i = 0

    def plus(self, other):
        self.i = self.i + other
        return self.i + other

    def count(self):
        return self.i

class Square:
    value = 0
    isFixed = False

if __name__ == '__main__':
    sudoku = getSudoku("sudoku.txt")
    fillSudoku(sudoku)
    score = Score()
    random.seed(100)


    initialEvaluation(sudoku, score)
    print score.count()
    start_time = time.time()



    iteratedLocalSearch(sudoku, score)
    print prettyPrint(sudoku)
    print "Run Time:", (time.time() - start_time) * 1000, "milliseconds"

