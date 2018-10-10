from tkinter import *
import random

class Continent:
    def __init__(self, movability, growability, x, y):
        self.movability = movability
        self.growability = growability
        self.cells = [(x, y)]
        

con = Continent(1, 10, 250, 150)

window = Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = PhotoImage(width=500, height=300)
canvas = Canvas(master=window, height=300, width=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=NW)
#canvasimage.put("#000000", (i, j)) # reminder for pixel manipulation

for coords in con.cells:
    canvasimage.put("#000000", (coords[0], coords[1]))
