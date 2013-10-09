# Comm Ave Frogger
# Creators: Dean De Carli, Matthew Kasper, Matthew Owney
# Credit for the idea goes to Alex O'Donovan
# Credit for the vehicle and background design goes to Leah Kallins and Josh Hughes

import tkinter as tk
from tkinter import *

#player object
class Rhett:
    x1 = 435
    y1 = 530
    x2 = 460
    y2 = 555
    row = -1
    lifenum = 4 #algorithm starts with n+1

    # Creates Rhetts lives and calls gameover when you die 3 times 
    def lives(self,canvas): # called in vehicleinit() and isCollison()
        canvas.delete("lives")
        for i in range(self.lifenum-1):
            #draw the life boxes
            canvas.create_image(15 + (i)*26, 500, image = canvas.data['rhett'], tag="lives") 
        self.lifenum -= 1
        canvas.create_text(45,475, text='Lives',font = ('Helvetica',15,'bold'), fill='white')
        if self.lifenum == 0:
            #restart rhett, but cars moving
            canvas.data["needdone"]=False
            vehicleinit(canvas) # CALL
            canvas.create_text(450,260, text='GameOver',font = ('Helvetica',15,'bold'), fill='white', tag='msg')

    # redraws Rhett and resets gameover to false 
    def reinit(self,canvas): # called in gameOver()
        self.x1 = 435
        self.y1 = 530
        self.x2 = 460
        self.y2 = 5505
        canvas.data["gameover"]=False
        canvas.delete("msg")
        canvas.delete("rhett")
        Rhett.draw(Rhett,canvas)# CALL

    # draws Rhett when canvas is initialized and at every keypress
    def draw(self, canvas): # called in vehicleinit() and keyPressed()
        canvas.create_image(self.x1, self.y1, image = canvas.data['rhett'], tag = 'rhett')

    # moves Rhett with every keypress and prevents him from moving off the screen 
    def move(self, vert, hor): # called in keyPressed()
        self.x1 += hor
        self.y1 += vert
        self.x2 += hor
        self.y2 += vert
        #screen boundary testing
        if self.x1 < 5:
            self.x1 = 5
        if self.y1 < 5:
            self.y1 = 5
        if self.x1 > 865:
            self.x1 = 865
        if self.y1 > 525:
            self.y1 = 525
        if self.x2 < 30:
            self.x2 = 30
        if self.y2 < 30:
            self.y2 = 30
        if self.x2 > 890:
            self.x2 = 890
        if self.y2 > 550:
            self.y2 = 550

    # Allows for Rhett's current row to be determined
    def findRow(self):
         if self.y1 < 50:
            self.row = 0
         elif self.y1 > 50 and self.y1 < 100:
            self.row = 1
         elif self.y1 > 100 and self.y1 < 150:
            self.row = 2
         elif self.y1 > 150 and self.y1 < 200:
            self.row = 3
         elif self.y1 > 300 and self.y1 < 350:
            self.row = 4
         elif self.y1 > 350 and self.y1 < 400:
            self.row = 5
         elif self.y1 > 400 and self.y1 < 450:
            self.row = 6
         elif self.y1 > 450 and self.y1 < 500:
            self.row = 7
         return self.row

