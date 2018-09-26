import tkinter
import os

# following code from https://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir
if os.name == 'nt':
    import win32api, win32con


def ishidden(p):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return p.startswith('.') #linux-osx
# end copied code

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

saves_found = os.listdir("./Maps")
print("Found saves:")
for item in saves_found:
    if ishidden(item):
        continue
    file = open("./Maps/"+item, 'r')
    contents = file.readlines()
    map_name = contents[0].replace("Map name: ", "") # could just slice it off but this is more legible
    print("Map {mapname} file {filename}".format(mapname=map_name, filename=item))
    file.close()

while True:
    filename = input("Open which file?\n>>>")
    if not filename in saves_found or ishidden(filename): # ishidden just in case
        print("Invalid file name")
    else:
        break

SAVE_FILE = open("./Maps/"+filename, 'r')
CONTENTS = SAVE_FILE.readlines()
SAVE_FILE.close()

MAP_NAME = CONTENTS[0].replace("Map name: ", "")
DATA = eval(CONTENTS[2])

window = tkinter.Tk()
window.title(MAP_NAME)
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=500, height=500)
canvas = tkinter.Canvas(master=window, width=500, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

for point in DATA:
    for coords in point[3]:
        canvasimage.put(decrypt_color(point[2]), coords)
