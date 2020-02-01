import mss
import mss.tools
from PIL import Image
import math

class Recognizer(object):

    referenceAverages = {
        -5: (233, 113, 113), # flags
        -10: (24, 15, 15), # bombs (exploded)
        -1: (229, 229, 229), # unknown
        0: (218, 218, 218),
        1: (169, 169, 226),
        2: (182, 203, 182),
        3: (222, 192, 192),
        4: (146, 146, 188),
        5: (198, 170, 170),
        6: (137, 185, 185),
        7: (179, 179, 179), #179 originally
        8: (185, 185, 185) #185 originally
    }

    referenceColors = {
        -20: (255, 153, 153), # pink area
        -5: (255, 3, 3), # flags
        -10: (255, 255, 255), # bombs (exploded)
        -1: (229, 229, 229), # unknown
        #0: (218, 218, 218),
        1: (0, 0, 255),
        2: (0, 128, 0),
        3: (255, 0, 0),
        4: (12, 12, 133),
        5: (143, 37, 37),
        6: (37, 143, 143),
        7: (37, 37, 37),
        8: (143, 143, 143)
    }

    numsToChars = {
        -20: 'L',
        -5: 'F',
        -10: 'B',
        -1: ' ',
        0: '-',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8'
    }

    charsToNums = {
        'L': -20,
        'F': -5,
        'B': -10,
        ' ': -1,
        '-': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8
    }

    def __init__(self, topLeftCoords, bottomRightCoords, rows, columns):
        self.topLeftCoords = topLeftCoords
        self.bottomRightCoords = bottomRightCoords
        self.rows = rows
        self.columns = columns
        self.grid = [[]]

        self.width = self.bottomRightCoords[0] - self.topLeftCoords[0]
        self.height = self.bottomRightCoords[1] - self.topLeftCoords[1]

        # Find the size of each grid tile
        averageGridWidth = (self.bottomRightCoords[0] - self.topLeftCoords[0])/self.columns
        averageGridHeight = (self.bottomRightCoords[1] - self.topLeftCoords[1])/self.rows
        if abs(averageGridHeight - averageGridWidth) > 20:
            print("Warning: Is it just me, or is the grid made up of non-square rectangles?")
        self.averageGridSize = int((averageGridWidth + averageGridHeight)/2)

        self.sct = mss.mss()
        self.sct.compression_level = 1
        self.sctSection = {
            "top": self.topLeftCoords[1],
            "left": self.topLeftCoords[0],
            "width": self.width,
            "height": self.height
        }

        self.updateGrid()

    def updateGrid(self):
        self._updateBoardImage()
        self.grid = []
        for y in range(self.rows):
            self.grid.append([])
            for x in range(self.columns):
                self.grid[y].append(self._identifyTileByAverage(x, y)[0])

    def update3x3(self, x, y):
        self._updateBoardImage()
        for indicies in self.getChunkIndicies(x, y):
            x, y = indicies
            self.grid[y][x] = self._identifyTileByAverage(x, y)[0]

    def getChunkIndicies(self, x, y):
        indicies = self.getSurroundingIndicies(x, y)
        indicies.insert(4, (x, y))
        return indicies

    def tileInGrid(self, x, y):
        return not ((y >= len(self.grid) or y < 0) or (x >= len(self.grid[0]) or x < 0))

    def getSurroundingIndicies(self, x, y):
        return filter(lambda indicies: self.tileInGrid(indicies[0], indicies[1]),[
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1)
        ])

    def printUpdatedBoard(self):
        #self._updateBoardImage()
        precision = []
        for y in range(self.rows):
            for x in range(self.columns):
                nearest = self._identifyTileByAverage(x, y)
                precision.append(nearest[1])
                print(Recognizer.numsToChars[nearest[0]].rjust(3, " "), end="")
            print("")
        print("Precision Output - Max: ", round(max(precision), 3), "  Min: ", round(min(precision), 3))

    def _updateBoardImage(self):
        boardImageData = self.sct.grab(self.sctSection)
        self.boardImage = Image.frombytes("RGB", boardImageData.size, boardImageData.bgra, "raw", "BGRX")


    def _identifyTileByAverage(self, x, y):
        tileImage = self._getCroppedSubTile(x, y)
        averageColor = tileImage.resize((1, 1), Image.ANTIALIAS).getpixel((0, 0))
        nearest = self._findClosestAverage(averageColor)

        # Look for pink
        if(nearest[1] > 25):
            if((255, 153, 153) in list(tileImage.getdata())):
                nearest = (-20, -1)

        # 7 extrema: 58
        # 8 extrema: 139
        # Cutoff: 99
        if(nearest[0] == 7 or nearest[0] == 8):
            nearest = (7 if tileImage.getextrema()[0][0] < 99 else 8, -1)

        return nearest

    def getTileCenter(self, x, y):
        return (self.topLeftCoords[0] + x*self.averageGridSize + self.averageGridSize/2,
                self.topLeftCoords[1] + y*self.averageGridSize + self.averageGridSize/2)

    def _getCroppedSubTile(self, x, y):
        startingX = x*self.averageGridSize + self.averageGridSize/3
        startingY = y*self.averageGridSize + self.averageGridSize/3
        return self.boardImage.crop((startingX, startingY, startingX + self.averageGridSize/3, startingY + self.averageGridSize/3))

    def _findClosestAverage(self, color):
        smallestDistance = 1000
        closest = -100
        for key in Recognizer.referenceAverages:
            distance = self._colorDistance(color, Recognizer.referenceAverages[key])
            if distance < smallestDistance:
                smallestDistance = distance
                closest = key
        return (closest, smallestDistance)

    def _colorDistance(self, color1, color2):
        return math.sqrt(math.pow(color2[0]-color1[0], 2) + math.pow(color2[1]-color1[1], 2)+ math.pow(color2[2]-color1[2], 2))