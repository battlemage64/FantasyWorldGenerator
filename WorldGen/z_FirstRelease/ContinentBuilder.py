import random
import tkinter

import TileGeneratorSmooth as cg

BIOMETYPES = ('deciduous forest', 'deciduous forest', 'evergreen forest', 'evergreen forest',
              'desert', 'marsh', 'marsh', 'grasslands', 'grasslands',
              'mountains', 'mountains', 'tundra',
              'hills', 'hills') # desert and tundra are half as likely
BIOMECOLORS = {'deciduous forest': '#007700',
               'evergreen forest': '#005500',
               'desert': '#EEEE00',
               'marsh': '#336600',
               'grasslands': '#0000FF',
               'mountains': '#AAAAAA',
               'tundra': '#FFFFFF',
               'hills': '#00DD00'}

class MapContinent:
    def __init__(self, seed=None):
        self.maptiles = []
        self.rivers = []
        if seed == None:
            random.seed()
        else:
            random.seed(seed)

        self.biomegrid = [] # array 5x5 of biomes
        for x in range(6):
            self.biomegrid.append([])
            for y in range(6):
                self.biomegrid[x].append(random.choice(BIOMETYPES))
            
        relevant_points = [] # possible start points for rivers

        for i in range(random.randint(20, 50)):
            positionx = random.randint(0, 599)
            positiony = random.randint(0, 599)
            tile = cg.MapTile(False, offset=10, seed=random.random())

            biomex = int(positionx/100)
            biomey = int(positiony/100)
            tile.biome = self.biomegrid[biomex][biomey] # sets tile biome to whatever is in grid
            tile.position = (positionx, positiony)
            
            if __name__ == '__main__':
                perturbed_polygon = canvas.create_polygon(tile.perturbed_points, fill=BIOMECOLORS[tile.biome], outline='')
                canvas.move(perturbed_polygon, positionx, positiony)

            tilelakes = []
            for k in range(random.randint(0, 4)):
                lake = cg.MapTile(False, True, tile, offset=10, seed=random.random())
                if __name__ == '__main__':
                    perturbed_polygon2 = canvas.create_polygon(lake.perturbed_points, fill='#0000FF', outline='')
                    canvas.move(perturbed_polygon2, positionx, positiony)
                for i in range(random.randint(1, 4)):
                    relevant_points.append(random.choice(lake.perturbed_points))
                tilelakes.append(lake)

            self.maptiles.append((tile, tilelakes))

        for i in range(random.randint(20, 30)): # draw river
            width = random.randint(1, 3) # usd later, possibly changed before used
            # Algorithm: choose 2 pts, draw line, perturb line
            mode = random.randint(1, 5) # obtains 2 #s non-repeating from 1 to 4
            point1 = (random.randint(0, 999), random.randint(0, 999))
            if mode == 1:
                point2 = [0, random.randint(0, 999)] # point is on left
            elif mode == 2:
                point2 = [999, random.randint(0, 999)] # point is on right
            elif mode == 3:
                point2 = [random.randint(0, 999), 999] # point is on top
            elif mode == 4:
                point2 = [random.randint(0, 999), 0] # point is on bottom
            elif relevant_points != []:
                point2 = random.choice(relevant_points)
                width -= 1 # limits width (pre-declared) to 1 or 2
            else:
                point2 = [random.randint(1, 999), random.randint(0, 999)]
            if point1[0] == point2[0]:
                point2[0] -= 1
            slope = (point2[1] - point1[1])/(point2[0] - point1[0]) # slope = (y2-y1)/(x2-x1)
            yint = point1[1] - (point1[0] * slope) # y-int = point y - point x times slope

            river_points = [point1]
            detail = 100
            for i in range(detail):
                x = river_points[-1][0]
                y = river_points[-1][1]
                x += (point2[0] - point1[0])/detail
                y += slope * ((point2[0] - point1[0])/detail)
                river_points.append((x + random.randint(-10, 10), y + random.randint(-10, 10)))
            river_points.append(point2)
            for i in range(random.randint(0, 5)):
                relevant_points.append(random.choice(river_points))
            if __name__ == '__main__':
                canvas.create_line(river_points, fill="#0000FF", width=width)

            self.rivers.append((river_points, width))

def openConfig():
    configWindow = tkinter.Tk()
    configWindow.title('Map Size')
    configWindow.resizable(False, False)
    configWindow.wm_attributes("-topmost", 1)
    scaler = tkinter.Scale(configWindow, from_=0.1, to=3, orient=tkinter.HORIZONTAL, resolution=0.1)
    scaler.pack()
    updateButton = tkinter.Button(configWindow, text="Update", command=lambda: updateconfig(canvas, scaler))
    updateButton.pack()

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

if __name__ == '__main__':
    CANVAS_SIZE = 1000
    window = tkinter.Tk()
    window.title("Your Finished Map")
    window.wm_attributes("-topmost", 1)
    #window.resizable(False, False)
    canvas = tkinter.Canvas(master=window, width=1000, height=1000, bg='#0000FF')
    canvasimage = tkinter.PhotoImage(width=1000, height=1000)
    canvas.pack()
    canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)
    menubar = tkinter.Menu(window)
    configmenu = tkinter.Menu(menubar, tearoff=0)
    configmenu.add_command(label="Resize...", command=openConfig)
    menubar.add_cascade(label="Config", menu=configmenu)
    window.config(menu=menubar)
    cont = MapContinent(input('Enter a seed:\n>>> '))
    print("World generated.")
    window.mainloop()