import time
from recognizer import Recognizer
from pynput.mouse import Button, Controller

class Solver(object):
    def __init__(self, recognizer, mines):
        self.recognizer = recognizer
        self.mines = mines

        self.grid = self.recognizer.getUpdatedGrid()

        self.mouse = Controller()

        # self._click(0, 0)
        # for y, t in enumerate(self.grid):
        #     for x, num in enumerate(self.grid[y]):
        #         if self.shouldStop(): return
        #         if(num == -1):
        #             self._click(x, y, right=True)

    def badTileEncountered(self):
        for y, t in enumerate(self.grid):
            for x, num in enumerate(self.grid[y]):
                if(Recognizer.numsToChars[num] == 'L' or Recognizer.numsToChars[num] == 'B'):
                    return True
        return False
    
    def solve(self, shouldContinue):
        # Click middle of screen to get started
        self._click(int(self.recognizer.columns/2), int(self.recognizer.rows/2))

        while not self.badTileEncountered() and shouldContinue():
            print("Solving...")
            time.sleep(0.1)

    def _click(self, x, y, right=False):
        if((y >= len(self.grid) or y < 0) or (x >= len(self.grid[0]) or x < 0)):
            raise Exception("_click called on non-existant tile")
        self.mouse.position = self.recognizer.getTileCenter(x, y)
        self.mouse.press(Button.left if right == False else Button.right)
        self.mouse.release(Button.left if right == False else Button.right)
        self.grid = self.recognizer.getUpdatedGrid()