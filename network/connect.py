''' 
Code to connect a Pico W to wifi
see micropython>networking (https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html)
'''

# ('BT-7NCKRR', 'YMpbAPf3NG7qQN')

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('<ssid>', '<key>')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())