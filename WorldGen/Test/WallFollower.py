import random
import tkinter
import math

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=500, height=500)
canvas = tkinter.Canvas(master=window, width=500, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

cells = []
for i in range(25):
    cells.append([])
    for j in range(25):
        cells[i].append(0)

cells[random.randint(1, 23)][random.randint(1, 23)] = 1

for a in range(10):
   for i in range(2, 24):
      for j in range(2, 24):
         if cells[i][j] == 1 and random.randint(1, 3) != 1:
            way = random.randint(1, 4)
            if way == 1 and cells[i][j+1] == 0:
               cells[i][j+1] = 2
            if way == 2 and cells[i][j-1] == 0:
               cells[i][j-1] = 2
            if way == 3 and cells[i-1][j] == 0:
               cells[i-1][j] = 2
            if way == 4 and cells[i+1][j] == 0:
               cells[i+1][j] = 2
   for i in range(0, 25):
      for j in range(0, 25):
         if cells[i][j] == 2:
            cells[i][j] = 1

outline_points = []
outline_walls = {}

for i in range(2, 24):
    for j in range(2, 24):
        if cells[i][j]:
            if not cells[i+1][j]: # nothing below
                canvas.create_line((i+1)*20, j*20, (i+1)*20, (j+1)*20)
                outline_walls[((i+1)*20, j*20)] = ((i+1)*20, (j+1)*20)
            if not cells[i-1][j]: # nothing above
                canvas.create_line(i*20, j*20, i*20, (j+1)*20)
                outline_walls[(i*20, j*20)] = (i*20, (j+1)*20)
            if not cells[i][j+1]: # nothing right
                canvas.create_line(i*20, (j+1)*20, (i+1)*20, (j+1)*20)
                outline_walls[(i*20, (j+1)*20)] = ((i+1)*20, (j+1)*20)
            if not cells[i][j-1]: # nothing left
                canvas.create_line(i*20, j*20, (i+1)*20, j*20)
                outline_walls[(i*20, j*20)] = ((i+1)*20, j*20)
                
##            if not cells[i+1][j] or not cells[i][j+1]:
##                outline_points.append(((i+1)*20, (j+1)*20))
##            if not cells[i-1][j] or not cells[i][j+1]:
##                outline_points.append((i*20, (j+1)*20))
##            if not cells[i-1][j] or not cells[i][j-1]:
##                outline_points.append((i*20, j*20))
##            if not cells[i+1][j] or not cells[i][j-1]:
##                outline_points.append(((i+1)*20, j*20))

start = next(iter(outline_walls.keys()))
endpoint = start
while True:
    outline_points.append(start)
    outline_points.append(outline_walls[start])
    start = outline_walls[start]
    if start == endpoint:
        break

canvas.create_polygon(outline_points, fill='')
    

#canvas.create_polygon(outline_points)
