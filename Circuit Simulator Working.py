#################################################
# 15-112-n19 hw4-2
# Your Name: Zachary Zheng
# Your Andrew ID: zacharyz
# Your Section: C
# Collaborators: N/A
#################################################

#isPrime function taken off from website
def isPrime(n):
    if (n < 2):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False
    maxFactor = round(n**0.5)
    for factor in range(3,maxFactor+1,2):
        if (n % factor == 0):
            return False
    return True

#uses backtracking recursive method to find the smallest RTP number of a length
def findRTP(digits, smallestRTP = 0):
    #base case: checks if we have reached a RTP with the # of digits desired
    if len(str(smallestRTP)) == digits and isPrime(smallestRTP):
        return smallestRTP
    #recursive case with backtracking
    for dig in range(10):
        smallestRTP = (smallestRTP * 10) + dig #adding digit is the 'move'
        if isPrime(smallestRTP): #this is the 'isValid' function
            tmpSolution = findRTP(digits, smallestRTP)
            if tmpSolution != None:
                return tmpSolution
        smallestRTP = (smallestRTP - dig) // 10 #undos the 'move'
    return None
 
################################################################################
#Circuit Simulator
################################################################################
 
##main class that keeps track of each gate's input, output info 
class Gate(object):
    
    #stores the info for each gate
    def __init__(self, cx, cy):
        self.inputGates = []
        self.outputGates = []
        self.inputValues = [ ]
        self.outputValue = None
        self.cx = cx
        self.cy = cy
    
    #displays the input gate that's connected to it
    def getInputGates(self):
        return self.inputGates
    
    #displays the output gate that's connected to it
    def getOutputGates(self):
        return self.outputGates
        
    def getMaxInputGates(self):
        return 1
    
    #main connect function that connects two gates and transfers their values    
    def connectTo(self, otherGate):
        if len(otherGate.inputGates) < otherGate.getMaxInputGates():
            self.outputGates.append(otherGate)
            otherGate.inputGates.append(self)
            otherGate.inputValues.append((self, self.outputValue))

##keeps track of info for the Input gate (inherits from Gate)        
class Input(Gate):
    
    #gets the coordinate of the input gate's output node
    def outputLoc(self, data):
        radius = data.cellSize / 12
        return self.cx + radius + data.lineLen, self.cy
    
    #max amount of input gates for the Input
    def getMaxInputGates(self):
        return 0
    
    #sets the input value of the input gate and then updates each connection
    def setInputValue(self, fromGate, value):
        if type(self.getOutputGates()[0]) == Output: #base case
            self.inputValues = [(fromGate, value)]
            self.outputValue = value 
            self.getOutputGates()[0].inputValues = [(self, value)]
            self.getOutputGates()[0].outputValue = value
        else: #recursive case
            self.inputValues = [(fromGate, value)]
            self.outputValue = value
            for eachOutput in range(len(self.getOutputGates())):
            #finds the index at which a desired gate is located in
                for i in range(len(self.getOutputGates()[eachOutput].\
                inputValues)):
                    if self.getOutputGates()[eachOutput].inputValues[i][0] == \
                    self:
                        index = i #index of the desired gate from inputValues
                self.getOutputGates()[eachOutput].inputValues[index] = (self, \
                value) #sets the input value for the gate it's connected to
                #gets the next gate
                self.getOutputGates()[eachOutput].setInputValue(self, value)
    
    #draws the input gate            
    def draw(self, canvas, data, color):
        #color parameter is either red or black; determined if gate is clicked
        innerRadius = data.cellSize / 16
        radius = data.cellSize / 12
        textDist = data.cellSize / 6
        outputX, outputY = self.cx + radius + data.lineLen, self.cy
        canvas.create_line(outputX, outputY, self.cx + radius, self.cy, \
        fill = "pink", width = 2)
        canvas.create_oval(self.cx - radius, self.cy - radius, self.cx + \
        radius, self.cy + radius, fill = "pink") 
        canvas.create_oval(self.cx - innerRadius, self.cy - innerRadius, \
        self.cx + innerRadius, self.cy + innerRadius, fill = color) 

