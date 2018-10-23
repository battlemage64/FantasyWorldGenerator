import tkinter
import ContinentPiecewiseGenerator as wg
import random

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

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=500, height=500)
canvas = tkinter.Canvas(master=window, width=500, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

seed = input("Enter a seed:\n>>>")
random.seed(seed)

# 20x20 grid of maps
mapdata = [[[] for j in range(5)] for i in range(5)]

next_to_process = [(2, 2)]

def gen_cont(x, y):
    "x and y are from 0 to 19. Starting point to generate a continent."
    if x < 0 or x > 4 or y < 0 or y > 4:
        return

    connections = [False, False, False, False] # top, bottom, left, right

    if y > 0 and "bottom" in mapdata[x][y-1]:
        connections[0] = True
    if y < 4 and "top" in mapdata[x][y+1]:
        connections[1] = True
    if x > 0 and "right" in mapdata[x-1][y]:
        connections[2] = True
    if x < 4 and "left" in mapdata[x+1][y]:
        connections[3] = True

    loop = True
    while loop:
        choice = random.randint(-5, 15)
        if choice in range(-5, 2):
            land_shape = [True, True, True, True]
            loop = False
        elif choice == 2 and connections[0] and (not connections[1] and not connections[2] and not connections[3]):
            land_shape = [True, False, False, False]
            loop = False
        elif choice == 3 and connections[1] and (not connections[0] and not connections[2] and not connections[3]):
            land_shape = [False, True, False, False]
            loop = False
        elif choice == 4 and connections[2] and (not connections[1] and not connections[0] and not connections[3]):
            land_shape = [False, False, True, False]
            loop = False
        elif choice == 5 and connections[3] and (not connections[1] and not connections[2] and not connections[0]):
            land_shape = [False, False, False, True]
            loop = False
        elif choice == 6 and (connections[0] or connections[2]) and (not connections[1] and not connections[3]):
            land_shape = [True, False, True, False]
            loop = False
        elif choice == 7 and (connections[0] or connections[3]) and (not connections[1] and not connections[2]):
            land_shape = [True, False, False, True]
            loop = False
        elif choice == 8 and (connections[1] or connections[2]) and (not connections[0] and not connections[3]):
            land_shape = [False, True, True, False]
            loop = False
        elif choice == 9 and (connections[1] or connections[3]) and (not connections[0] and not connections[2]):
            land_shape = [False, True, False, True]
            loop = False
        elif choice == 10 and (connections[0] or connections[1]) and (not connections[2] and not connections[3]):
            land_shape = [True, True, False, False]
            loop = False
        elif choice == 11 and (connections[2] or connections[3]) and (not connections[0] and not connections[1]):
            land_shape = [False, False, True, True]
            loop = False
        elif choice == 12 and (connections[0] or connections[1] or connections[2]) and not connections[3]:
            land_shape = [True, True, True, False]
            loop = False
        elif choice == 13 and (connections[0] or connections[1] or connections[3]) and not connections[2]:
            land_shape = [True, True, False, True]
            loop = False
        elif choice == 14 and (connections[1] or connections[2] or connections[3]) and not connections[0]:
            land_shape = [False, True, True, True]
            loop = False
        elif choice == 15 and (connections[0] or connections[2] or connections[3]) and not connections[1]:
            land_shape = [True, False, True, True]
            loop = False
    tile_connections = ""
    if land_shape[0]:
        tile_connections += "top"
    if land_shape[1]:
        tile_connections += "bottom"
    if land_shape[2]:
        tile_connections += "left"
    if land_shape[3]:
        tile_connections += "right"
    mapdata[x][y] = tile_connections

    tile_map = wg.gen_continent(seed, 25, coast=land_shape)

    for point in tile_map:
        for coords in point[3]:
            canvasimage.put(decrypt_color(point[2]), (int(coords[0]/5+100*x), int(coords[1]/5+100*y)))

    global next_to_process
    if y > 0 and land_shape[0] and not mapdata[x][y-1]:
        next_to_process.append((x, y-1))
    if y < 4 and land_shape[1] and not mapdata[x][y+1]:
        next_to_process.append((x, y+1))
    if x > 0 and land_shape[2] and not mapdata[x-1][y]:
        next_to_process.append((x-1, y))
    if x < 4 and land_shape[3] and not mapdata[x+1][y]:
        next_to_process.append((x+1, y))

while next_to_process:
    gen_cont(next_to_process[0][0], next_to_process[0][1])
    del next_to_process[0]

##for i in range(0, 50):
##    for j in range(0, 50):
##        print("{0} {1}".format(i, j))
##        print(mapdata[i][j])
