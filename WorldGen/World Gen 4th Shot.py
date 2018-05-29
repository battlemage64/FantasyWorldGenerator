from tkinter import *
import random

cells = []

for i in range(0, 100):
   cells.append([])
   for j in range(0, 100):
       cells[i].append([])

for i in range(0, 100):
   for j in range(0, 100):
      cells[i][j] = 0

for i in range(0, 100):
   cells[i][99] = 1
   cells[i][0] = 1
   cells[99][i] = 1
   cells[0][i] = 1

for a in range(1, 5):
   cells[random.randint(0, 99)][random.randint(0, 99)] = 1

for a in range(1, 50):
   for i in range(1, 99):
      for j in range(1, 99):
         if cells[i][j] == 1 and random.randint(1, 3) != 1:
            way = random.randint(1, 8)
            if way == 1 and cells[i][j+1] == 0 and random.randint(0, 1):
               cells[i][j+1] = 2
            if way == 2 and cells[i][j-1] == 0 and random.randint(0, 1):
               cells[i][j-1] = 2
            if way == 3 and cells[i-1][j] == 0:
               cells[i-1][j] = 2
            if way == 4 and cells[i+1][j] == 0:
               cells[i+1][j] = 2
            if way == 5 and cells[i-1][j-1] == 0 and random.randint(0, 1):
               cells[i-1][j-1] = 2
            if way == 6 and cells[i-1][j+1] == 0 and random.randint(0, 1):
               cells[i-1][j+1] = 2
            if way == 7 and cells[i+1][j-1] == 0 and random.randint(0, 1):
               cells[i+1][j-1] = 2
            if way == 8 and cells[i+1][j+1] == 0 and random.randint(0, 1):
               cells[i+1][j+1] = 2

   for i in range(0, 99):
      for j in range(0, 99):
         if cells[i][j] == 2:
            cells[i][j] = 1

window = Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = PhotoImage(width=100, height=100)
canvas = Canvas(master=window, height=100, width=100)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=NW)
for i in range(0, 100):
   for j in range(0, 100):
      if cells[i][j] == 1:
         canvasimage.put("#000000", (i, j))
