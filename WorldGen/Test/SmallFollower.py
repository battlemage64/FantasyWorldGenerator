import random
import tkinter
import math

class NoConnectionError(Exception):
    pass

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvas = tkinter.Canvas(master=window, width=1000, height=1000)
canvas.pack()

def create_continent(draw=True, lake=False, parent=None):
    cells = []
    for i in range(50):
        cells.append([])
        for j in range(50):
            cells[i].append(0)

    if not lake:
        cells[random.randint(20, 30)][random.randint(20, 30)] = 1
    else:
        # TODO: pick random point on parent to start

    if lake:
        growth = 5
    else:
        growth = 30
    for a in range(growth):
       for i in range(2, 49):
          for j in range(2, 49):
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
       for i in range(0, 50):
          for j in range(0, 50):
             if cells[i][j] == 2:
                cells[i][j] = 1

    def callback(event):
        print("clicked at", int(event.x/20), int(event.y/20))
        print(cells[int(event.x/20)][int(event.y/20)])

    window.bind("<Button-1>", callback)

    for i in range(50):
        cells[i][0] = 0
        cells[0][i] = 0
        cells[i][49] = 0
        cells[49][i] = 0

    outline_points = []
    outline_walls = {}

    for i in range(1, 49):
        for j in range(1, 49):
            if cells[i][j]:
                if not cells[i+1][j]: # nothing right
                    if draw:
                        canvas.create_line((i+1)*20, j*20, (i+1)*20, (j+1)*20)
                    outline_walls[((i+1)*20, j*20)] = ((i+1)*20, (j+1)*20)
                if not cells[i-1][j]: # nothing left
                    if draw:
                        canvas.create_line(i*20, j*20, i*20, (j+1)*20)
                    outline_walls[(i*20, (j+1)*20)] = (i*20, j*20)
                if not cells[i][j+1]: # nothing below
                    if draw:
                        canvas.create_line(i*20, (j+1)*20, (i+1)*20, (j+1)*20)
                    outline_walls[((i+1)*20, (j+1)*20)] = (i*20, (j+1)*20)
                if not cells[i][j-1]: # nothing above
                    if draw:
                        canvas.create_line(i*20, j*20, (i+1)*20, j*20)
                    outline_walls[(i*20, j*20)] = ((i+1)*20, j*20)

    start = next(iter(outline_walls.keys()))
    endpoint = start
    for i in range(2000): # escape condition just in case
        outline_points.append(start)
        outline_points.append(outline_walls[start])
        start = outline_walls[start]
        if start == endpoint:
            break
        if i == 2000:
            raise NoConnectionError("maximum recursion reached")

    if draw:
        grid_polygon = canvas.create_polygon(outline_points, fill='', activefill='#00FF00')

    perturbed_points = []

    for point in outline_points:
        perturbed_points.append((point[0] + random.randint(-10, 10), point[1] + random.randint(-10, 10)))

    if draw:
        perturbed_polygon = canvas.create_polygon(perturbed_points, fill='', outline='#FF0000')
        canvas.tag_raise(grid_polygon)

    average_pos = [0, 0]
    for point in outline_points:
        average_pos[0] += point[0]
        average_pos[1] += point[1]
    average_pos[0] /= len(outline_points)
    average_pos[1] /= len(outline_points)

    if not draw:
        return (cells, outline_points, perturbed_points, average_pos)

if __name__ == '__main__':
    cont = create_continent(False)
    grid_polygon = canvas.create_polygon(cont[1], fill='', activefill='#00FF00')
    perturbed_polygon = canvas.create_polygon(cont[2], fill='', outline='#FF0000')
    canvas.tag_raise(grid_polygon)
    
    lake = create_continent(False, True, cont)
    grid_polygon2 = canvas.create_polygon(lake[1], fill='', activefill='#0000FF')
    perturbed_polygon2 = canvas.create_polygon(lake[2], fill='#0000FF', outline='#FF00FF')
    canvas.tag_raise(grid_polygon2)
    
##for i in range(random.randint(1, 3)):
##    lake_points = []
##    offset_x = random.randint(-100, 100)
##    offset_y = random.randint(-100, 100)
##    for i in range(random.randint(3, 10)):
##        lake_points.append((average_pos[0] + random.randint(-5, 5) + offset_x, average_pos[1] + random.randint(-5, 5) + offset_y))
##    canvas.create_polygon(lake_points, fill="#0000FF")
