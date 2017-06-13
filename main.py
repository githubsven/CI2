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

class Counter:
    i = 0

    def up(self):
        self.i = self.i + 1

    def count(self):
        return self.i

if __name__ == '__main__':
    sudoku = getSudoku("sudoku.txt")
    start_time = time.time()
    counter = Counter()

    print "Run Time:", (time.time() - start_time) * 1000, "milliseconds"