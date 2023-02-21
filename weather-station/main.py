# This example lets you plug a BME280 breakout into your Pico Explorer and make a little indoor weather station, with barometer style descriptions.

import time
from breakout_bme280 import BreakoutBME280
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER
import machine

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
i2c = PimoroniI2C(**PICO_EXPLORER_I2C_PINS)
bme = BreakoutBME280(i2c, address=0x76)

# set up the buttons
button_a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button_b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button_x = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button_y = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# variable to hold last pressed button
CURRENT_BUTTON = 'a'

# button event handlers


def button_a_handler(pin):
    global CURRENT_BUTTON
    CURRENT_BUTTON = 'a'
    print('a pressed')


def button_b_handler(pin):
    global CURRENT_BUTTON
    CURRENT_BUTTON = 'b'
    print('b pressed')


def button_x_handler(pin):
    global CURRENT_BUTTON
    CURRENT_BUTTON = 'x'
    print('x pressed')


def button_y_handler(pin):
    global CURRENT_BUTTON
    CURRENT_BUTTON = 'y'
    print('y pressed')


# set button event listeners
button_a.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_a_handler)
button_b.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_b_handler)
button_x.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_x_handler)
button_y.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_y_handler)

# lets set up some pen colours to make drawing easier
# this colour will get changed in a bit
TEMPCOLOUR = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(255, 0, 0)
GREY = display.create_pen(125, 125, 125)


# converts the temperature into a barometer-type description and pen colour
def describe_temperature(temperature):
    global TEMPCOLOUR
    if temperature < 10:
        description = "very cold"
        TEMPCOLOUR = display.create_pen(0, 255, 255)
    elif 10 <= temperature < 20:
        description = "cold"
        TEMPCOLOUR = display.create_pen(0, 0, 255)
    elif 20 <= temperature < 25:
        description = "temperate"
        TEMPCOLOUR = display.create_pen(0, 255, 0)
    elif 25 <= temperature < 30:
        description = "warm"
        TEMPCOLOUR = display.create_pen(255, 255, 0)
    elif temperature >= 30:
        description = "very warm"
        TEMPCOLOUR = display.create_pen(255, 0, 0)
    else:
        description = ""
        TEMPCOLOUR = display.create_pen(0, 0, 0)
    return description

# converts pressure into barometer-type description


def describe_pressure(pressure):
    if pressure < 970:
        description = "storm"
    elif 970 <= pressure < 990:
        description = "rain"
    elif 990 <= pressure < 1010:
        description = "change"
    elif 1010 <= pressure < 1030:
        description = "fair"
    elif pressure >= 1030:
        description = "dry"
    else:
        description = ""
    return description


# converts humidity into good/bad description
def describe_humidity(humidity):
    if 40 < humidity < 60:
        description = "good"
    else:
        description = "bad"
    return description


# vars to hold line positions
TOP = (10, 10, 240, 3)
MIDDLE = (10, 50, 240, 8)
BOTTOM = (10, 130, 240, 3)
# display a (temperature)


def display_a(temperature):
    display.set_pen(WHITE)
    display.text("temperature:", *TOP)
    display.set_pen(TEMPCOLOUR)
    display.text('{:.1f}'.format(temperature) + 'C', *MIDDLE)
    display.set_pen(WHITE)
    display.text(describe_temperature(temperature), *BOTTOM)

# display b (pressure)


def display_b(pressure):
    display.set_pen(WHITE)
    display.text("pressure (hPa):", *TOP)
    display.text('{:.0f}'.format(pressurehpa), *MIDDLE)
    display.text(describe_pressure(pressurehpa), *BOTTOM)

# display x (humidity)


def display_x(humidity):
    display.set_pen(WHITE)
    display.text("humidity:", *TOP)
    display.text('{:.0f}'.format(humidity) + '%', *MIDDLE)
    display.text(describe_humidity(humidity), *BOTTOM)

# display y (whatever you want!)


def display_y():
    pass


while True:
    display.set_pen(BLACK)
    display.clear()

    # read the sensors
    temperature, pressure, humidity = bme.read()
    # pressure comes in pascals which is a reight long number, lets convert it to the more manageable hPa
    pressurehpa = pressure / 100

    if CURRENT_BUTTON == 'a':
        display_a(temperature)
    elif CURRENT_BUTTON == 'b':
        display_b(pressurehpa)
    elif CURRENT_BUTTON == 'x':
        display_x(humidity)
    else:
        display_y()

    # time to update the display
    display.update()

    # waits for 1 second and clears to BLACK
    time.sleep(.5)
