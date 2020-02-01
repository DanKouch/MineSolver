from recognizer import Recognizer

class Analyzer(object):
    def __init__(self, recognizer: Recognizer):
        self.recognizer = recognizer
        self.width = self.recognizer.columns
        self.height = self.recognizer.rows
        self.tileInGrid = self.recognizer.tileInGrid

    def getTileNumber(self, x, y):
        return self.recognizer.grid[y][x]

    def getTileChar(self, x, y):
        return Recognizer.numsToChars[self.recognizer.grid[y][x]]

    def getSurroundingNumbers(self, x, y):
        return map(lambda indicies: self.getTileNumber(indicies[0], indicies[1]),self.recognizer.getSurroundingIndicies(x, y))

    def getSurroundingChars(self, x, y):
        return map(lambda indicies: self.getTileChar(indicies[0], indicies[1]),self.recognizer.getSurroundingIndicies(x, y))
    
    def getNumberOfSurroundingVarient(self, x, y, varient):
        out = 0
        v = varient if type(varient) is int else Recognizer.charsToNums[varient]
        for n in self.getSurroundingNumbers(x, y):
            if n == v:
                out += 1
        return out

    def getIndiciesOfSurroundingVarient(self, x, y, varient):
        out = []
        v = varient if type(varient) is int else Recognizer.charsToNums[varient]
        for indicies in self.recognizer.getSurroundingIndicies(x, y):
            if(self.getTileNumber(indicies[0], indicies[1]) == v):
                out.append(indicies)
        return out

    def areAdjacent(self, pos1, pos2):
        for indicies in self.recognizer.getSurroundingIndicies(pos1[0], pos1[1]):
            if(indicies == pos2):
                return True
        return False