import tkinter as tk
from pynput import mouse
from threading import Thread

class MineSolverInterface(tk.Frame, object):
    def __init__(self, solveCallback):
        self.solveCallback = solveCallback
        self.solving = False
        self.master = tk.Tk()
        super(MineSolverInterface, self).__init__(master=self.master)
        self.master.title("MineSolver")
        self.master.resizable(False, False)
        self.master.iconbitmap(bitmap="favicon.ico")
        
        self.grid()

        self.explainatoryText = tk.Label(master=self, padx=10, pady=10, justify="center", wraplength=200,text="""\
            This utility is designed to automatically solve the Minesweeper game "Mines" from Simon Tatham's Portable Puzzle Collection.
            \nTo get started, press the "Select Bounds" button to tell the program where to look for the game board. Then, enter the number of rows, columns, and mines and hit solve when you are ready.
        """)
        self.explainatoryText.grid(row=0, column=0)

        self.settingsFrame = tk.LabelFrame(master=self, text="Settings", padx=10)
        self.settingsFrame.grid(row=0, column=1, padx=10, pady=10)

        self.select_bounds_button = tk.Button(master=self.settingsFrame, command=self.selectBoundsAction, text="Select Bounds")
        self.select_bounds_button.grid(row=1, column=0, columnspan=2)

        # self.upper_left_coordinate = tk.Text(height=1)
        # self.upper_left_coordinate.insert("insert", "Upper-left corner")
        # self.upper_left_coordinate.config(state="disabled")
        # 


        self.bound_select_exp = tk.Label(master=self.settingsFrame, height=1, wraplength=200)
        self.bound_select_exp.grid(row=0, column=0, columnspan=2)

        tk.Label(master=self.settingsFrame, text="Upper-left corner:", justify="right").grid(row=2, column=0)
        self.upper_left_coordinate = tk.Label(master=self.settingsFrame, justify="left", text="(?, ?)")
        self.upper_left_coordinate.grid(row=2, column=1)

        tk.Label(master=self.settingsFrame, text="Lower-right corner:", justify="right").grid(row=3, column=0)
        self.lower_right_coordinate = tk.Label(master=self.settingsFrame, justify="left", text="(?, ?)")
        self.lower_right_coordinate.grid(row=3, column=1)

        tk.Label(master=self.settingsFrame, text="Rows:", anchor="e").grid(row=4, column=0)
        self.rows_entry = tk.Entry(master=self.settingsFrame, width=6)
        self.rows_entry.grid(row=4, column=1)

        tk.Label(master=self.settingsFrame, text="Columns:", anchor="e").grid(row=5, column=0)
        self.columns_entry = tk.Entry(master=self.settingsFrame, width=6)
        self.columns_entry.grid(row=5, column=1)

        tk.Label(master=self.settingsFrame, text="Mines:", anchor="e").grid(row=6, column=0)
        self.mines_entry = tk.Entry(master=self.settingsFrame, width=6)
        self.mines_entry.grid(row=6, column=1)

        self.solveButton = tk.Button(master=self, command=self.solve, text="Solve", width=50)
        self.solveButton.grid(row=1, column=0, columnspan=2)

        self.bottomText = tk.Label(master=self)
        self.bottomText.grid(row=2, column=0, columnspan=2)

        self.upperLeft = (-1, -1)
        self.lowerRight = (-1, -1)

        self.master.after(10, self.checkCanSolve)

    def selectBoundsAction(self):
        self.upperLeft = self.lowerRight = (-1, -1)

        self.upper_left_coordinate.config(text="(?, ?)")
        self.lower_right_coordinate.config(text="(?, ?)")

        self.select_bounds_button.config(state="disabled")

        self.bound_select_exp.config(text="Click the upper-left corner")

        def on_click(x, y, button, pressed):
            if pressed: return True
            if self.upperLeft == (-1, -1):
                self.upperLeft = (x, y)
                self.upper_left_coordinate.config(text="(" + str(self.upperLeft[0]) + ", " + str(self.upperLeft[1]) + ")")
                self.bound_select_exp.config(text="Now click the lower-right corner")
            elif self.lowerRight == (-1, -1):
                self.lowerRight = (x, y)
                self.lower_right_coordinate.config(text="(" + str(self.lowerRight[0]) + ", " + str(self.lowerRight[1]) + ")")
                self.select_bounds_button.config(state="normal")
                self.bound_select_exp.config(text="")
                return False
        listener = mouse.Listener(on_click=on_click)
        listener.start()

    def checkCanSolve(self):
        canSolve = True
        try:
            self.rows = int(self.rows_entry.get())
        except ValueError:
            canSolve = False
        try:
            self.columns = int(self.columns_entry.get())
        except ValueError:
            canSolve = False
        try:
            self.mines = int(self.mines_entry.get())
        except ValueError:
            canSolve = False

        if self.upperLeft == (-1, -1) or self.lowerRight == (-1, -1):
            canSolve = False

        self.solveButton.config(state=("normal" if (canSolve and not self.solving) else "disabled"))
        self.master.after(10, self.checkCanSolve)

    def checkIfDone(self):
        if not self.solveThread.isAlive():
            # Exit
            self.master.destroy()
        self.master.after(100, self.checkIfDone)

    def solve(self):
        self.solving = True

        for widget in self.settingsFrame.winfo_children():
            widget.config(state="disabled")
        self.solveButton.config(state="disabled") 
        self.bottomText.config(text="Press escape to stop solving...")
        #self.solveCallback(self.upperLeft, self.lowerRight, self.rows, self.columns, self.mines)
        self.solveThread = Thread(target=self.solveCallback, args=(self.upperLeft, self.lowerRight, self.rows, self.columns, self.mines))
        self.solveThread.start()
        self.master.after(100, self.checkIfDone)
