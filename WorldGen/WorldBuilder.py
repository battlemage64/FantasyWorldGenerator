import random
import tkinter

import InteractableContinentGenerator as cg
import IslandGenerator as ig
import IslandStretchedGenerator as isg

random.seed(input("Enter a world seed:\n>>> "))

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvas = tkinter.Canvas(master=window, width=1000, height=1000, bg='#0000FF')
canvasimage = tkinter.PhotoImage(width=1000, height=1000)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

relevant_points = [] # possible start points for rivers

for i in range(random.randint(20, 50)):
    positionx = random.randint(0, 600)
    positiony = random.randint(0, 600)
    cont = cg.create_continent(False, offset=10, seed=random.random())
    perturbed_polygon = canvas.create_polygon(cont[2], fill='#00FF00', outline='')
    canvas.move(perturbed_polygon, positionx, positiony)

    for k in range(random.randint(1, 4)):
        lake = cg.create_continent(False, True, cont, offset=10, seed=random.random())
        perturbed_polygon2 = canvas.create_polygon(lake[2], fill='#0000FF', outline='')
        canvas.move(perturbed_polygon2, positionx, positiony)
        for i in range(random.randint(1, 4)):
            relevant_points.append(random.choice(lake[2]))

for i in range(random.randint(20, 30)): # draw river
    width = random.randint(1, 3) # usd later, possibly changed before used
    # Algorithm: choose 2 pts, draw line, perturb line
    mode = random.randint(1, 5) # obtains 2 #s non-repeating from 1 to 4
    point1 = (random.randint(0, 999), random.randint(0, 999))
    if mode == 1:
        point2 = (0, random.randint(0, 499)) # point is on left
    elif mode == 2:
        point2 = (999, random.randint(0, 499)) # point is on right
    elif mode == 3:
        point2 = (random.randint(0, 999), 999) # point is on top
    elif mode == 4: # here it's 4 but just in case
        point2 = (random.randint(0, 999), 0) # point is on bottom
    elif relevant_points != []:
        point2 = random.choice(relevant_points)
        width -= 1 # limits width (pre-declared) to 1 or 2
    else:
        point2 = (random.randint(0, 999), random.randint(0, 999))
    slope = (point2[1] - point1[1])/(point2[0] - point1[0]) # slope = (y2-y1)/(x2-x1)
    yint = point1[1] - (point1[0] * slope) # y-int = point y - point x times slope

    river_points = [point1]
    detail = 100
    for i in range(detail):
        x = river_points[-1][0]
        y = river_points[-1][1]
        x += (point2[0] - point1[0])/detail
        y += slope * ((point2[0] - point1[0])/detail)
        river_points.append((x + random.randint(-10, 10), y + random.randint(-10, 10)))
    river_points.append(point2)
    for i in range(random.randint(0, 5)):
        relevant_points.append(random.choice(river_points))
    canvas.create_line(river_points, fill="#0000FF", width=width)
