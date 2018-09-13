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
    voronoi_points.append((random.randint(0, 499), random.randint(0, 499), gen_color())) # generates random point and an assigned color

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=500, height=500)
canvas = tkinter.Canvas(master=window, width=500, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

for i in range(0, 499):
    for j in range(0, 499):
        lowest = 999
        for point in voronoi_points:
            # The distance from the pixel to each point is calculated,
            # and then the pixel is turned the color of the closest
            # point. The formula below is to find shortest distance
            # between points: sqrt((x2-x1)^2+(y2-y1)^2)
            dist_to_point = math.sqrt((point[0]-i)**2+(point[1]-j)**2)
            if dist_to_point < lowest:
                lowest = dist_to_point
                colorSelected = point[2]
##        if i in range(0, 100) or i in range(401, 500):
##            colorSelected[0] *= 0.5
##        if j in range(0, 100) or j in range(401, 500):
##            colorSelected[0] *= 0.5

        # Weighting function: red amount *= 650/650 times distance from center (max ~636)
        #colorSelected[0] *= 100/(650 - math.sqrt((point[0]-450)**2+(point[1]-450)**2)) # Finds the distance from center and weights red in color based on distance
        canvasimage.put(decrypt_color(colorSelected), (i, j))
