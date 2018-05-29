import random
import tkinter

class Continent:
    def __init__(self):
        self.bitmap = [(0, 0)]
        for i in range(random.randint(1000, 10000)):
            tochange = random.choice(self.bitmap)
            xchng = random.randint(-1, 1) # how much x changes
            ychng = random.randint(-1, 1) # how much y changes
            if random.randint(0, 2) != 0: # 50% chance to not go up or down
                ychng = 0 # result: continents fatter than wide
            if not (tochange[0] + xchng, tochange[1] + ychng) in self.bitmap:
                self.bitmap.append((tochange[0] + xchng, tochange[1] + ychng))

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=100, height=100)
canvas = tkinter.Canvas(master=window, height=100, width=100)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)
cont = Continent()
for pixel in cont.bitmap:
    canvasimage.put("#000000", (pixel[0] + 50, pixel[1] + 50)) # number in tuple = offset from origin
