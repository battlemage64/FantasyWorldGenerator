import random
import tkinter
import math
import re
import os
import math

# For normal use or importing

# This version of the map generator uses Voronoi polygons.
# Consulted: http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

if __name__ == "__main__":
    seed = input("Enter a seed.\n>>> ") # saved and put in save file
    random.seed(seed)


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

def gen_continent(seed, resolution=9, center=(250, 250)): # valid resolutions: 1, 9, 25
    """Generates a continent or piece for use in a larger map.
Seed=user-given seed; center=set center for continent;
Coast=4 numbers 1-250 (higher is recommended) for top, bottom, left, right coast"""
    voronoi_points = [] # list of tuples (x, y, color): random points to draw polygons around

    #center = (random.randint(100, 399), random.randint(100, 399))

    rad_x = random.randint(10, 200) # radii in x/y directions for ellipse
    rad_y = random.randint(10, 200)
    rotation = random.randint(0, 359) # unused for now

    for i in range(random.randint(300, 500)):
        new_point = [random.randint(0, 499), random.randint(0, 499), gen_color(), [], "tile"]
        voronoi_points.append(new_point) # generates random point and an assigned color and related points list

    for i in range(0, 499, int(math.sqrt(resolution))):
        for j in range(0, 499, int(math.sqrt(resolution))):
            lowest = 999
            for point in voronoi_points:
                dist_to_point = math.sqrt((point[0]-i)**2+(point[1]-j)**2)
                if dist_to_point < lowest:
                    lowest = dist_to_point
                    target = point
            target[3].append((i, j))

    if __name__ == "__main__":
        window = tkinter.Tk()
        window.title("Your Finished Map")
        window.wm_attributes("-topmost", 1)
        window.resizable(False, False)
        canvasimage = tkinter.PhotoImage(width=500, height=500)
        canvas = tkinter.Canvas(master=window, width=500, height=500)
        canvas.pack()
        canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

    for point in voronoi_points:
        # distance from ellipse perimeter determines chance of color change
        chance_of_land = ((point[0]-center[0])**2/rad_x**2)+((point[1]-center[1])**2/rad_y**2)
        # decreasing as farther, chance to be land, small chance to be random lake
        if random.random() > chance_of_land:
            point[2][0] *= 0.1
            point[2][2] *= 0.1
            point[2][1] = random.randint(100, 255) # limits it to 100 minimum
            point[4] = "land"
        else:
            point[2][0] *= 0.1
            point[2][1] *= 0.1
            point[2][2] = random.randint(100, 255)
            point[4] = "water"
        if __name__ == "__main__":
            for coords in point[3]:
                #canvasimage.put(decrypt_color(point[2]), coords)
                canvas.create_rectangle(coords[0]-1, coords[1]-1, coords[0]+1, coords[1]+1, fill=decrypt_color(point[2]), outline=decrypt_color(point[2]))

    def save():
        while True:
            map_name = input("What would you like to name your map?\n>>>")
            file_name = re.sub("""[*."/\\\[\]:;|=,.]""", "", map_name) # removes invalid characters
            if map_name == "":
                print("Please enter a file name.")
            elif os.path.isfile("./Maps/{0}.fwgmap".format(file_name)):
                print("That file already exists. Please choose another name or delete the current file.")
            else:
                break
        save_file = open("./Maps/"+file_name+".fwgmap", 'w')
        save_file.write("Map name: " + map_name)
        save_file.write("\nSeed: " + seed)
        save_file.write("\nVersion: 1.0")
        save_file.write("\nResolution: 9x")
        save_file.write("\n")
        save_file.write(str(voronoi_points))
        save_file.flush()
        save_file.close()
        window.title(map_name)
        print("Map {mapname} saved as {filename}.fwgmap".format(mapname=map_name, filename=file_name))

    if __name__ == "__main__":
        window.after(1000, save)
        window.mainloop()
    else:
        return voronoi_points

if __name__ == "__main__":
    gen_continent(seed)
