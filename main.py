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

    print result

def fillBlock(sudoku,rowNumber, columnNumber):
    sudokuSize =len(sudoku)
    domain = set(i + 1 for i in range(sudokuSize))

    blockLength = int(math.sqrt(sudokuSize))
    blockRow = rowNumber - rowNumber % blockLength
    blockColumn = columnNumber - columnNumber % blockLength
    for x in range(blockLength):
        for y in range(blockLength):
            domain.discard(sudoku[blockRow + x][blockColumn + y].value)
    domain = list(domain)
    random.shuffle(domain)
    #domain = domain[::-1]
    #print domain
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

def switchSquares(sudoku, (firstRow, firstCol), (secondRow, secondCol)):
    temp = sudoku[firstRow][firstCol]
    sudoku[firstRow][firstCol] = sudoku[secondRow][secondCol]
    sudoku[secondRow][secondCol] = temp

def updateEvaluation(sudoku, (firstRow, firstCol), (secondRow, secondCol)):
    #Bereken de score van de huidige indeling (alleen van de row/col)
    #Bereken de score van de nieuwe indeling
    #return het verschil tussen de twee (om te kijken of de nieuwe beter is)
    currentScore = getScore(sudoku, firstRow, firstCol) + getScore(sudoku, secondRow, secondCol)
    switchSquares(sudoku, (firstRow, firstCol), (secondRow, secondCol))
    newScore = getScore(sudoku, firstRow, firstCol) + getScore(sudoku, secondRow, secondCol)
    switchSquares(sudoku, (firstRow, firstCol), (secondRow, secondCol))

    return newScore - currentScore

def getScore(sudoku, row, col):
    score = 0

    # Loop over iedere rij en tel het aantal nummers dat ontbreekt
    domain = set(i + 1 for i in range(len(sudoku)))
    for x in range(len(sudoku)):
        domain.discard(sudoku[x][col].value)
    score += len(domain)

    #Loop over iedere kolom en tel het aantal nummers dat ontbreekt
    domain = set(i + 1 for i in range(len(sudoku)))
    for y in range(len(sudoku)):
        domain.discard(sudoku[row][y].value)
    score += len(domain)

    return score

def initialEvaluation(sudoku, score):
    score.reset()
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

def getRandomBlockList(sudoku):
    randInt = random.randint(0, len(sudoku) - 1)
    length = int(math.sqrt(len(sudoku)))
    blockRow = int(randInt / length * length)
    blockColumn = randInt % length * length

    blockList = []
    for x in range(length):
        for y in range(length):
            if not sudoku[blockRow + x][blockColumn + y].isFixed:
                blockList.append((blockRow + x, blockColumn + y))
    return blockList

def randomWalk(sudoku, S):
    blockSwitchAmount = 1
    squareSwitchAmount = 1

    #prettyPrint(sudoku)
    for i in range(S):
        for i in range(blockSwitchAmount):
            blockList = getRandomBlockList(sudoku)
            for j in range(squareSwitchAmount):
                firstSquare = blockList[random.randint(0, len(blockList) - 1)]
                secondSquare = blockList[random.randint(0, len(blockList) - 1)]
                switchSquares(sudoku, firstSquare, secondSquare)

    #prettyPrint(sudoku)

def iteratedLocalSearch(sudoku, score, counter, s, noImprovementCounter = 0, randomWalkCounter = 0):
    initialScore = score.count()
    if initialScore < 100:
        maxWalks = 100
    elif initialScore < 200:
        maxWalks = 200
    elif initialScore < 300:
        maxWalks = 300
    else: maxWalks = 400
    while score.count() != 0 and randomWalkCounter < maxWalks:
        counter.plus(1)

        blockList = getRandomBlockList(sudoku)
        bestSwap = ((0, 0), (0, 0), 0) #((firstSquare), (secondSquare), swapScore)

        for i in range(len(blockList)):
            firstSquare = blockList.pop()
            for j in range(len(blockList)):
                secondSquare = blockList[j]
                evaluation = updateEvaluation(sudoku, firstSquare, secondSquare) #bereken de verandering van de score
                if evaluation < bestSwap[2]:
                    bestSwap = (firstSquare, secondSquare, evaluation)
                elif evaluation == bestSwap[2]:
                    acceptNeutralSwap = random.randint(0, 10) > 5
                    if acceptNeutralSwap:
                        bestSwap = (firstSquare, secondSquare, evaluation)

        if bestSwap != ((0, 0), (0, 0), 0):
            switchSquares(sudoku, bestSwap[0], bestSwap[1]) #apply the best swap

        if bestSwap[2] == 0: #if there was no improvement
            noImprovementCounter += 1
        else:
            score.plus(bestSwap[2])

        if noImprovementCounter >= (maxWalks):
            randomWalk(sudoku, s)
            initialEvaluation(sudoku, score)
            noImprovementCounter = 0
            randomWalkCounter += 1

    #print randomWalkCounter
    return True