##keeps track of info for the Output gate (inherits from Gate)
class Output(Gate):

    #gets the coordinate of the output gate's input node
    def inputLoc(self, data):
        radius = data.cellSize / 12
        return self.cx - radius - data.lineLen, self.cy
        
    #max amount of input gates for the Output
    def getMaxInputGates(self):
        return 1
    
    #draws the output gate    
    def draw(self, canvas, data, color):
        #color parameter is either red or black; determined if gate is clicked
        innerRadius = data.cellSize / 16
        radius = data.cellSize / 12
        textDist = data.cellSize / 6
        outputX, outputY = self.cx - radius - data.lineLen, self.cy
        canvas.create_line(outputX, outputY, self.cx - radius, self.cy, \
        fill = "green", width = 2)
        canvas.create_oval(self.cx - radius, self.cy - radius, self.cx + \
        radius, self.cy + radius, fill = "green")  
        canvas.create_oval(self.cx - innerRadius, self.cy - innerRadius, \
        self.cx + innerRadius, self.cy + innerRadius, fill = color)  

##keeps track of info for the Not gate (inherits from Gate)
class Not(Gate):

    #gets the coordinate of the not gate's input node
    def inputLoc(self, data):
        radius = data.cellSize / 6
        return self.cx - radius - data.lineLen, self.cy
    
    #gets the coordinate of the not gate's output node    
    def outputLoc(self, data):
        radius = data.cellSize / 6
        return self.cx + radius + data.lineLen, self.cy
        
    #max amount of input gates for the Not gate
    def getMaxInputGates(self):
        return 1
    
    #recursing function that updates the value of the gate it's connected to
    def setInputValue(self, fromGate, value):
        #base case
        if type(self.getOutputGates()[0]) == Output:
            self.inputValues = [(fromGate, value)]
            self.outputValue = not value 
            self.getOutputGates()[0].inputValues = [(self, not value)]
            self.getOutputGates()[0].outputValue = not value
        #recursive case
        else:
            self.inputValues = [(fromGate, value)]
            self.outputValue = not value
            #finds the index at which a desired gate is located in
            for i in range(len(self.getOutputGates()[0].inputValues)):
                if self.getOutputGates()[0].inputValues[i][0] == self:
                    index = i #index of the desired gate from inputValues
            self.getOutputGates()[0].inputValues[index] = (self, not value)
            #gets the next gate
            self.getOutputGates()[0].setInputValue(self, not value)
    
    #draws the NOT gate        
    def draw(self, canvas, data):
        radius = data.cellSize / 6
        x0, y0 = self.cx - radius, self.cy - radius / 2
        x1, y1 = self.cx + radius, self.cy
        x2, y2 = self.cx - radius, self.cy + radius / 2
        inputX, inputY = self.cx - radius - data.lineLen, self.cy
        outputX, outputY = self.cx + radius + data.lineLen, self.cy
        #input node
        canvas.create_line(inputX,inputY,self.cx - radius,self.cy,fill = \
        "green",width = 2)
        #output node
        canvas.create_line(outputX,outputY,self.cx + radius,self.cy,fill = \
        "pink",width = 2)
        #gate shape
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill = "gray")

##keeps track of info for the And gate (inherits from Gate)
class And(Gate):
     
    #gets the coordinate of the and gate's input node    
    def inputLoc(self, data):
        radius = data.cellSize / 6
        return self.cx - radius, self.cy
    
    #gets the coordinate of the and gate's output node    
    def outputLoc(self, data):
        radius = data.cellSize / 6
        return self.cx + radius + data.lineLen, self.cy
    
    #max amount of input gates for the And gate
    def getMaxInputGates(self):
        return 2
    
    #helper function that conducts the AND logic
    def andChecker(self): 
        for eachGate in self.inputValues:
            if eachGate[1] == None:
                return None
        for eachGate in self.inputValues:
            if eachGate[1] != True:
                return False
        return True
    
    #recursing function that updates the value of the gate it's connected to
    def setInputValue(self, fromGate, value):
        #base case
        if type(self.getOutputGates()[0]) == Output:
            value = self.andChecker()
            self.outputValue = value
            self.getOutputGates()[0].inputValues = [(self, value)]
            self.getOutputGates()[0].outputValue = value
        #recursive case           
        else:
            value = self.andChecker()
            self.outputValue = value
            #finds the index at which a desired gate is located in
            for i in range(len(self.getOutputGates()[0].inputValues)):
                if self.getOutputGates()[0].inputValues[i][0] == self:
                    index = i #index of the desired gate from inputValues
            self.getOutputGates()[0].inputValues[index] = (self, value)
            #gets the next gate
            self.getOutputGates()[0].setInputValue(self, value) 
    
    #draw the AND gate        
    def draw(self, canvas, data):
        radius = data.cellSize / 6
        x0, y0 = self.cx - radius, self.cy - radius
        x1, y1 = self.cx + radius / 2, y0
        x2, y2 = self.cx + radius, self.cy
        x3, y3 = x1, self.cy + radius
        x4, y4 = self.cx - radius, self.cy + radius
        inputX1, inputY1 = x0 - data.lineLen, self.cy - radius / 2
        inputX2, inputY2 = x0 - data.lineLen, self.cy + radius / 2
        outputX, outputY = x2 + data.lineLen, self.cy
        #input nodes
        canvas.create_line(inputX1, inputY1, x0, self.cy - radius / 2, fill = \
        "green", width = 2)
        canvas.create_line(inputX2, inputY2, x0, self.cy + radius / 2, fill = \
        "green", width = 2)
        #output node
        canvas.create_line(outputX, outputY, x2, y2, fill = "pink", width = 2)
        #gate shape
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, fill = \
        "gray")

