import random
import tkinter
import math
import numpy as np

# Generates a continent from a grid using an algorithm based on that of
# David Stark, developer of Airships: Conquer the Skies. Thanks a lot!

# Intended to be used multiple times by WorldBuilder.py to make and combine a continent

class NoConnectionError(Exception):
    pass

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title("Your Finished Map")
    window.wm_attributes("-topmost", 1)
    window.resizable(False, False)
    canvas = tkinter.Canvas(master=window, width=1000, height=1000, bg='#0000FF')
    canvas.pack()

def chaikins_corner_cutting(coords, refinements=10):
    # code from https://stackoverflow.com/questions/47068504/where-to-find-python-implementation-of-chaikins-corner-cutting-algorithm/47072438
    coords = np.array(coords)

    for _ in range(refinements):
        L = coords.repeat(2, axis=0)
        R = np.empty_like(L)
        R[0] = L[0]
        R[2::2] = L[1:-1:2]
        R[1:-1:2] = L[2::2]
        R[-1] = L[-1]
        coords = L * 0.75 + R * 0.25

    return coords

def create_landtile(draw=True, lake=False, parent=None, offset=20, seed=None, trend=random.randint(1, 8)):
    if not seed:
        random.seed()
    else:
        random.seed(seed)
    cells = []
    for i in range(50):
        cells.append([])
        for j in range(50):
            cells[i].append(0)

    if not lake:
        cells[random.randint(20, 30)][random.randint(20, 30)] = 1
    else:
        point = (-1, -1)
        while not parent[0][point[0]][point[1]]:
            point = (random.randint(0, 49), random.randint(0, 49))
        cells[point[0]][point[1]] = 1

    if lake:
        growth = random.randint(0, 6)
    else:
        growth = 30
    
    for a in range(growth):
        for i in range(2, 49):
            for j in range(2, 49):
                if cells[i][j] == 1 and random.randint(1, 3) != 1:
                    way = random.randint(1, 5)
                    if random.randint(1, 3) == 1: # 1 in 3 chance to follow trend
                        way = trend
                        if trend == 5:
                            way = random.choice([1, 3])
                        elif trend == 6:
                            way = random.choice([1, 4])
                        elif trend == 7:
                            way = random.choice([2, 3])
                        elif trend == 8:
                            way = random.choice([2, 4])
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

    for x in range(50): # this block should detect water cells surrounded by land
        for y in range(50): # and assimilate them
            if cells[x][y] == 0: # so the border-finder works
                hitswall = [True, True, True, True]
                for i in range(x, 50):
                    if cells[i][y]:
                        hitswall[0] = False
                for i in range(x, 0, -1):
                    if cells[i][y]:
                        hitswall[1] = False
                for j in range(y, 50):
                    if cells[x][j]:
                        hitswall[2] = False
                for j in range(y, 0, -1):
                    if cells[x][j]:
                        hitswall[3] = False
                if not hitswall[0] and not hitswall[1] and not hitswall[2] and not hitswall[3]:
                    cells[x][y] = 1

