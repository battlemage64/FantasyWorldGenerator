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

for a in range(20):
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

def callback(event):
    print("clicked at", int(event.x/20), int(event.y/20))
    print(cells[int(event.x/20)][int(event.y/20)])

window.bind("<Button-1>", callback)

for i in range(25):
    cells[i][0] = 0
    cells[0][i] = 0
    cells[i][24] = 0
    cells[24][i] = 0

outline_points = []
outline_walls = {}

lakes = []

for i in range(1, 24):
    for j in range(1, 24):
        if cells[i][j]:
            if not cells[i+1][j]: # nothing right
                canvas.create_line((i+1)*20, j*20, (i+1)*20, (j+1)*20)
                outline_walls[((i+1)*20, j*20)] = ((i+1)*20, (j+1)*20)
            if not cells[i-1][j]: # nothing left
                canvas.create_line(i*20, j*20, i*20, (j+1)*20)
                outline_walls[(i*20, (j+1)*20)] = (i*20, j*20)
            if not cells[i][j+1]: # nothing below
                canvas.create_line(i*20, (j+1)*20, (i+1)*20, (j+1)*20)
                outline_walls[((i+1)*20, (j+1)*20)] = (i*20, (j+1)*20)
            if not cells[i][j-1]: # nothing above
                canvas.create_line(i*20, j*20, (i+1)*20, j*20)
                outline_walls[(i*20, j*20)] = ((i+1)*20, j*20)

        elif cells[i+1][j] and cells[i-1][j] and cells[i][j-1] and cells[i][j+1]: # is a lake
            lakes.append((i, j))

start = next(iter(outline_walls.keys()))
endpoint = start
while True:
    outline_points.append(start)
    outline_points.append(outline_walls[start])
    start = outline_walls[start]
    if start == endpoint:
        break

grid_polygon = canvas.create_polygon(outline_points, fill='', activefill='#00FF00')

perturbed_points = []

for point in outline_points:
    perturbed_points.append((point[0] + random.randint(-10, 10), point[1] + random.randint(-10, 10)))

perturbed_polygon = canvas.create_polygon(perturbed_points, fill='#0000FF', outline='#FF0000')

for point in lakes:
    canvas.create_rectangle(point[0]*20, point[1]*20, (point[0]+1)*20, (point[1]+1)*20, fill='#000000')

canvas.tag_raise(grid_polygon)
