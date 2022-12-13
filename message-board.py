import time
import ascii5x5 as l
from breakout_bme68x import BreakoutBME68X
from breakout_rgbmatrix5x5 import BreakoutRGBMatrix5x5
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
i2c = PimoroniI2C(**PICO_EXPLORER_I2C_PINS)
# bme = BreakoutBME68X(i2c, address=0x76)
rgb = BreakoutRGBMatrix5x5(i2c, address=0x74)

# colors
RED = (60, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

INTERVAL = 0.09

# blank col
BLANK = [0,0,0,0,0]

decoder = {
    'a': l.A,
    'b': l.B,
    'c': l.C,
    'd': l.D,
    'e': l.E,
    'f': l.F,
    'g': l.G,
    'h': l.H,
    'i': l.I,
    'j': l.J,
    'k': l.K,
    'l': l.L,
    'm': l.M,
    'n': l.N,
    'o': l.O,
    'p': l.P,
    'q': l.Q,
    'r': l.R,
    's': l.S,
    't': l.T,
    'u': l.U,
    'v': l.V,
    'w': l.W,
    'x': l.X,
    'y': l.Y,
    'z': l.Z,
    ' ': l.SPACE,
    '!': l.EXCLAMATION,
    '?': l.QUESTION_MARK,
    '.': l.PERIOD
}


# turn message into array of pixel columns to display
def createMessageArray(message):
    # add blank to end of message
    # message.append('     ')

    messageArray = []
    for c in message:
        for a in decoder[c.lower()]:
            messageArray.append(a)
        messageArray.append(BLANK)


    return messageArray


def displayFrame(frame, color=RED):
    r, g, b = color
    print(frame)
    print('\n')
    for i in range(0, 5):
            for j in range(0, 5):
                if frame[i][j] == 1:
                    rgb.set_pixel(j, i, r, g, b)
                else:
                    rgb.set_pixel(j, i, 0, 0, 0)
    rgb.update()

def display(message):
    # create the message array
    messageArray = createMessageArray(message)
    #print(messageArray)
   
    # set the color
    r, g, b = RED
    # clear the screen
    rgb.clear()
    rgb.update()

    
    
    # on a set interval, move the message through the screen
    columns = len(messageArray)
    for i in range(0, columns):
        print(f'i:{i} of {columns}')
        if columns - i < 5:
            col0 = BLANK
        else:
            col0 = messageArray[i]
        
        if columns - i < 2:
            col1 = BLANK
        else:
            col1 = messageArray[i + 1]
       
        if columns - i < 3:
            col2 = BLANK
        else:
            col2 = messageArray[i + 2]
        
        if columns - i < 4:
            col3 = BLANK
        else: 
            col3 = messageArray[i + 3]
        
        if columns - i < 5:
            col4 = BLANK
        else:
            col4 = messageArray[i + 4]
    
        # set columns into the screen
        frame = [col0, col1, col2, col3, col4]
        displayFrame(frame)
        time.sleep(INTERVAL)

        
        
    


# the message to print
message = "Merry Christmas!"

while True:
    display(message)
