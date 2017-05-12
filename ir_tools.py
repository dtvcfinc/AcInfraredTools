import RPi.GPIO as GPIO
from datetime import datetime
import fire
import json
#Pin for the IR receptor.
INPUT_WIRE = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_WIRE, GPIO.IN)
CEND = '\033[0m'
OKGREEN = '\033[32m'
RED = '\033[31m'
BLUE = '\033[34m'
def compare(a, b):
        diff = []
        for i in range(len(a)):
                if i < len(b):
                        if a[i] == b[i]:
                                diff.append("1")
                        else:
                                diff.append("0")
                else:
                        diff.append(a[i])
        return diff

def applyColor(binaryString, diff):
        binaryStringColored = []
        if len(binaryString) != len(diff):
                return
        for i in range(len(binaryString)):
                # Applies red color
                if diff[i] == "0":
                        binaryStringColored.append(redColorString(binaryString[i]))
                # Applies green color
                elif diff[i] == "1":
                        binaryStringColored.append(greenColorString(binaryString[i]))
                else:
                        binaryStringColored.append(binaryString[i])
        return binaryStringColored

def greenColorString(string):
   return OKGREEN + string + CEND
   
def blueColorString(string):
   return BLUE + string + CEND

def redColorString(string):
   return RED + string + CEND

def tokenizeInBytes(binaryString):
    n = 8
    byteArr = [binaryString[i:i+n] for i in range(1, len(binaryString), n)]
    byteString = binaryString[0] + " " + ' '.join(byteArr)
    return byteString
        
def readCommand():
    startTime = datetime.now()
    command = []
    # Used to check when the command is finished
    # after an arbirary number of 1s (1 is off for my IR receiver)
    numOnes = 0
    previousVal = 0
    value = 0
    while True:
        if value != previousVal:
            # When the value changes calculate the pulse's lenght.
            now = datetime.now()
            pulseLength = now - startTime
            startTime = now
            command.append((previousVal, pulseLength.microseconds))

        if value:
            numOnes = numOnes + 1
        else:
            numOnes = 0

        # 10000 is arbitrary, adjust as necessary
        if numOnes > 10000: 
            break
        previousVal = value
        value = GPIO.input(INPUT_WIRE)
    return command

def readRawCommands():
    while True:
        value = 1
        # Loop until we read a 0
        while value:
            value = GPIO.input(INPUT_WIRE)
        command = readCommand()    
        print(json.dumps(command))
        
def exportRawCommand(commandName):   
    while True:
        value = 1
        # Loop until we read a 0
        while value:
            value = GPIO.input(INPUT_WIRE)
        command = readCommand()    
        textFile = open(commandName, "w")
        textFile.write(json.dumps(command))
        textFile.close()
        break
        
def compareRawCommands(compareComand):
    #100ms of tolerance was enough for my ac unit.
    tolerance = 100
    while True:
        value = 1
        # Loop until we read a 0
        while value:
            value = GPIO.input(INPUT_WIRE)
        command = readCommand()    
        i = 0
        for value,pulse in command:
            comparePulse =  compareComand[i][1]
            comparePulseString = ""
            if abs(pulse - comparePulse) < tolerance:
                comparePulseString = greenColorString(str(pulse))
            else:
                if comparePulse >  pulse:
                    comparePulseString = blueColorString(str(pulse))
                else:
                     comparePulseString = redColorString(str(pulse))
            print("%s," %(comparePulseString)),     
            i+=1   
                
        print("\n\n")
        
def readBinaryCodes():
    previousBinaryString = ""
    previousBinaryByteString = ""
    while True:
        value = 1
        # Loop until we read a 0
        while value:
            value = GPIO.input(INPUT_WIRE)
        command = readCommand()    
        binaryString = "".join(map(lambda x: "1" if x[1] > 1000 else "0", filter(lambda x: x[0] == 1, command)))
        binaryByteString = tokenizeInBytes(binaryString)
        print ("Current value: " + binaryByteString)
        print ("Prev    value: " + previousBinaryByteString)
        diffString = "".join(compare(binaryString,previousBinaryString))
        diffByteString  = tokenizeInBytes(diffString)
        print ("Diff    value: " + "".join(applyColor(binaryByteString, diffByteString)) + "\n")
        previousBinaryByteString = binaryByteString
        previousBinaryString = binaryString
        
        
def rawCodeComparator(rawFile):
   with open(rawFile) as data_file:    
       previousRawData = json.load(data_file)
       compareRawCommands(previousRawData)
       
fire.Fire()