class vehicle:
    #initialize variables
    x = 0
    y = 0
    speed = 0
    #vehicle id
    viid = ""
    # sets vehicle objects initial imagename, location, speed, row, and respawn rate
    def __init__(self, row, canvas):
        if row == 0:
            self.imagename = canvas.data["bike1"]
            self.x = 0
            self.y = 70
            self.speed = 2
            self.row = row
            self.respawn = 180
        elif row == 1:
            self.imagename = canvas.data["car1"]
            self.x = 0
            self.y = 120
            self.speed = 4
            self.row = row
            self.respawn = 252
        elif row == 2:
            self.imagename = canvas.data["bus1"]
            self.x = 0
            self.y = 170
            self.speed = 5
            self.row = row
            self.respawn = 300
        elif row == 3:
            self.imagename = canvas.data["train1"]
            self.x = 0
            self.y = 220
            self.speed = 3
            self.row = row
            self.respawn = 444
        elif row == 4:
            self.imagename = canvas.data["train2"]
            self.x = 890
            self.y = 320
            self.speed = -3
            self.row = row
            self.respawn = 446
        elif row == 5:
            self.imagename = canvas.data["car2"]
            self.x = 890
            self.y = 370
            self.speed = -4
            self.row = row
            self.respawn = 642
        elif row == 6:
            self.imagename = canvas.data["bus2"]
            self.x = 890
            self.y = 420
            self.speed = -5
            self.row = row
            self.respawn = 590
        elif row == 7:
            self.imagename = canvas.data["bike2"]
            self.x = 890
            self.y = 470
            self.speed = -2
            self.row = row
            self.respawn = 668

    # moves the vehicles 
    def moveyourself(self): # called in drawyourself()
        self.x += self.speed

    # draws the vehicles on the canvas 
    def drawyourself(self,canvas): # called in timerFired()
        self.moveyourself() # CALL
        canvas.delete(self.viid)
        self.viid = canvas.create_image(self.x, self.y, image = self.imagename, tag = 'transport')

    # Deletes vehicles when they get to the end of the board
    def deleteyourself(self,canvas,vlist): # called in timerFired()
        if  self.speed > 0 and self.x > 890:
            vlist.remove(self)
            canvas.delete(self.viid)
        elif self.speed < 0 and self.x < 0:
            vlist.remove(self)
            canvas.delete(self.viid)

    # draws a new vehicle when it reaches the respawn distance
    def drawanother(self,canvas,vlist): # called in timerFired
        if self.x == self.respawn:
            vlist.append(vehicle(self.row,canvas))

    # Collison detection and Win detection, adds to Score board and subtracts from life 
    def isCollision(self, canvas): # called in timerFired() 
        score  = 0
        gRow = Rhett.findRow(Rhett) # CALL
        for i in range(1,9):
            if Rhett.y1 < 35: #if Rhetts position is in the top row, the game is won and score incremented
                canvas.create_text(450,270, text='You Win',font = ('Helvetica',15,'bold'), tag = "msg", fill='white')
                canvas.after(1000, Rhett.reinit, Rhett, canvas)
                canvas.data["gameover"]=True
                canvas.data["Score"] = canvas.data["Score"]+1
                #this function runs 8 times every scoring, so we must use score%8
                if canvas.data["Score"]%8 == 0:
                    canvas.delete("score")
                    canvas.create_text(50,35, text='Score:'+str(int(canvas.data['Score']/8)),font = ('Helvetica',15,'bold'), fill = 'white', tag = "score")
        if self.imagename == canvas.data['car1']:#defines collision boundaries for the car
            if Rhett.x1 > self.x - 41 and Rhett.x1 < self.x + 41 and Rhett.y1 > self.y - 17 and Rhett.y1 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            if Rhett.x2 > self.x - 41 and Rhett.x2 < self.x + 41 and Rhett.y2 > self.y - 17 and Rhett.y2 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            else:
                return False
        elif self.imagename == canvas.data['car2']:#defines collision boundaries for the car
            if Rhett.x1 > self.x - 53 and Rhett.x1 < self.x + 53 and Rhett.y1 > self.y - 17 and Rhett.y1 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            if Rhett.x2 > self.x - 53 and Rhett.x2 < self.x + 53 and Rhett.y2 > self.y - 17 and Rhett.y2 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            else:
                return False
        elif self.imagename == canvas.data['bike1'] or self.imagename == canvas.data['bike2']:#defines collision boundaries for the bikes
            if Rhett.x1 > self.x - 16 and Rhett.x1 < self.x + 16 and Rhett.y1 > self.y - 17 and Rhett.y1 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            if Rhett.x2 > self.x - 16 and Rhett.x2 < self.x + 16 and Rhett.y2 > self.y - 17 and Rhett.y2 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            else:
                return False
        elif self.imagename == canvas.data['bus1'] or self.imagename == canvas.data['bus2']:#defines collision boundaries for the buses
            if Rhett.x1 > self.x - 38 and Rhett.x1 < self.x + 38 and Rhett.y1 > self.y - 17 and Rhett.y1 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            if Rhett.x2 > self.x - 38 and Rhett.x2 < self.x + 38 and Rhett.y2 > self.y - 17 and Rhett.y2 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            else:
                return False
        elif self.imagename == canvas.data['train1'] or self.imagename == canvas.data['train2']:#defines collision boundaries for the trains
            if Rhett.x1 > self.x - 79 and Rhett.x1 < self.x + 79 and Rhett.y1 > self.y - 17 and Rhett.y1 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True
            if Rhett.x2 > self.x - 79 and Rhett.x2 < self.x + 79 and Rhett.y2 > self.y - 17 and Rhett.y2 < self.y + 17:
                Rhett.lives(Rhett,canvas) # CALL
                return True 
            else:
                return False
