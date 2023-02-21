import mb3x3
import mb5x5
import unicorn7x17
import color

INTERVAL = 0.09

SCREEN = unicorn7x17

# the message to print
message = "Merry Christmas"

while True:
    SCREEN.display(message, INTERVAL)
