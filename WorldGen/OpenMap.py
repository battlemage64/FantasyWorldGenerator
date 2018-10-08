import tkinter
import os
import re
import WGInteractable

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

class FileCorruptedError(Exception):
    "Raised if file data is corrupted or invalid"
    pass

class FileOutOfDateError(Exception):
    "Raised if file is the wrong version"
    pass

saves_found = os.listdir("./Maps")
print("Found saves:")
for item in saves_found:
    if ishidden(item):
        continue
    file = open("./Maps/"+item, 'r')
    contents = file.readlines()
    #map_name = contents[0].replace("Map name: ", "") # could just slice it off but this is more legible
    #print("Map {mapname} file {filename}".format(mapname=map_name, filename=item))
    print(contents[0], contents[1], contents[2], contents[3])
    file.close()

while True:
    filename = input("Open which file?\n>>>") + ".fwgmap"
    if not filename in saves_found or ishidden(filename): # ishidden just in case
        print("Invalid file name")
    else:
        break

SAVE_FILE = open("./Maps/"+filename, 'r')
CONTENTS = SAVE_FILE.readlines()
SAVE_FILE.close()

if not CONTENTS[2] in ["Version: 1.0\n"]: # list of supported file types
    raise FileOutOfDateError("File version is {version}; supported file versions: 1.0".format(version=CONTENTS[2][:-1]))

MAP_NAME = CONTENTS[0].replace("Map name: ", "")
try:
    RESOLUTION = re.findall("[0-9]+x", CONTENTS[3])[0]
except:
    raise FileCorruptedError("Missing resolution")
DATA = eval(CONTENTS[4])

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
        if RESOLUTION == "1x":
            canvasimage.put(decrypt_color(point[2]), coords)
        elif RESOLUTION == "9x":
            canvas.create_rectangle(coords[0]-1, coords[1]-1, coords[0]+1, coords[1]+1, fill=decrypt_color(point[2]), outline=decrypt_color(point[2]))
        elif RESOLUTION == "25x":
            canvas.create_rectangle(coords[0]-2, coords[1]-2, coords[0]+2, coords[1]+2, fill=decrypt_color(point[2]), outline=decrypt_color(point[2]))
        else:
            raise FileCorruptedError("Invalid resolution")
