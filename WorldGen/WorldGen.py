import random
import tkinter

random.seed(input("Enter a seed. \n>>> "))

worldbitmap = []
for i in range(0, 1000):
   worldbitmap.append([])
   for j in range(0, 500):
       worldbitmap[i].append([])

for i in range(0, 1000):
   for j in range(0, 500):
      worldbitmap[i][j] = 0

for iteration in range(random.randint(2, 2)): # iterations of algorithm
    mode = random.sample([1, 2, 3, 4], 2) # obtains 2 #s non-repeating from 1 to 4
    if mode[0] == 1:
        point1 = (0, random.randint(0, 499)) # point is on left
    elif mode[0] == 2:
        point1 = (999, random.randint(0, 499)) # point is on right
    elif mode[0] == 3:
        point1 = (random.randint(0, 999), 999) # point is on top
    else: # here it's 4 but just in case
        point1 = (random.randint(0, 999), 0) # point is on bottom
    # then repeats for point 2 which will be on another side (different mode)
    if mode[1] == 1:
        point2 = (0, random.randint(0, 499)) # point is on left
    elif mode[1] == 2:
        point2 = (999, random.randint(0, 499)) # point is on right
    elif mode[1] == 3:
        point2 = (random.randint(0, 999), 999) # point is on top
    else: # here it's 4 but just in case
        point2 = (random.randint(0, 999), 0) # point is on bottom
    slope = (point2[1] - point1[1])/(point2[0] - point1[0]) # slope = (y2-y1)/(x2-x1)
    yint = point1[1] - (point1[0] * slope) # y-int = point y - point x times slope
    above_below = random.randint(0, 1) # true or false to go above or below
    for x in range(0, 1000):
        for y in range(0, 500):
            if y > (x * slope + yint):
                if above_below:
                    worldbitmap[x][y] += 1
                else:
                    worldbitmap[x][y] -= 1
            else:
                if not above_below:
                    worldbitmap[x][y] += 1
                else:
                    worldbitmap[x][y] -= 1

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=1000, height=500)
canvas = tkinter.Canvas(master=window, width=1000, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

for x in range(0, 999):
    for y in range(0, 499):
        if worldbitmap[x][y] > 0: # above 0
            canvasimage.put("#0000FF", (x, y)) # turn blue
        elif worldbitmap[x][y] < 0:
            canvasimage.put("#FF0000", (x, y)) # turn red
        else: # equal to 0
            canvasimage.put("#FFFF00", (x, y)) # turn yellow
            
