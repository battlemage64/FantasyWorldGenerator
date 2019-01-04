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
    window.wm_attributes("-topmost", 1)
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

for i in range(3):
    for j in range(3):
        if j == 0 or j == 2:
            cont = cb.gen_continent(random.random(), "tundra")
        elif j == 1:
            cont = cb.gen_continent(random.random(), "desert")
        for tile in cont[0]:
            xoffset = i*1000 + tile[0][5][0]
            yoffset = j*1000 + tile[0][5][1]
            continent_polygon = canvas.create_polygon(tile[0][2], fill=BIOMECOLORS[tile[0][4]], outline='', tags=("current"))
            canvas.move(continent_polygon, xoffset, yoffset)
            tile[0][6] = continent_polygon

            for lake in tile[1]:
                if __name__ == '__main__':
                    lake_polygon = canvas.create_polygon(lake[2], fill='#0000FF', outline='')
                    canvas.move(lake_polygon, xoffset, yoffset)
            
        for river in cont[1]: # ([points], width)
            riverpts = []
            for point in river[0]:
                riverpts.append((point[0] + i*1000, point[1] + j*1000))
            canvas.create_line(riverpts, fill="#0000FF", width=river[1])

        canvas.create_rectangle(canvas.bbox("current"), outline="red")
        canvas.dtag("all", "current")