##keeps track of info for the Or gate (inherits from Gate)            
class Or(Gate):
    
    #gets the coordinate of the or gate's input node
    def inputLoc(self, data):
        innerRadius = data.cellSize / 12
        radius = data.cellSize / 6
        return self.cx - innerRadius, self.cy
    
    #gets the coordinate of the or gate's output node    
    def outputLoc(self, data):
        radius = data.cellSize / 6
        return self.cx + radius + data.lineLen, self.cy
    
    #max amount of input gates for the Or gate
    def getMaxInputGates(self):
        return 2
    
    #helper function that conducts the OR logic
    def orChecker(self): 
        for eachGate in self.inputValues:
            if eachGate[1] == None:
                return None
        for eachGate in self.inputValues:
            if eachGate[1] == True:
                return True
        return False
    
    #recursing function that updates the value of the gate it's connected to 
    def setInputValue(self, fromGate, value):
        #base case
        if type(self.getOutputGates()[0]) == Output:
            value = self.orChecker()
            self.outputValue = value
            self.getOutputGates()[0].inputValues = [(self, value)]
            self.getOutputGates()[0].outputValue = value
        #recursive case           
        else:
            value = self.orChecker
            self.outputValue = value
            #finds the index at which a desired gate is located in
            for i in range(len(self.getOutputGates()[0].inputValues)):
                if self.getOutputGates()[0].inputValues[i][0] == self:
                    index = i #index of the desired gate from inputValues
            self.getOutputGates()[0].inputValues[index] = (self, value)
            #gets the next gate
            self.getOutputGates()[0].setInputValue(self, value) 
    
    #draw the OR gate
    def draw(self, canvas, data):
        radius = data.cellSize / 6
        innerRadius = data.cellSize / 12
        x0, y0 = self.cx - innerRadius, self.cy
        x1, y1 = self.cx - radius, self.cy - radius
        x2, y2 = self.cx + radius, self.cy
        x3, y3 = self.cx - radius, self.cy + radius
        inputX1, inputY1 = x0 - data.lineLen, (y0 + y1) / 2
        inputX2, inputY2 = x0 - radius + data.lineLen, (y0 + y3) / 2
        outputX, outputY = self.cx + radius + data.lineLen, y2 
        #input nodes
        canvas.create_line(inputX1, inputY1, self.cx - innerRadius, inputY1, \
        fill = "green", width = 2)
        canvas.create_line(inputX2, inputY2, self.cx - innerRadius, inputY2, \
        fill = "green", width = 2)
        #output node
        canvas.create_line(outputX, outputY, x2, y2, fill = "pink", width = 2)
        #gate shape
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = "gray")
            
################################################################################
#ignore_rest
################################################################################

import math, random
from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.margin = 40
    data.buttonNum = 5
    data.cellSize = (data.height - data.margin) / data.buttonNum
    data.lineLen = data.cellSize / 12 #length of the input/output nodes
    data.notClicked = False
    data.orClicked = False
    data.andClicked = False
    data.inputClicked = False
    data.outputClicked = False
    data.notGates = []
    data.orGates = []
    data.andGates = []
    data.inputGates = []
    data.outputGates = []
    data.currentPair = []
    data.connectedGates = [] #should be a list of len 2 lists
    data.clickedGate = False #checks if you clicked on a gate or not
    data.power = False #if power button is on or not
    data.powerColor = ["white", "light blue"] #power button colors
    data.lineColor = ["black", "red"] #possible color of connecting line

