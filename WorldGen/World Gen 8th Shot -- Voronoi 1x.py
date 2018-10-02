import random
import tkinter
import math
import re
import os

# This version of the map generator uses Voronoi polygons.
# Consulted: http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

seed = input("Enter a seed.\n>>> ") # saved and put in save file
random.seed(seed)

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

for i in range(random.randint(300, 500)):
    new_point = [random.randint(0, 499), random.randint(0, 499), gen_color(), []]
    voronoi_points.append(new_point) # generates random point and an assigned color and related points list

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
            dist_to_point = math.sqrt((point[0]-i)**2+(point[1]-j)**2)
            if dist_to_point < lowest:
                lowest = dist_to_point
                target = point
        target[3].append((i, j))

for point in voronoi_points:
    # distance to center (250, 250) determines chance of color change
    dist_to_center = math.sqrt((250-point[0])**2+(250-point[1])**2)
    # decreasing as farther, chance to be land, small chance to be random lake
    if random.random() > ((dist_to_center / 354) * 1.5)**2.5:
        point[2][0] *= 0.1
        point[2][2] *= 0.1
        point[2][1] = random.randint(100, 255) # limits it to 100 minimum
    else:
        point[2][0] *= 0.1
        point[2][1] *= 0.1
        point[2][2] = random.randint(100, 255)
    for coords in point[3]:
        canvasimage.put(decrypt_color(point[2]), coords)

def save():
    while True:
        map_name = input("What would you like to name your map?\n>>>")
        file_name = re.sub("""[*."/\\\[\]:;|=,.]""", "", map_name) # removes invalid characters
        if map_name == "":
            print("Please enter a file name.")
        elif os.path.isfile("./Maps/{0}.txt".format(file_name)):
            print("That file already exists. Please choose another name or delete the current file.")
        else:
            break
    save_file = open("./Maps/"+file_name+".txt", 'w')
    save_file.write("Map name: " + map_name)
    save_file.write("\nSeed: " + seed)
    save_file.write("\n")
    save_file.write(str(voronoi_points))
    save_file.flush()
    save_file.close()
    window.title(map_name)
    print("Map {mapname} saved as {filename}.txt".format(mapname=map_name, filename=file_name))

window.after(1000, save)
window.mainloop()