# Moves Rhett with the arrow keys
def keyPressed(event): # called in begin()
    canvas = event.widget.canvas
    #disable moving in gameover state
    if canvas.data["gameover"]:
        return
    if event.keysym == 'Up':
        Rhett.move(Rhett, -20, 0) # CALL
        canvas.delete('rhett')
        Rhett.draw(Rhett, canvas) # CALL
    elif event.keysym == 'Down':
        Rhett.move(Rhett, 20, 0) # CALL
        canvas.delete('rhett')
        Rhett.draw(Rhett, canvas) # CALL
    elif event.keysym == 'Left':
        Rhett.move(Rhett, 0, -20) # CALL
        canvas.delete('rhett')
        Rhett.draw(Rhett, canvas) # CALL
    elif event.keysym == 'Right':
        Rhett.move(Rhett, 0, 20) # CALL
        canvas.delete('rhett')
        Rhett.draw(Rhett, canvas) # CALL

# Resets Rhett's position with .reinit() when you die and creates "Try Again" text
def gameOver(canvas): # called in timerFired()
    canvas.create_text(450,280, text='Try Again',font = ('Helvetica',15,'bold'),
                       tag="msg", fill='white')
    canvas.data["gameover"]=True
    canvas.after(1000, Rhett.reinit, Rhett, canvas) # CALL

# Calls all the vehicle draw functions and Collison detection
def timerFired(canvas,a): # called in vehicleinit() and calls itslef
    for v in a:
        v.drawyourself(canvas) # CALL
        v.drawanother(canvas,a) # CALL
        v.deleteyourself(canvas,a) # CALL
        if not canvas.data["gameover"]:
            if v.isCollision(canvas): # CALL
                gameOver(canvas) # CALL
    if canvas.data["needdone"]:
#        when "needdone"==True, skip passing this list to the timer fired. This because it will be making another thread of
#        timerfired()'s whith another list of vehicles, which will be on there with the original list. so "needdone" is checking
#        whether antoher thread of vehicles need's done
        canvas.after(canvas.data["delay"], timerFired, canvas, a) # CALL

# Intiates all the vehicles, Rhett and the Score board
# In this function, the list of vehicles needing rendered is initialized inside of list a.
# Everytime timerfired is called, it updates the posiiton of every single car and draws them. It also checks
# for win, loose, and screen edges. If it reaches the end of the screen, a.remove(self) is called from
# within a funciton in the object. When it reaches its respawn point, it a.append(vehicle(self.row, canvas)),
# which adds another vehcile in the same lane to the render list.
def vehicleinit(canvas): # called in begin() and Rhett.lives()
    canvas.delete(ALL)
#################*** the speed of the cars can be changed here***##############
    canvas.data["delay"]=20
    a = []
    a = [vehicle(i,canvas) for i in range(8)]
    timerFired(canvas,a) # CALL
    canvas.data["needdone"]=True
    canvas.create_image(445,275, image = canvas.data["background"])
    Rhett.draw(Rhett, canvas) # CALL
    Rhett.lifenum = 4
    Rhett.lives(Rhett,canvas) # CALL
    canvas.data["Score"]=0
    canvas.create_text(50,35, text='Score:'+str(canvas.data['Score']),font = ('Helvetica',15,'bold'), fill = 'white', tag = "score")

# Creates the canvas and the dictionary
def begin():
    root = Tk()
    canvas = Canvas(root, width=890, height=550) #Golden Ratio, just like the Greeks
    canvas.pack()
    root.bind("<Key>", keyPressed) # CALL
    root.canvas = canvas.canvas = canvas
    canvas.data = {"background":tk.PhotoImage(file='froggy.gif'),
                   "rhett":tk.PhotoImage(file='rhett.gif'),
                   "car1":tk.PhotoImage(file='car4.gif'),
                   "car2":tk.PhotoImage(file="car.gif"),
                   "bus1":tk.PhotoImage(file="bus3.gif"),
                   "bus2":tk.PhotoImage(file="bus4.gif"),
                   "bike1":tk.PhotoImage(file="guy_bike.gif"),
                   "bike2":tk.PhotoImage(file="girl_bike.gif"),
                   "train1":tk.PhotoImage(file="train.gif"),
                   "train2":tk.PhotoImage(file="train.gif"),
                   "gameover":False,
                   "needdone":True,
                   "Score":0}
    vehicleinit(canvas) # CALL
    root.mainloop()

begin()