class Score:
    i = 0

    def plus(self, other):
        self.i = self.i + other
        return self.i + other

    def reset(self):
        self.i = 0

    def count(self):
        return self.i

class Square:
    value = 0
    isFixed = False

if __name__ == '__main__':
    file = open("test2.txt", "a")
    file2 = open("test3.txt", "a+")
    #random.seed(100)
    avgIt = 0
    avgTime = 0
    goes = 4
    sMax = 30
    tried = goes

    file.write("times ran" + str(goes) + "\n")
    file2.write("times ran " + str(goes) + "\n")
    for sudokuNr in [16,17]:
        fileSudoku = open("results"+str(sudokuNr)+".txt", "a+")
        fileSudoku.write("times ran " + str(goes) + "\n")
        print sudokuNr
        sudokuFile = "sudoku" + str(sudokuNr) + ".txt"
        file2.write("Sudoku " + str(sudokuNr) + "\n")
        for s in range(5, 6, 1):
            print s
            avgIt = 0
            avgTime = 0
            timesNotSolved = 0
            #file.write("s value "+ str(s)+ "\n")
            file2.write("s value " + str(s) + "\n")
            fileSudoku.write("s value " + str(s) + "\n")
            for i in range(goes):
                #file2.write("difficulty " + str(score.count()) + "\n")
                #fileSudoku.write("difficulty " + str(score.count()) + "\n")
                sudokuFile = "sudoku"+str(sudokuNr)+".txt"
                sudoku = getSudoku(sudokuFile)
                fillSudoku(sudoku)

                score = Score()
                counter = Score()

                initialEvaluation(sudoku, score)
                print score.count()

                start_time = time.time()

                solved = iteratedLocalSearch(sudoku, score, counter, s)
                #prettyPrint(sudoku)
                #print score.count()
                #print counter.count()
                x = (time.time() - start_time) * 1000
                y = counter.count()
                #print "Run Time:", x, "milliseconds"
                avgIt += y
                avgTime += x


                file.write(sudokuFile+"\n")
                file.write(str(score.count())+"\n")
                file.write(str(y)+"\n")
                file.write("Run Time: "+str(x)+" milliseconds\n")
                if score.count() > 0:
                    timesNotSolved += 1
                    avgTime -=x
                    avgIt -=y
                #if avgTime > 300000:
                 #   file.write("times completed "+ str(i+1)+ "\n")
                  #  file2.write("times completed " + str(i+1) + "\n")
                   # fileSudoku.write("times completed " + str(i+1) + "\n")
                    #tried = i+1
                    #break


            file.write("average time: " + str(avgTime/tried-timesNotSolved)+"\n")
            file.write("average iterations: " + str(avgIt / tried-timesNotSolved) + "\n")
            file.write("Times not solved: " + str(timesNotSolved) + "\n")
            file2.write("average time: " + str(avgTime / tried-timesNotSolved) + "\n")
            file2.write("average iterations: " + str(avgIt / tried-timesNotSolved) + "\n")
            file2.write("Times not solved: " + str(timesNotSolved) + "\n")
            fileSudoku.write("average time: " + str(avgTime / tried-timesNotSolved) + "\n")
            fileSudoku.write("average iterations: " + str(avgIt / tried-timesNotSolved) + "\n")
            fileSudoku.write("Times not solved: " + str(timesNotSolved) + "\n")
        fileSudoku.close()
    file.close()
    file2.close()

