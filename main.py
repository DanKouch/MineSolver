#!/usr/bin/python

from pynput import keyboard

from interface import MineSolverInterface
from recognizer import Recognizer
from solver import Solver

# def solve(topLeftCoords, bottomRightCoords, rows, columns, mines):
#     # Look for the user pressing escape to stop the loop
#     # In the loop, escapeListener.is_alive() will return false when escape has been pressed
#     def on_press(key):
#         if key == keyboard.Key.esc:
#             return False
#     escapeListener = keyboard.Listener(on_press=on_press)
#     escapeListener.start()

#     recognizer = Recognizer(topLeftCoords, bottomRightCoords, rows, columns)
#     solver = Solver(recognizer, mines, shouldContinue=escapeListener.is_alive)

#     solver.solve()

#     print("Solve thread ended.")

# interface = MineSolverInterface(solve)
# interface.mainloop()

def on_press(key):
    if key == keyboard.Key.esc:
        return False
escapeListener = keyboard.Listener(on_press=on_press)
escapeListener.start()

# Works specifically on 30x16 games with 99 mines on 150% zoom where https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mines.html#9x9n10#975656693524649 is on the right half of the screen
recognizer = Recognizer((1460, 369), (2363, 852), 16, 30)
solver = Solver(recognizer, 99)
solver.solve(shouldContinue=escapeListener.is_alive)

# Works specifically on out 3 when the image is manually inputed in recognizer.py
# print(recognizer.getUpdatedGrid())
#recognizer = Recognizer((0, 0), (547, 548), 9, 9)
