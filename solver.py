import time
from recognizer import Recognizer
from analyzer import Analyzer
from pynput.mouse import Button, Controller

class Solver(object):
    def __init__(self, recognizer : Recognizer, analyzer : Analyzer, mines):
        self.analyzer = analyzer
        self.recognizer = recognizer
        self.mines = mines
        self.minesRemaining = mines
        self.mouse = Controller()
        self.badTileEncountered = False
        self.actionTaken = False
    
    def solve(self, shouldContinue):
        # Click middle of screen to get started
        self._click(int(self.analyzer.width/2), int(self.analyzer.height/2))
        self.recognizer.printUpdatedBoard()
        self.solveLoop(shouldContinue)
        #self.recognizer.printUpdatedBoard()
        print("All done!" if not self.badTileEncountered else "Whoops...")
        self.recognizer.printUpdatedBoard()

    def solveLoop(self, shouldContinue):
        while True:
            self.actionTaken = False
            for y in range(self.analyzer.height):
                for x in range(self.analyzer.width):
                    if(self.badTileEncountered or not shouldContinue()): return
                    # Find data
                    tileNum = self.analyzer.getTileNumber(x, y)
                    surroundingUnknownIndicies = self.analyzer.getIndiciesOfSurroundingVarient(x, y, -1)
                    numOfSurroundingFlags = len(self.analyzer.getIndiciesOfSurroundingVarient(x, y, 'F'))
                    # Run actual algorithms
                    self._definiteFlag(x, y, tileNum, surroundingUnknownIndicies, numOfSurroundingFlags)
                    self._definiteClick(x, y, tileNum, surroundingUnknownIndicies, numOfSurroundingFlags)
            #self._checkForPatterns()
            if not self.actionTaken: return

    def _click(self, x, y, right=False):
        self.actionTaken = True
        self._point(x, y)
        self.mouse.press(Button.left if right == False else Button.right)
        time.sleep(0.1)
        self.mouse.release(Button.left if right == False else Button.right)
        # If flag placed, add to count
        if right: self.minesRemaining -= 1
        # Sleep a little to give the board a chance to update
        time.sleep(0.1)
        self.recognizer.updateGrid()
        # Check for bad tile
        if (not right and self.analyzer.getTileChar(x, y) == 'B') or \
           (self.analyzer.getNumberOfSurroundingVarient(x, y, 'L') > 0):
            self.badTileEncountered = True

    def _point(self, x, y):
        if(not self.analyzer.tileInGrid(x, y)):
            raise Exception("_click called on non-existant tile")
        self.mouse.position = self.analyzer.recognizer.getTileCenter(x, y)

    # Specific solving algorithms
    def _definiteFlag(self, x, y, tileNum, surroundingUnknownIndicies, numOfSurroundingFlags):
        if(tileNum > 0 and (tileNum == len(surroundingUnknownIndicies) + numOfSurroundingFlags)):
            for indicies in surroundingUnknownIndicies:
                self._click(indicies[0], indicies[1], right=True)
    
    def _definiteClick(self, x, y, tileNum, surroundingUnknownIndicies, numOfSurroundingFlags):
        if(tileNum > 0 and (tileNum == numOfSurroundingFlags)):
            for indicies in surroundingUnknownIndicies:
                self._click(indicies[0], indicies[1])

    # def _checkForPatterns(self):
    #     # Only run if previous methods have failed
    #     if not self.actionTaken:
    #         unknownCounts = {}
    #         # Update table of unknown tile possibilities
    #         for y in range(self.analyzer.height):
    #             for x in range(self.analyzer.width):
    #                 tileNum = self.analyzer.getTileNumber(x, y)
    #                 if tileNum > 0:
    #                     surroundingUnknownIndicies = self.analyzer.getIndiciesOfSurroundingVarient(x, y, -1)
    #                     numOfSurroundingFlags = len(self.analyzer.getIndiciesOfSurroundingVarient(x, y, 'F'))
    #                     rating = tileNum - numOfSurroundingFlags
    #                     #if(numOfSurroundingFlags > 0):
    #                     for unknownIndicies in surroundingUnknownIndicies:
    #                         if unknownIndicies not in unknownCounts:
    #                             unknownCounts[unknownIndicies] = (0, 0)
    #                         if rating > 0:
    #                             unknownCounts[unknownIndicies] = (unknownCounts[unknownIndicies][0] + 1, max([unknownCounts[unknownIndicies][1], rating]))

    #         if(len(unknownCounts) == 0): return

    #         # Print out
    #         for y in range(self.analyzer.height):
    #             for x in range(self.analyzer.width):
    #                 text = "" if (x, y) not in unknownCounts else str(unknownCounts[(x, y)][0]) 
    #                 # if text == "0":
    #                 #     text = ""
    #                 print(text.rjust(3, " "), end="")
    #             print()

    #         # Check patterns
    #         self._twoDownOneUp(unknownCounts)
    #         self._twoUpOneDown(unknownCounts)

    #         # maxIndicies = (-1, -1)
    #         # maxValue = -1
    #         # for k in unknownCounts.keys():
    #         #     v = unknownCounts[k]
    #         #     if((v > maxValue) and v > 1):
    #         #         maxValue = v
    #         #         maxIndicies = k

    #         # if(maxValue is not 100):
    #         #     self._point(maxIndicies[0], maxIndicies[1])

    #         # lessThanList = []
    #         # for k in unknownCounts.keys():
    #         #     surrounding = list(self.recognizer.getSurroundingIndicies(k[0], k[1]))
    #         #     for indicies in surrounding:
    #         #         if(indicies in unknownCounts):
    #         #             # check if decreasing
    #         #             if(unknownCounts[k][0] > unknownCounts[indicies][0] + 1):
    #         #                 if(k not in lessThanList):
    #         #                     lessThanList.append(k)

    #         #print(lessThanList)

    # # When two unknown counts are one less than another in a line, mark the one up as a mine
    # def _twoDownOneUp(self, unknownCounts):
    #     for blockOne in unknownCounts:
    #         for blockTwo in self.recognizer.getSurroundingIndicies(blockOne[0], blockOne[1]):
    #             if(blockTwo in unknownCounts):
    #                 if(unknownCounts[blockOne][0] == unknownCounts[blockTwo][0]):
    #                     #print("Same ", blockOne, blockTwo)
    #                     for blockThree in self.recognizer.getSurroundingIndicies(blockTwo[0], blockTwo[1]):
    #                         if((blockThree[0] - blockTwo[0] == blockTwo[0] - blockOne[0] or blockThree[1] - blockTwo[1] == blockTwo[1] - blockOne[1]) and blockThree in unknownCounts):
    #                             if(unknownCounts[blockTwo][0] + 1 == unknownCounts[blockThree][0]):
    #                                 print("TwoDownOneUp ", blockOne, blockTwo, blockThree)
    #                                 self._click(blockThree[0], blockThree[1], right=True) # Right Click
    #                                 self._point(blockOne[0], blockOne[1])
    #                                 time.sleep(2)
    #                                 self._point(blockTwo[0], blockTwo[1])
    #                                 time.sleep(2)
    #                                 self._point(blockThree[0], blockThree[1])
    #                                 time.sleep(2)
    #                             if(unknownCounts[blockTwo][0] - 1 == unknownCounts[blockThree][0]):
    #                                 print("TwoUpOneDown ", blockOne, blockTwo, blockThree)
    #                                 self._click(blockThree[0], blockThree[1]) # Left Click
    #                                 self._point(blockOne[0], blockOne[1])
    #                                 time.sleep(2)
    #                                 self._point(blockTwo[0], blockTwo[1])
    #                                 time.sleep(2)
    #                                 self._point(blockThree[0], blockThree[1])
    #                                 time.sleep(2)

    # def _twoUpOneDown(self, unknownCounts):
    #     pass