#checks if you clicked NOT button
def notCell(data, x, y):
    if x > 0 and x < data.cellSize and y > data.margin and y < data.margin \
    + data.cellSize:
        data.notClicked = True
        data.orClicked = False
        data.andClicked = False
        data.inputClicked = False
        data.outputClicked = False

#checks if you clicked AND button
def andCell(data, x, y):
    if x > 0 and x < data.cellSize and y > data.margin + data.cellSize and \
    y < data.margin + 2 * data.cellSize:
        data.notClicked = False
        data.orClicked = True
        data.andClicked = False
        data.inputClicked = False
        data.outputClicked = False

#checks if you clicked OR button        
def orCell(data, x, y):
    if x > 0 and x < data.cellSize and y > data.margin + 2 * data.cellSize and \
    y < data.width - 2 * data.cellSize:
        data.notClicked = False
        data.orClicked = False
        data.andClicked = True
        data.inputClicked = False
        data.outputClicked = False

#checks if you clicked INPUT button        
def inputCell(data, x, y):
    if x > 0 and x < data.cellSize and y > data.width - 2 * data.cellSize and \
    y < data.width - data.cellSize:
        data.notClicked = False
        data.orClicked = False
        data.andClicked = False
        data.inputClicked = True
        data.outputClicked = False

#checks if you cliked OUTPUT button
def outputCell(data, x, y):
    if x > 0 and x < data.cellSize and y > data.width - data.cellSize and \
    y < data.width:
        data.notClicked = False
        data.orClicked = False
        data.andClicked = False
        data.inputClicked = False
        data.outputClicked = True

#checks which button/cell you clicked if any        
def getCellClicked(data, x, y):
    notCell(data, x, y)
    andCell(data, x, y)
    orCell(data, x, y)
    inputCell(data, x, y)
    outputCell(data, x, y)

#checks if you clicked on the board and appends the gate you added onto board
def getBoardClicked(data, x, y):
    if x > data.cellSize and y > data.margin:
        #gate's info are appended into a list
        if data.notClicked == True:
            data.notGates.append(Not(x, y))
        if data.andClicked == True:
            data.andGates.append(And(x, y))
        if data.orClicked == True:
            data.orGates.append(Or(x, y))
        if data.inputClicked == True:
            data.inputGates.append(Input(x, y))
        if data.outputClicked == True:
            data.outputGates.append(Output(x, y))
        return True
    return False

#operates the clicking of two gates to connect them
def notClicked(data, x, y, boundary):
    for notGate in data.notGates:
        #checks if clicked within the gate boundary
        if x > notGate.cx - boundary and x < notGate.cx + boundary and y > \
        notGate.cy - boundary and y < notGate.cy + boundary:
            if len(data.currentPair) < 2:
                data.currentPair.append(notGate)
                #if just clicked on two gates
                if len(data.currentPair) == 2:
                    #connects the two gates with connectTo method
                    data.currentPair[0].connectTo(data.currentPair[1])
                    #adds pair into connectedGates list
                    data.connectedGates.append(data.currentPair)
                    #resets your current pair list
                    data.currentPair = []
            data.clickedGate = True 
 
#same procedure as notClicked but with or gate    
def orClicked(data, x, y, boundary):
    for orGate in data.orGates:
        if x > orGate.cx - boundary and x < orGate.cx + boundary and y > \
        orGate.cy - boundary and y < orGate.cy + boundary:
            if len(data.currentPair) < 2:
                data.currentPair.append(orGate)
                if len(data.currentPair) == 2:
                    data.currentPair[0].connectTo(data.currentPair[1])
                    data.connectedGates.append(data.currentPair)
                    data.currentPair = []
            data.clickedGate = True

#same procedure as notClicked but with and gate     
def andClicked(data, x, y, boundary):
    for andGate in data.andGates:
        if x > andGate.cx - boundary and x < andGate.cx + boundary and y > \
        andGate.cy - boundary and y < andGate.cy + boundary:
            if len(data.currentPair) < 2:
                data.currentPair.append(andGate)
                if len(data.currentPair) == 2:
                    data.currentPair[0].connectTo(data.currentPair[1])
                    data.connectedGates.append(data.currentPair)
                    data.currentPair = []
            data.clickedGate = True

