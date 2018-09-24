import random
import tkinter
import math

# This version of the map generator uses Voronoi polygons.
# Consulted: http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

random.seed(input("Enter a seed. \n>>> "))

voronoi_points = [] # list of tuples (x, y, color): random points to draw polygons around

def gen_color(): # generates a list of hex values to be turned into a color later with decrypt_color()
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

def decrypt_color(data): # where data is a list of (r, g, b)
    color = "#"
    for num in data:
        if num > 255:
            num = 255
        if num < 0:
            num = 0
        if num < 16: # single digit of hex
            color += "0" # add the zero
        color += hex(int(num))[2:] # removes the "0x"
    return color

for i in range(random.randint(50, 100)):
    new_point = [random.randint(0, 499), random.randint(0, 499), gen_color(), []]
##    if new_point[0] in range(0, 70) or new_point[0] in range(430, 500) or new_point[1] in range(0, 70) or new_point[1] in range(430, 500):
##        new_point[2][0] *= 0.2
##        new_point[2][1] *= 0.2
##    if new_point[0] in range(70, 100) or new_point[0] in range(400, 430) or new_point[1] in range(70, 100) or new_point[1] in range(400, 430):
##        new_point[2][1] *= 0.5
##        new_point[2][2] *= 0.8
##    if new_point[0] in range(101, 431) and new_point[1] in range(101, 431):
##        new_point[2][0] *= 0.2
##        new_point[2][2] *= 0.2
##        if new_point[0] in range(100, 400) and new_point[1] in range(100, 400) and random.randint(1, 10) == 1:
##            new_point[2][0] *= 10
    voronoi_points.append(new_point) # generates random point and an assigned color and related points list

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=500, height=500)
canvas = tkinter.Canvas(master=window, width=500, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

##for i in range(0, 499):
##    for j in range(0, 499):
##        lowest = 999
##        for point in voronoi_points:
##            # The distance from the pixel to each point is calculated,
##            # and then the pixel is turned the color of the closest
##            # point. The formula below is to find shortest distance
##            # between points: sqrt((x2-x1)^2+(y2-y1)^2)
##            dist_to_point = math.sqrt((point[0]-i)**2+(point[1]-j)**2)
##            if dist_to_point < lowest:
##                lowest = dist_to_point
##                colorSelected = point[2]
##        canvasimage.put(decrypt_color(colorSelected), (i, j))

for i in range(0, 499):
    for j in range(0, 499):
        lowest = 999
        for point in voronoi_points:
            dist_to_point = math.sqrt((point[0]-i)**2+(point[1]-j)**2)
            if dist_to_point < lowest:
                lowest = dist_to_point
                target = point
        target[3].append((i, j))

for point in voronoi_points:
    for coords in point[3]:
        canvasimage.put(decrypt_color(point[2]), coords)

