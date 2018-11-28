import tkinter
import random
import math

random.seed(input("Enter a seed:\n>>>"))

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=500, height=500)
canvas = tkinter.Canvas(master=window, width=500, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

circlepoints = []
for x in range(-200, 200):
    y = int(math.sqrt(40000-x**2))
    circlepoints.append([x, y])

for x in range(200, -200, -1):
    y = int(math.sqrt(40000-x**2))
    circlepoints.append([x, -y])

for point in circlepoints:
    #canvasimage.put("#000000", (point[0]+250, point[1]+250))
    point[0] += random.randint(-50, 50) + 250
    point[1] += random.randint(-50, 50) + 250

canvas.create_polygon(circlepoints)