def distance(x0, y0, x1, y1):
    return (((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)

#same procedure as notClicked but with input gate 
def inputClicked(data, x, y):
    radius = data.cellSize / 12
    for inputGate in data.inputGates:
        if distance(x, y, inputGate.cx, inputGate.cy) < radius:
            if len(data.currentPair) < 2:
                data.currentPair.append(inputGate)
                if len(data.currentPair) == 2:
                    data.currentPair[0].connectTo(data.currentPair[1])
                    data.connectedGates.append(data.currentPair)
                    data.currentPair = []
            data.clickedGate = True

#same procedure as notClicked but with output gate  
def outputClicked(data, x, y):
    radius = data.cellSize / 12
    for outputGate in data.outputGates:
        if distance(x, y, outputGate.cx, outputGate.cy) < radius:
            if len(data.currentPair) < 2:
                data.currentPair.append(outputGate)
                if len(data.currentPair) == 2:
                    data.currentPair[0].connectTo(data.currentPair[1])
                    data.connectedGates.append(data.currentPair)
                    data.currentPair = []
            data.clickedGate = True

#checks which gate on the board you clicked on if any
def gateClicked(data, x, y):
    boundary = data.cellSize / 6
    notClicked(data, x, y, boundary)
    orClicked(data, x, y, boundary)
    andClicked(data, x, y, boundary)
    inputClicked(data, x, y)
    outputClicked(data, x, y)

#method for clearing the board
def clearBoard(data, x, y):
    cx = data.width / 2
    cy = data.margin / 2
    width = data.cellSize / 2
    height = data.margin * (1 / 3)
    #calls init data if you click within the clear button
    if x > cx - data.cellSize - width and x < cx - data.cellSize + width and \
    y > cy - height and y < cy + height:
        init(data)

#method for 'turning on/off' the power button
def clickPower(data, x, y):
    cx = data.width / 2
    cy = data.margin / 2
    width = data.cellSize / 2
    height = data.margin * (1 / 3)
    #checks if clicked within the button
    if x > cx + data.cellSize - width and x < cx + data.cellSize + width and \
    y > cy - height and y < cy + height:
        data.power = not data.power #turns power to on/off
        data.notClicked = False
        data.orClicked = False
        data.andClicked = False
        data.inputClicked = False
        data.outputClicked = False
        if data.power == True:
            for inputGate in data.inputGates:
                inputGate.setInputValue(None, False) #defaults input to False
        elif data.power == False:
            for inputGate in data.inputGates:
                inputGate.outputValue = None #resets gate value to None when off

#checks if you clicked on input gate when power is on 
def clickedInput(data, x, y):
    radius = data.cellSize / 12
    for inputGate in data.inputGates:
        #checks boundary
        if distance(x, y, inputGate.cx, inputGate.cy) < radius:
            #if clicked on gate, calls the setInputValue for that input
            inputGate.setInputValue(None, not inputGate.outputValue)

#keeps track of all the mouse click features                
def mousePressed(event, data):
    # use event.x and event.y
    if data.power == True:
        #can only change input gate's output when power on
        clickedInput(data, event.x, event.y)
    else:
        data.clickedGate = False
        getCellClicked(data, event.x, event.y)
        gateClicked(data, event.x, event.y)
        if data.clickedGate != True:
            getBoardClicked(data, event.x, event.y)
    clearBoard(data, event.x, event.y)
    clickPower(data, event.x, event.y)

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

#draws the NOT gate button on the side bar
def drawNot(canvas, data):
    cx, cy = data.cellSize / 2, data.margin + data.cellSize / 2
    radius = data.cellSize / 6
    x0, y0 = cx - radius, cy - radius / 2
    x1, y1 = cx + radius, cy
    x2, y2 = cx - radius, cy + radius / 2
    inputX, inputY = cx - radius - data.lineLen, cy
    outputX, outputY = cx + radius + data.lineLen, cy
    #input node
    canvas.create_line(inputX,inputY,cx - radius,cy,fill = "green",width = 2)
    #output node
    canvas.create_line(outputX,outputY,cx + radius,cy,fill = "pink",width = 2)
    #gate shape
    canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill = "gray")
    #gate name
    canvas.create_text(cx, cy + 2 * radius, text = "NOT Gate")

#draws the OR gate button on the side bar
def drawOr(canvas, data):
    cx, cy = data.cellSize / 2, data.margin + data.cellSize * 3 / 2
    radius = data.cellSize / 6
    innerRadius = data.cellSize / 12
    x0, y0 = cx - innerRadius, cy
    x1, y1 = cx - radius, cy - radius
    x2, y2 = cx + radius, cy
    x3, y3 = cx - radius, cy + radius
    inputX1, inputY1 = x0 - data.lineLen, (y0 + y1) / 2
    inputX2, inputY2 = x0 - radius + data.lineLen, (y0 + y3) / 2
    outputX, outputY = cx + radius + data.lineLen, y2 
    canvas.create_line(inputX1, inputY1, cx - innerRadius, inputY1, fill = \
    "green", width = 2)
    canvas.create_line(inputX2, inputY2, cx - innerRadius, inputY2, fill = \
    "green", width = 2)
    canvas.create_line(outputX, outputY, x2, y2, fill = "pink", width = 2)
    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = "gray")
    canvas.create_text(cx, cy + 2 * radius, text = "OR Gate")

