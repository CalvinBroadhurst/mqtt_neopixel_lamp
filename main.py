import gc
import ujson
import network
from utime import sleep
from utime import sleep_ms
from machine import Pin, reset
from neopixel import NeoPixel
from umqtt.robust import MQTTClient

# Define some basic colours
led_off = (0, 0, 0)
led_red = (32, 0, 0)
led_green = (0, 32, 0)
led_blue = (0, 0, 32)


with open("./config.json") as fp:
    config = ujson.load(fp)

pin = Pin(config["neopixel_pin"], Pin.OUT) 
np = NeoPixel(pin, config["pixel_count"])

heartbeat = Pin(2, Pin.OUT)  # Pin 2 is connected to the blue LED on Wemos board

client = MQTTClient(config["mqtt_client"], config["mqtt_server"])

############## Here we go then #################

def goLamp():
    client.set_callback(do_callback)

    if not client.connect(clean_session=True):
        print("New session being set up")
        client.subscribe(config["mqtt_topic"])

    while 1:
        print("waiting for message")
        client.wait_msg() 
        gc.collect()


def do_callback(topic, msg):
    value = str(msg, "utf-8")
    print("value: " + value)
    splitval = value.split(",")
    red = int(splitval[0])
    green = int(splitval[1])
    blue = int(splitval[2])
    print(red, green, blue)
    lampcolour = (red, green, blue)
    np.fill(lampcolour)
#    for i in range(0, config["pixel_count"]):
#        np[i] = lampcolour
    np.write()

def spin_the_ring():
    # If we are running on micropython then spin the LED's on the ring
    np.fill(led_off)
    np.write()
    for i in range(0, config["pixel_count"]):
        np[i] = led_blue
        if i > 0:
            np[i - 1] = led_green
        if i > 1:
            np[i - 2] = led_red
        if i > 2:
            np[i - 3] = led_off
        np.write()
        sleep_ms(50)
    np.fill(led_off)
    np.write()

# If we are being imported as a module then do nothing
# If we are being run as a script then run
if __name__ == '__main__':
    gc.enable()
    
    sta_if = network.WLAN(network.STA_IF)

    while not sta_if.isconnected():
        print("Not connected to WiFi")
        sleep(5)
    
    try:
        spin_the_ring()
        goLamp()
    except Exception as e:
        print("Something has gone horribly wrong")
        print(e)
        sleep(10)
        reset()
