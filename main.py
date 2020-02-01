#!/usr/bin/python

from pynput import keyboard
import time

from interface import MineSolverInterface
from recognizer import Recognizer
from analyzer import Analyzer
from solver import Solver

def solve(topLeftCoords, bottomRightCoords, rows, columns, mines):
    # Look for the user pressing escape to stop the loop
    # In the loop, escapeListener.is_alive() will return false when escape has been pressed
    def on_press(key):
        if key == keyboard.Key.esc:
            return False
    escapeListener = keyboard.Listener(on_press=on_press)
    escapeListener.start()

    print(topLeftCoords, bottomRightCoords, rows, columns)
    recognizer = Recognizer(topLeftCoords, bottomRightCoords, rows, columns)
    analyzer = Analyzer(recognizer)
    solver = Solver(recognizer, analyzer, mines)
    solver.solve(shouldContinue=escapeListener.is_alive)

interface = MineSolverInterface(solve)
interface.mainloop()

# Testing setup
# def on_press(key):
#     if key == keyboard.Key.esc:
#         return False
# escapeListener = keyboard.Listener(on_press=on_press)
# escapeListener.start()
# recognizer = Recognizer((2572, 341) , (3296, 727) , 16 , 30)
# analyzer = Analyzer(recognizer)
# solver = Solver(recognizer, analyzer, 99)
# solver.solve(shouldContinue=escapeListener.is_alive)