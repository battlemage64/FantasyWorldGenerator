from tkinter import *
import random

def pointOnCircle(): # generates a random point on the globe
    xtoy = random.random()
    point = (int((300 * xtoy) + 0.5), int((300 * (1/xtoy)) + 0.5))
    return point

window = Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = PhotoImage(width=300, height=300)
canvas = Canvas(master=window, height=300, width=300)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=NW)
#canvasimage.put("#000000", (i, j)) # reminder for pixel manipulation

arc = canvas.create_arc(3, 3, 297, 297, style=ARC, extent=359)

coords = pointOnCircle()
canvasimage.put("#FF0000", coords)
print(coords)