##    def callback(event):
##        print("clicked at", int(event.x/20), int(event.y/20))
##        print(cells[int(event.x/20)][int(event.y/20)])
##
##    window.bind("<Button-1>", callback)

    for i in range(50):
        cells[i][0] = 0
        cells[0][i] = 0
        cells[i][49] = 0
        cells[49][i] = 0

    outline_points = []
    outline_walls = {}

    for i in range(1, 50):
        for j in range(1, 50):
            if cells[i][j]:
                if not cells[i+1][j]: # nothing right
                    if draw:
                        canvas.create_line((i+1)*offset, j*offset, (i+1)*offset, (j+1)*offset)
                    outline_walls[((i+1)*offset, j*offset)] = ((i+1)*offset, (j+1)*offset)
                if not cells[i-1][j]: # nothing left
                    if draw:
                        canvas.create_line(i*offset, j*offset, i*offset, (j+1)*offset)
                    outline_walls[(i*offset, (j+1)*offset)] = (i*offset, j*offset)
                if not cells[i][j+1]: # nothing below
                    if draw:
                        canvas.create_line(i*offset, (j+1)*offset, (i+1)*offset, (j+1)*offset)
                    outline_walls[((i+1)*offset, (j+1)*offset)] = (i*offset, (j+1)*offset)
                if not cells[i][j-1]: # nothing above
                    if draw:
                        canvas.create_line(i*offset, j*offset, (i+1)*offset, j*offset)
                    outline_walls[(i*offset, j*offset)] = ((i+1)*offset, j*offset)

    start = next(iter(outline_walls.keys()))
    endpoint = start
    for i in range(500): # escape condition just in case
        outline_points.append(start)
        outline_points.append(outline_walls[start])
        start = outline_walls[start]
        if start == endpoint:
            break
##        if i == 499:
##            print(outline_walls)
##            raise NoConnectionError('No connection')

    if draw:
        grid_polygon = canvas.create_polygon(outline_points, fill='', activefill='#00FF00')

    perturbed_points = []

    variation = random.randint(5, 15)

    for point in outline_points:
        perturbed_points.append((point[0] + random.randint(-variation, variation), point[1] + random.randint(-variation, variation)))

    smoothed_points = chaikins_corner_cutting(perturbed_points).tolist()
    

##    for point in perturbed_points:
##        totalx = 0
##        totaly = 0
##        totalweight = 0
##        for avgpt in perturbed_points:
##            dist = math.sqrt((point[0] - avgpt[0])**2 + (point[1] - avgpt[1])**2)
##            weight = 20 / (dist * dist + 20)
##            totalx += avgpt[0] * weight
##            totaly += avgpt[1] * weight
##            totalweight += weight
##        #totalx /= len(perturbed_points)
##        #totaly /= len(perturbed_points)
##        totalx /= totalweight
##        totaly /= totalweight
##        smoothed_points.append((int(totalx), int(totaly)))
##        #smoothed_points.append((int(totalx/len(perturbed_points))*20,int(totaly/len(perturbed_points))*20))

    if draw:
        perturbed_polygon = canvas.create_polygon(perturbed_points, fill='', outline='#FF0000')
        canvas.tag_raise(grid_polygon)
        smoothed_polygon = canvas.create_polygon(smoothed_points, fill='', outline='#FFFFFF')

    if not draw:
        return [cells, outline_points, perturbed_points, smoothed_points, "", (), 0] # last items will become biome, position, tag later

if __name__ == '__main__':
    cont = create_landtile(False)
    grid_polygon = canvas.create_polygon(cont[1], fill='', activefill='#00FF00')
    perturbed_polygon = canvas.create_polygon(cont[2], fill='#00FF00', outline='#FF0000')
    smoothed_polygon = canvas.create_polygon(cont[3], fill='', outline='#FFFFFF')
    cont[6] = perturbed_polygon
    
    for i in range(random.randint(1, 4)):
        lake = create_landtile(False, True, cont)
        grid_polygon2 = canvas.create_polygon(lake[1], fill='', activefill='#0000FF')
        perturbed_polygon2 = canvas.create_polygon(lake[2], fill='#0000FF', outline='#FF00FF')
        canvas.tag_raise(grid_polygon2)
    canvas.tag_raise(grid_polygon)
    canvas.tag_raise(smoothed_polygon)
    
##for i in range(random.randint(1, 3)):
##    lake_points = []
##    offset_x = random.randint(-100, 100)
##    offset_y = random.randint(-100, 100)
##    for i in range(random.randint(3, 10)):
##        lake_points.append((average_pos[0] + random.randint(-5, 5) + offset_x, average_pos[1] + random.randint(-5, 5) + offset_y))
##    canvas.create_polygon(lake_points, fill="#0000FF")
