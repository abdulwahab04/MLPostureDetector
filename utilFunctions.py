import math as m
import time
import pyttsx3
import threading

engine = pyttsx3.init()
lastTime = 0

# Function to calculate the angle between two points using vectors
def getAngle(x1, y1, x2, y2):
    angle = m.acos((y2 -y1)*(-y1)/(m.sqrt((x2 - x1)**2 + (y2 - y1)**2)*y1))
    angleDegree = m.degrees(angle)
    return angleDegree

# Function to convert text to speech
def textToSpeech(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Function to warn the user if they have been in bad posture for more than 60 seconds in 2 minute intervals
# Also uses threading so that the warning doesn't interrupt the main program
def warning(badPostureTime):
    global lastTime
    currentTime = time.time()
    warningInterval = 120
    if (badPostureTime > 60 and ((currentTime - lastTime) > warningInterval)):
        t = threading.Thread(target=textToSpeech, args=("You have been in bad posture for " + str(int(badPostureTime)) + " seconds. Please correct your posture.",))
        t.start()
        lastTime = currentTime