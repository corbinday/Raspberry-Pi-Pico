import time
from breakout_bme68x import BreakoutBME68X
from breakout_rgbmatrix5x5 import BreakoutRGBMatrix5x5
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
i2c = PimoroniI2C(**PICO_EXPLORER_I2C_PINS)
#bme = BreakoutBME68X(i2c, address=0x76)
rgb = BreakoutRGBMatrix5x5(i2c, address=0x74)

while True:
    time.sleep(1)
    rgb.clear()
    rgb.update()
    time.sleep(1)
    for i in range(5):
        for j in range(5):
            rgb.set_pixel(i, j, 255, 0, 0)
            time.sleep(.25)
            rgb.update()

