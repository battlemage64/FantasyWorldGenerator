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
canvasimage = tkinter.PhotoImage(width=2000, height=2000)
canvas = tkinter.Canvas(master=window, width=2000, height=2000)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

seed = input("Enter a seed:\n>>>")
random.seed(seed)

map1 = wg.gen_continent(seed, 25, coast=(False, True, False, True))
map2 = wg.gen_continent(seed, 25, coast=(False, True, True, False))
map3 = wg.gen_continent(seed, 25, coast=(True, False, False, True))
map4 = wg.gen_continent(seed, 25, coast=(True, False, True, False))

res = 1
for point in map1:
    for coords in point[3]:
        canvasimage.put(decrypt_color(point[2]), (int(coords[0]/5), int(coords[1]/5)))

res = 2
for point in map2:
    for coords in point[3]:
        canvasimage.put(decrypt_color(point[2]), (int(coords[0]/5+100), int(coords[1]/5)))
res = 0
for point in map3:
    for coords in point[3]:
        canvasimage.put(decrypt_color(point[2]), (int(coords[0]/5), int(coords[1]/5+100)))
res = 1
for point in map4:
    for coords in point[3]:
        canvasimage.put(decrypt_color(point[2]), (int(coords[0]/5+100), int(coords[1]/5+100)))
