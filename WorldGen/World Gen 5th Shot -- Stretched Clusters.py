import random
import tkinter

random.seed(input("Enter a seed. \n>>> "))

xrate = random.randint(50, 100) * 0.01
yrate = random.randint(50, 100) * 0.01

class Continent:
    def __init__(self):
        self.bitmap = [(0, 0)]
        for i in range(random.randint(10000, 100000)):
            tochange = random.choice(self.bitmap)
            xchng = random.randint(-1, 1) # how much x changes
            ychng = random.randint(-1, 1) # how much y changes
            if random.random() < xrate:
                xchng = 0
            if random.random() < yrate:
                ychng = 0
            if not (tochange[0] + xchng, tochange[1] + ychng) in self.bitmap:
                self.bitmap.append((tochange[0] + xchng, tochange[1] + ychng))

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=500, height=500)
canvas = tkinter.Canvas(master=window, height=500, width=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

conts_master = []
for i in range(random.randint(2, 6)):
    conts_master.append(Continent())

for cont in conts_master:
    x = random.randint(0, 499)
    y = random.randint(0, 499)
    for pixel in cont.bitmap:
        canvasimage.put("#000000", (pixel[0] + x, pixel[1] + y)) # number in tuple = offset from origin
