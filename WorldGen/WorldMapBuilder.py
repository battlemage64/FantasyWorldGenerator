import random
import tkinter

import ContinentBuilder as cb

BIOMETYPES = ('deciduous forest', 'deciduous forest', 'evergreen forest', 'evergreen forest',
              'desert', 'marsh', 'marsh', 'grasslands', 'grasslands',
              'mountains', 'mountains', 'tundra',
              'hills', 'hills') # desert and tundra are half as likely
BIOMECOLORS = {'deciduous forest': '#007700',
               'evergreen forest': '#005500',
               'desert': '#EEEE00',
               'marsh': '#336600',
               'grasslands': '#00FF00',
               'mountains': '#AAAAAA',
               'tundra': '#FFFFFF',
               'hills': '#00DD00'}

CANVAS_SIZE = 3000

previous = 1
def updateconfig(canvas, scale):
    'Called by config window, updates config settings'
    global previous
    canvas.scale("all", 0, 0, 1/previous, 1/previous)
    canvas.scale("all", 0, 0, scale.get(), scale.get())
    if scale.get() * CANVAS_SIZE < CANVAS_SIZE:
        canvas.config(width=scale.get() * CANVAS_SIZE, height=scale.get() * CANVAS_SIZE, scrollregion=(0, 0, scale.get()*1000, scale.get()*1000))
    else:
        canvas.config(width=CANVAS_SIZE, height=CANVAS_SIZE, scrollregion=(0, 0, scale.get()*CANVAS_SIZE, scale.get()*CANVAS_SIZE))
    if scale.get() <= 0.7:
        canvas.itemconfig("river_small", state='hidden')
    else:
        canvas.itemconfig("river_small", state='normal')
    if scale.get() <= 0.4:
        canvas.itemconfig("river_medium", state='hidden')
    else:
        canvas.itemconfig("river_medium", state='normal')
    if scale.get() < 0.2:
        canvas.itemconfig("river_large", state='hidden')
    else:
        canvas.itemconfig("river_large", state='normal')
    previous = scale.get()

def openConfig():
    configWindow = tkinter.Tk()
    configWindow.title('Map Size')
    configWindow.resizable(False, False)
    scaler = tkinter.Scale(configWindow, from_=0.1, to=3, orient=tkinter.HORIZONTAL, resolution=0.1)
    scaler.pack()
    updateButton = tkinter.Button(configWindow, text="Update", command=lambda: updateconfig(canvas, scaler))
    updateButton.pack()

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title("Your Finished Map")
    window.wm_attributes("-topmost", True) # puts window on top, then cancels forced top
    window.wm_attributes("-topmost", False)
    window.resizable(False, False)
    
    frame = tkinter.Frame(window)
    frame.pack()
    
    scrollframex = tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL)
    scrollframey = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
    scrollframex.pack(side=tkinter.BOTTOM)
    scrollframey.pack(side=tkinter.RIGHT)
    scrollframex.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    scrollframey.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    
    canvas = tkinter.Canvas(master=frame, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='#0000FF')
    canvas.config(xscrollcommand=scrollframex.set, yscrollcommand=scrollframey.set, scrollregion=canvas.bbox("all"))
    canvas.pack()

    scrollframex.config(command=canvas.xview)
    scrollframey.config(command=canvas.yview)

    menubar = tkinter.Menu(window)
    configmenu = tkinter.Menu(menubar, tearoff=0)
    configmenu.add_command(label="Resize...", command=openConfig)
    menubar.add_cascade(label="Config", menu=configmenu)
    window.config(menu=menubar)

if __name__ == '__main__':
    seed = input("Enter a seed:\n>>>")
    random.seed(seed)

takenboxes = []

for i in range(random.randint(4, 7)):
    cont = cb.gen_continent(random.random())
    for tile in cont[0]:
        xoffset = tile[0][5][0]
        yoffset = tile[0][5][1]
        continent_polygon = canvas.create_polygon(tile[0][3], fill=BIOMECOLORS[tile[0][4]], outline='', tags=("bbox"))
        canvas.move(continent_polygon, xoffset, yoffset)
        tile[0][6] = continent_polygon

    contdimensions = canvas.bbox("bbox")
    canvas.delete("bbox")
    canvas.dtag("all", "bbox")
    
    positiontaken = True
    timeout = 0
    timedout = False
    while positiontaken:
        contxoffset = random.randint(0, 2000) # any more and it'll stick off the edge of the map
        contyoffset = random.randint(0, 2000)

        if len(takenboxes):
            positiontaken = True # assume position is taken unless proved otherwise
        else:
            positiontaken = False # no continents yet, must be available
        ## positiontaken = False # use this line for the commented-out code below

        x1 = contxoffset + contdimensions[0]
        y1 = contyoffset + contdimensions[1]
        x2 = contxoffset + contdimensions[2]
        y2 = contyoffset + contdimensions[3]

        touching = [] # list of whether cont would touch each other cont
        
        for bbox in takenboxes:
##                if x1 in range(bbox[0], bbox[2]) and y1 in range(bbox[1], bbox[3]):
##                    positiontaken = True
##                if x2 in range(bbox[0], bbox[2]) and y1 in range(bbox[1], bbox[3]):
##                    positiontaken = True
##                if x1 in range(bbox[0], bbox[2]) and y2 in range(bbox[1], bbox[3]):
##                    positiontaken = True
##                if x2 in range(bbox[0], bbox[2]) and y2 in range(bbox[1], bbox[3]):
##                    positiontaken = True
            if x1 > bbox[2] or y1 > bbox[3] or x2 < bbox[0] or y2 < bbox[1]: # if any side of bbox is too far to be overlapping
                touching.append(False)
            else:
                touching.append(True)

        if not True in touching: # touching no continents
            positiontaken = False

        timeout += 1
        if timeout == 50:
            timedout = True
            print("Timeout while placing continent")

    if timedout:
        continue

    if contyoffset < 200 or contyoffset > 800: # if necessary, replace desert with tundra
        print(cont[2])
        for x in range(6):
            for y in range(6):
                if cont[2][x][y] == "desert":
                    cont[2][x][y] = "tundra"

    for tile in cont[0]:
        xoffset = contxoffset + tile[0][5][0]
        yoffset = contyoffset + tile[0][5][1]
        continent_polygon = canvas.create_polygon(tile[0][3], fill=BIOMECOLORS[tile[0][4]], outline='', tags=("current"))
        canvas.move(continent_polygon, xoffset, yoffset)
        tile[0][6] = continent_polygon

        for lake in tile[1]:
            if __name__ == '__main__':
                lake_polygon = canvas.create_polygon(lake[3], fill='#0000FF', outline='')
                canvas.move(lake_polygon, xoffset, yoffset)
        
    for river in cont[1]: # ([points], width)
        riverpts = []
        for point in river[0]:
            riverpts.append((point[0] + contxoffset, point[1] + contyoffset))
        if river[1] == 1:
            tags = ("river_small")
        elif river[1] == 2:
            tags = ("river_medium")
        else:
            tags = ("river_large")
        canvas.create_line(riverpts, fill="#0000FF", width=river[1], tags=tags)

    canvas.create_rectangle(canvas.bbox("current"), outline="red")
    takenboxes.append(canvas.bbox("current"))
    canvas.dtag("all", "current")