#draws the AND gate button on the side bar    
def drawAnd(canvas, data):
    cx, cy = data.cellSize / 2, data.margin + data.cellSize * 5 / 2
    radius = data.cellSize / 6
    x0, y0 = cx - radius, cy - radius
    x1, y1 = cx + radius / 2, y0
    x2, y2 = cx + radius, cy
    x3, y3 = x1, cy + radius
    x4, y4 = cx - radius, cy + radius
    inputX1, inputY1 = x0 - data.lineLen, cy - radius / 2
    inputX2, inputY2 = x0 - data.lineLen, cy + radius / 2
    outputX, outputY = x2 + data.lineLen, cy
    canvas.create_line(inputX1, inputY1, x0, cy - radius / 2, fill = "green", \
    width = 2)
    canvas.create_line(inputX2, inputY2, x0, cy + radius / 2, fill = "green", \
    width = 2)
    canvas.create_line(outputX, outputY, x2, y2, fill = "pink", width = 2)
    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, fill = "gray")
    canvas.create_text(cx, cy + 2 * radius, text = "AND Gate")

#draws the INPUT gate button on the side bar
def drawInput(canvas, data):
    cx, cy = data.cellSize / 2, data.margin + data.cellSize * 7 / 2
    innerRadius = data.cellSize / 16
    radius = data.cellSize / 12
    textDist = data.cellSize / 6
    outputX, outputY = cx + radius + data.lineLen, cy
    canvas.create_line(outputX, outputY, cx + radius, cy, fill = "pink", \
    width = 2)
    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, \
    fill = "pink") 
    canvas.create_oval(cx - innerRadius, cy - innerRadius, cx + innerRadius, \
    cy + innerRadius, fill = "black")
    canvas.create_text(cx, cy + 2 * textDist, text = "Input")
 
#draws the OUTPUT gate button on the side bar
def drawOutput(canvas, data):
    cx, cy = data.cellSize / 2, data.margin + data.cellSize * 9 / 2
    innerRadius = data.cellSize / 16
    radius = data.cellSize / 12
    textDist = data.cellSize / 6
    outputX, outputY = cx + radius + data.lineLen, cy
    canvas.create_line(outputX, outputY, cx - radius, cy, fill = "green", \
    width = 2)
    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, \
    fill = "green")#or color   
    canvas.create_oval(cx - innerRadius, cy - innerRadius, cx + innerRadius, \
    cy + innerRadius, fill = "black") 
    canvas.create_text(cx, cy + 2 * textDist, text = "Output") 

#draws the clear and power button on the top of screen    
def drawTopButtons(canvas, data):
    cx = data.width / 2
    cy = data.margin / 2
    width = data.cellSize / 2
    height = data.margin * (1 / 3)
    #controls the color of the power button
    if data.power == True:
        color = data.powerColor[1]
    else:
        color = data.powerColor[0]
    #draws the clear button at the top of screen
    canvas.create_rectangle(cx - data.cellSize - width, cy - height, cx - \
    data.cellSize + width, cy + height)
    canvas.create_text(cx - data.cellSize, cy, text = "Clear")
    #draws the power button at the top of screen
    canvas.create_rectangle(cx + data.cellSize - width, cy - height, cx + \
    data.cellSize + width, cy + height, fill = color)
    canvas.create_text(cx + data.cellSize, cy, text = "Power")

#get the bounds of the rectangle/square of the button
def getBounds(data, row):
    x0 = 0
    y0 = data.margin + row * data.cellSize
    x1 = data.cellSize
    y1 = y0 + data.cellSize
    return x0, y0, x1, y1

