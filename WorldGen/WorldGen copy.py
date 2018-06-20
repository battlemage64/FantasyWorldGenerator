import random
import tkinter

random.seed(input("Enter a seed. \n>>> "))

cuts = [] # list of all cuts of the rectangle

for iteration in range(random.randint(100, 100)): # iterations of algorithm
    mode = random.sample([1, 2, 3, 4], 2) # obtains 2 #s non-repeating from 1 to 4
    if mode[0] == 1:
        point1 = (0, random.randint(0, 499)) # point is on left
    elif mode[0] == 2:
        point1 = (999, random.randint(0, 499)) # point is on right
    elif mode[0] == 3:
        point1 = (random.randint(0, 999), 499) # point is on top
    else: # here it's 4 but just in case
        point1 = (random.randint(0, 999), 0) # point is on bottom
    # then repeats for point 2 which will be on another side (different mode)
    if mode[1] == 1:
        point2 = (0, random.randint(0, 499)) # point is on left
    elif mode[1] == 2:
        point2 = (999, random.randint(0, 499)) # point is on right
    elif mode[1] == 3:
        point2 = (random.randint(0, 999), 499) # point is on top
    else: # here it's 4 but just in case
        point2 = (random.randint(0, 999), 0) # point is on bottom
    slope = (point2[1] - point1[1])/(point2[0] - point1[0]) # slope = (y2-y1)/(x2-x1)
    yint = point1[1] - (point1[0] * slope) # y-int = point y - point x times slope
    above_below = random.randint(0, 1) # true or false to go above or below
    cuts.append((slope, yint, above_below))

window = tkinter.Tk()
window.title("Your Finished Map")
window.wm_attributes("-topmost", 1)
window.resizable(False, False)
canvasimage = tkinter.PhotoImage(width=1000, height=500)
canvas = tkinter.Canvas(master=window, width=1000, height=500)
canvas.pack()
canvas.create_image(0, 0, image=canvasimage, anchor=tkinter.NW)

for x in range(0, 999):
   for y in range(0, 499):
      count = 0 # count of increments at this location
      for cut in cuts: # evaluate point in each cut
         if y > (x * cut[0] + cut[1]): # cut 0: slope, 1: yint
             if cut[2]: # cut 2: above_below
                 count += 8
             else:
                 count -= 8
         else:
             if not cut[2]:
                 count += 8
             else:
                 count -= 8
      if count > 255:
         count = 255
      elif count < -255:
         count = -255
      numhex = "#"
      if count < 0: # negative -> blue (ocean)
         num = hex(-count)[2:] # makes hex out of positive (not strictly necessary but useful)
         if len(num) == 1: # if only 1 digit (near sea level), add preceding zero
            num = "0" + num
         numhex += "0000" + num
      elif count > 0: # positive -> red (land)
         num = hex(count)[2:]
         if len(num) == 1: # if only 1 digit (near sea level), add preceding zero
            num = "0" + num
         numhex += num + "0000"
      else: # 0 -> purple for now
         numhex = "#800080"
      canvasimage.put(numhex, (x, y))