#draws each gate based off of each gate list
def drawGates(canvas, data):
    for notGate in data.notGates:
        notGate.draw(canvas, data)
    for orGate in data.orGates:
        orGate.draw(canvas, data)
    for andGate in data.andGates:
        andGate.draw(canvas, data)
    for inputGate in data.inputGates:
        if inputGate.outputValue == True: #changes input color when clicked
            color = "red"
        else:
            color = "black"
        inputGate.draw(canvas, data, color)
    for outputGate in data.outputGates:
        if outputGate.outputValue == True: #changes output color when clicked
            color = "red"
        else:
            color = "black"
        outputGate.draw(canvas, data, color)

#draws the line that connects two gates
def drawConnections(canvas, data):
    for connection in data.connectedGates:
        #if connected gate value is None or false, line is black; else it's red
        if data.power == False:
            color = None
        elif connection[0].outputValue != None:
            color = data.lineColor[int(connection[0].outputValue)]
        else:
            color = "black"
        #connects line with the outputLoc and inputLoc from class
        canvas.create_line(connection[0].outputLoc(data), \
        connection[1].inputLoc(data), fill = color, width = 2)

#draws all the buttons on the side and top of screen
def drawSideBar(canvas, data):
    drawNot(canvas, data)
    drawOr(canvas, data)
    drawAnd(canvas, data)
    drawInput(canvas, data)
    drawOutput(canvas, data)
    drawTopButtons(canvas, data)

#controls all the things that needs to be drawn on board
def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_line(0, data.margin, data.width, data.margin, width = 5)
    for row in range(data.buttonNum):
        canvas.create_rectangle(getBounds(data, row))
    drawSideBar(canvas, data)
    drawGates(canvas, data)
    drawConnections(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)
################################################################################
# hw4-3 tests
################################################################################

def testFindRTP():
    print("Testing findRTP()...", end="")
    assert(findRTP(0) == None)
    assert(findRTP(1) == 2)
    assert(findRTP(100) == None)
    assert(findRTP(8) == 23399339)
    assert(findRTP(3) == 233)
    assert(findRTP(5) == 23333)
    print("Passed!")
    
# def testGateClass0_basics():
#     gate1 = Gate()
#     gate2 = Gate()
#     assert(gate1.getInputGates() == [])
#     assert(gate1.getOutputGates() == [])
# 
#     assert(gate1.inputValues == [ ])
#     assert(gate1.outputValue == None)
# 
#     # you can connect gates to each other! 
#     gate1.connectTo(gate2)
#     assert(gate1.getOutputGates() == [gate2])
#     assert(gate2.getInputGates() == [gate1])
# 
#     # gate2 now has gate1 as an input, but since gate1.outputValue = None,
#     # gate2.inputValues == [(gate1,None)]
#     assert(gate2.inputValues == [(gate1, None)])
# 
# def testGateClass1_inputToOutput():
#     # Connect an input gate to an output gate
#     in1 = Input()
#     out1 = Output()
#     in1.connectTo(out1)
# 
#     assert(in1.getInputGates() == [ ])
#     assert(in1.getMaxInputGates() == 0) # an input gate can't have any inputs
#     assert(in1.getOutputGates() == [ out1 ])
#     assert(out1.getInputGates() == [ in1 ])
#     assert(out1.getMaxInputGates() == 1)
#     assert(out1.getOutputGates() == [ ])
# 
#     assert(in1.inputValues == [ ])
#     assert(in1.outputValue == None)
#     assert(out1.inputValues == [(in1, None)])
#     assert(out1.outputValue == None)
# 
#     in2 = Input()
#     in2.connectTo(out1)
#     # since out1 has a maximum of one input, and it already has in1 as an input,
#     # this shouldn't do anything!
#     assert(in2.getOutputGates() == [])
#     assert(out1.getInputGates() == [ in1 ])
# 
#     # setInputValue should take in two values - a fromGate and a value, which
#     # represent the gate the input is coming from, and the value of that gate.
#     # Here, in1 is an input gate, meaning that it's input isn't coming from
#     # anywhere! So, the fromGate = None, and the value = True in this case.
# 
#     # be careful to examine the test cases to figure out what happens to the
#     # gates you're connected to once you set the input value!
#     in1.setInputValue(None, True)
# 
#     assert(in1.inputValues == [(None,True)])
#     assert(in1.outputValue == True)
#     assert(out1.inputValues == [(in1,True)])
#     assert(out1.outputValue == True)
#     # and set the input to False
#     in1.setInputValue(None, False)
#     assert(in1.inputValues == [(None,False)])
#     assert(in1.outputValue == False)
#     assert(out1.inputValues == [(in1,False)])
#     assert(out1.outputValue == False)
# 
# def testGateClass2_oneNotGate():
#     in1 = Input()
#     out1 = Output()
#     not1 = Not()
#     in1.connectTo(not1)
#     not1.connectTo(out1)
# 
#     assert(in1.outputValue == not1.outputValue == out1.outputValue == None)
# 
#     in1.setInputValue(None, False)
#     assert(not1.inputValues == [(in1,False)])
#     assert(out1.inputValues == [(not1,True)])
#     assert(out1.outputValue == True)
# 
#     in1.setInputValue(None, True)
#     assert(not1.inputValues == [(in1,True)])
#     assert(out1.inputValues == [(not1,False)])
#     assert(out1.outputValue == False)
# 
# def testGateClass3_oneAndGate():
#     in1 = Input()
#     in2 = Input()
#     out1 = Output()
#     and1 = And()
#     in1.connectTo(and1)
#     in2.connectTo(and1)
#     and1.connectTo(out1)
# 
#     assert(out1.outputValue == None)
#     in1.setInputValue(None, False)
#     assert(and1.inputValues == [(in1,False), (in2,None)])
#     assert(and1.outputValue == None) # not ready, need both inputs
#     in2.setInputValue(None, False)
#     assert(and1.inputValues == [(in1,False), (in2,False)])
#     assert(and1.outputValue == False)
#     assert(out1.outputValue == False)
# 
#     in1.setInputValue(None, True)
#     assert(and1.inputValues == [(in1,True), (in2,False)])
#     assert(out1.outputValue == False)
# 
#     in2.setInputValue(None, True)
#     assert(and1.inputValues == [(in1,True), (in2,True)])
#     assert(out1.outputValue == True)
# 
# def testGateClass4_oneOrGate():
#     in1 = Input()
#     in2 = Input()
#     out1 = Output()
#     or1 = Or()
#     in1.connectTo(or1)
#     in2.connectTo(or1)
#     or1.connectTo(out1)
# 
#     assert(or1.inputValues == [(in1,None), (in2,None)])
#     assert(or1.outputValue == None)
#     assert(out1.outputValue == None)
#     in1.setInputValue(None, False)
#     assert(or1.inputValues == [(in1,False), (in2,None)])
#     assert(or1.outputValue == None) # not ready, need both inputs
#     in2.setInputValue(None, False)
#     assert(or1.inputValues == [(in1,False), (in2,False)] )
#     assert(or1.outputValue == False)
#     assert(out1.outputValue == False)
# 
#     in1.setInputValue(None, True)
#     assert(or1.inputValues == [(in1,True), (in2,False)])
#     assert(out1.outputValue == True)
# 
#     in2.setInputValue(None, True)
#     assert(or1.inputValues == [(in1,True), (in2,True)])
#     assert(out1.outputValue == True)
# 
# def testGateClass5_xor():
#     in1 = Input()
#     in2 = Input()
#     out1 = Output()
#     and1 = And()
#     and2 = And()
#     not1 = Not()
#     not2 = Not()
#     or1 = Or()
#     in1.connectTo(and1)
#     in1.connectTo(not1)
#     in2.connectTo(and2)
#     in2.connectTo(not2)
#     not1.connectTo(and2)
#     not2.connectTo(and1)
#     and1.connectTo(or1)
#     and2.connectTo(or1)
#     or1.connectTo(out1)
# 
#     in1.setInputValue(None, False)
#     in2.setInputValue(None, False)
#     assert(out1.outputValue == False)
# 
#     in1.setInputValue(None, True)
#     in2.setInputValue(None, False)
#     assert(out1.outputValue == True)
# 
#     in1.setInputValue(None, False)
#     in2.setInputValue(None, True)
#     assert(out1.outputValue == True)
# 
#     in1.setInputValue(None, True)
#     in2.setInputValue(None, True)
#     assert(out1.outputValue == False)
# 
# def testGateClass():
#     print("Testing Gate class... ", end="")
#     testGateClass0_basics()
#     testGateClass1_inputToOutput()
#     testGateClass2_oneNotGate()
#     testGateClass3_oneAndGate()
#     testGateClass4_oneOrGate()
#     testGateClass5_xor()
#     print("Passed!")
# 
def testAll():
    testFindRTP()
#     testGateClass()
 
def main():
    testAll()
 
if __name__ == '__main__':
    main()